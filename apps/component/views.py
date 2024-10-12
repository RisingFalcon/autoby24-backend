from dj_rest_kit.views import BaseUUIDViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.vehicle import models, serializers, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import uuid
from django.utils import timezone
from apps.package.models import Package, Subscription
from apps.package.permissions import IsAdminUser
from django.db.models import Q
from django.db.models import Count, Case, When, IntegerField
from .models import (
    Component,
    ComponentCategory,
    ComponentImage,
    ComponentWishlists
)
from .serializers import (
    ComponentCategorySerializer,
    ComponentImageSerializer,
    ComponentSerializer,
    ComponentWishlistSerializer
)
from .filters import ComponentFilter


class ComponentCategoryViewSet(BaseUUIDViewSet):
    queryset = ComponentCategory.objects.all()
    serializer_class = ComponentCategorySerializer


class ComponentViewSet(BaseUUIDViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ComponentFilter
    ordering_fields = ['price', 'weight', 'stock_quantity']
    ordering = ['price']  # Default ordering

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"message": f"{instance.name} updated successfully", "data": serializer.data})


    def get_queryset(self):
        queryset = Component.objects.select_related("maker", "user", "subscription", "category").all()
        vehicle_type = self.request.query_params.get('vehicle_type')
        if vehicle_type in ['1', '2']:
            queryset = queryset.filter(vehicle_type=int(vehicle_type))
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='summary')
    def summary(self, request):
        user_id = self.request.query_params.get("user_id")
        subscription_id = self.request.query_params.get("subscription_id")
        
        components = Component.objects.all()
        if user_id:
            components = components.filter(user__uuid=user_id)
        if subscription_id:
            components = components.filter(subscription__uuid=subscription_id)
        
        component_counts = components.aggregate(
            total_count=Count('id'),
            active_count=Count(Case(When(is_active=True, then=1), output_field=IntegerField())),
            verified_count=Count(Case(When(is_verify=True, then=1), output_field=IntegerField())),
            sold_count=Count(Case(When(is_sold=True, then=1), output_field=IntegerField())),
            featured_count=Count(Case(When(is_featured=True, then=1), output_field=IntegerField())),
            pending_approval=Count(Case(When(status=2, then=1), output_field=IntegerField())),
            rejected_approval=Count(Case(When(status=0, then=1), output_field=IntegerField())),
            approved_approval=Count(Case(When(status=1, then=1), output_field=IntegerField())),
        )

        return Response({
            "total": component_counts["total_count"],
            "active_count": component_counts["active_count"],
            "verified_count": component_counts["verified_count"],
            "sold_count": component_counts["sold_count"],
            "featured_count": component_counts["featured_count"],
            "pending_approval": component_counts["pending_approval"],
            "rejected_approval": component_counts["rejected_approval"],
            "approved_approval": component_counts["approved_approval"]
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='sold')
    def component_sold(self, request):
        component_uuid = self.request.query_params.get("component_id")
        try:
            componenet = Component.objects.get(uuid=component_uuid)
            if componenet.is_sold:
                return Response({"error": "Componenet already marked as sold!"}, status=status.HTTP_400_BAD_REQUEST)
            componenet.is_sold = True
            componenet.save()
            return Response({"message": "Component has been marked as sold."}, status=status.HTTP_200_OK)
        except Component.DoesNotExist as err:
            return Response({"error": "Component doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


class ComponentWishlistViewSet(BaseUUIDViewSet):
    http_method_names = ["delete", "post", "get"]
    queryset = ComponentWishlists.objects.select_related("component", "user").all()
    serializer_class = ComponentWishlistSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
