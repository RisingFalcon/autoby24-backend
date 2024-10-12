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
from apps.vehicle.models import Brand, Model
from apps.features.models import (
    MultimediaFeature,
    OptionalFeature,
    SafetyAssistanceFeature,
    StandardFeature
)

from .models import (
    BikeRental, 
    BikeImage
    )

from .serializers import (
    BikeRentalSerializer, 
    MultimediaFeatureSerializer, 
    SafetyAssistanceFeatureSerializer, 
    BikeImageSerializer
    )

class BikeRentalViewSet(viewsets.ModelViewSet):
    queryset = BikeRental.objects.all()
    serializer_class = BikeRentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        subscription = Subscription.objects.filter(user=user, is_expired=False, package__package_type=10).first()
        order_number = 1000
        if subscription:  
            order_number = 1
        serializer.save(user=user, order_number=order_number)
        
    
    def perform_update(self, serializer):
        serializer.save()


class BikeImageViewSet(viewsets.ModelViewSet):
    queryset = BikeImage.objects.all()
    serializer_class = BikeImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UpdateUserBikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        subscription = Subscription.objects.filter(
            user=user, 
            is_expired=False, 
            package__package_type=10
        ).first()

        if subscription:
            cars = BikeRental.objects.filter(user=user)
            cars.update(order_number=1) 
            serializer = BikeRentalSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No valid subscription found."}, status=status.HTTP_404_NOT_FOUND)


class BikeRentalSearchListView(generics.ListAPIView):
    queryset = BikeRental.objects.all()
    serializer_class = BikeRentalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'brand__name': ['exact', 'icontains'],
        'model__name': ['exact', 'icontains'],
        'running_mileage': ['gte', 'lte'],
        'body_type': ['exact'],
        'registration_month': ['exact'],
        'registration_year': ['exact', 'gte', 'lte'],
        'interior_color': ['exact', 'icontains'],
        'vehicle_condition': ['exact'],
        'transmission': ['exact'],
        'daily_base_price': ['gte', 'lte'],
        'country__name': ['exact', 'icontains'],
        'state__name': ['exact', 'icontains'],
        'city__name': ['exact', 'icontains'],
        'fuel_type': ['exact'],
        'energy_efficiency': ['exact'],
        'horse_power': ['gte', 'lte'],
        'fuel_consumption': ['gte', 'lte'],
        'status': ['exact'],
        'pickup_date': ['exact', 'gte', 'lte'],
        'return_date': ['exact', 'gte', 'lte'],
    }
    search_fields = ['brand__name', 'model__name', 'license_number']
    ordering_fields = ['daily_base_price', 'registration_year', 'running_mileage', 'horse_power']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by features
        multimedia_uuids = self.request.query_params.getlist('multimedia')
        safety_assistance_uuids = self.request.query_params.getlist('safety_and_assistance')
        standard_features_uuids = self.request.query_params.getlist('standard_features')
        optional_features_uuids = self.request.query_params.getlist('optional_features')

        if multimedia_uuids:
            queryset = queryset.filter(
                Q(multimedia__uuid__in=multimedia_uuids)
            ).distinct()
        if safety_assistance_uuids:
            queryset = queryset.filter(
                Q(safety_and_assistance__uuid__in=safety_assistance_uuids)
            ).distinct()
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

class UserBikeListView(generics.ListAPIView):
    serializer_class = BikeRentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the cars that belong to the authenticated user
        return BikeRental.objects.filter(user=self.request.user)