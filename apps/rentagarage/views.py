from rest_framework import viewsets, permissions, status
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.rentacar import filters
from apps.core.custom_permissions import IsAdminOrReadOnly
from apps.package.models import Subscription, Package, CustomPackage
from .models import (
    GarageRental,  
    RentaGarageImage
    )

from .serializers import (
    RentagarageImageSerializer, 
    GarageRentalSerializer
    )


class GarageRentalViewSet(viewsets.ModelViewSet):
    queryset = GarageRental.objects.all()
    serializer_class = GarageRentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        subscription = Subscription.objects.filter(user=user, is_expired=False, package__package_type=11).first()
        order_number = 1000
        if subscription:  
            order_number = 1
        serializer.save(user=user, order_number=order_number)
        
    
    def perform_update(self, serializer):
        serializer.save()


class GarageImageViewSet(viewsets.ModelViewSet):
    queryset = RentaGarageImage.objects.all()
    serializer_class = RentagarageImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UpdateUserGaragesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        subscription = Subscription.objects.filter(
            user=user, 
            is_expired=False, 
            package__package_type=11
        ).first()

        if subscription:
            cars = GarageRental.objects.filter(user=user)
            cars.update(order_number=1) 
            serializer = GarageRentalSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No valid subscription found."}, status=status.HTTP_404_NOT_FOUND)


class GarageRentalSearchListView(generics.ListAPIView):
    queryset = GarageRental.objects.all()
    serializer_class = GarageRentalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'type': ['exact'],
        'garage_condition': ['icontains'],
        'monthly_rent_price': ['gte', 'lte'],
        'country__name': ['exact', 'icontains'],
        'state__name': ['exact', 'icontains'],
        'city__name': ['exact', 'icontains'],
        'postal_code': ['exact', 'icontains'],
        'street_name': ['exact', 'icontains'],
        'street_number': ['exact'],
        'status': ['exact'],
        'pickup_date': ['exact', 'gte', 'lte'],
        'return_date': ['exact', 'gte', 'lte'],
    }
    search_fields = ['name', 'type', 'garage_condition']
    ordering_fields = ['monthly_rent_price', 'pickup_date', 'return_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by features
        standard_features_uuids = self.request.query_params.getlist('standard_features')
        optional_features_uuids = self.request.query_params.getlist('optional_features')

        if standard_features_uuids:
            queryset = queryset.filter(
                Q(standard_features__uuid__in=standard_features_uuids)
            ).distinct()

        if optional_features_uuids:
            queryset = queryset.filter(
                Q(optional_features__uuid__in=optional_features_uuids)
            ).distinct()

        # Additional custom filters
        pickup_date = self.request.query_params.get('pickup_date')
        return_date = self.request.query_params.get('return_date')

        if pickup_date:
            queryset = queryset.filter(pickup_date__lte=pickup_date)
        if return_date:
            queryset = queryset.filter(return_date__gte=return_date)

        return queryset

class UserGarageListView(generics.ListAPIView):
    serializer_class = GarageRentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the cars that belong to the authenticated user
        return GarageRental.objects.filter(user=self.request.user)