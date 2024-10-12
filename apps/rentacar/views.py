from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# import 
from apps.rentacar import filters
from apps.core.custom_permissions import IsAdminOrReadOnly
from apps.package.models import Subscription, Package, CustomPackage
from .models import (
    CarRental,  
    CarImage,
    )

from .serializers import (
    CarRentalSerializer,  
    CarImageSerializer,
    CarImageSerializer,
    CarRentalSearchSerializer
    )

class CarRentalViewSet(viewsets.ModelViewSet):
    queryset = CarRental.objects.all()
    serializer_class = CarRentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CarRental.objects.all().order_by('order_number', '-updated_at')
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    def perform_create(self, serializer):
        user = self.request.user
        subscription = Subscription.objects.filter(user=user, is_expired=False, package__package_type=9).first()
        order_number = 1000
        if subscription:  
            order_number = 1
        serializer.save(user=user, order_number=order_number)
    
    def perform_update(self, serializer):
        serializer.save()


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UpdateUserCarsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        subscription = Subscription.objects.filter(
            user=user, 
            is_expired=False, 
            package__package_type=9
        ).first()

        if subscription:
            cars = CarRental.objects.filter(user=user)
            cars.update(order_number=1) 
            serializer = CarRentalSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No valid subscription found."}, status=status.HTTP_404_NOT_FOUND)
    
class CarRentalSearchListView(generics.ListAPIView):
    queryset = CarRental.objects.all()
    serializer_class = CarRentalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'brand__name': ['exact', 'icontains'],
        'model__name': ['exact', 'icontains'],
        'running_mileage': ['gte', 'lte'],
        'vehicle_condition': ['exact'],
        'body_type': ['exact'],
        'daily_base_price': ['gte', 'lte'],
        'registration_year': ['exact', 'gte', 'lte'],
        'registration_month': ['exact'],
        'horse_power': ['gte', 'lte'],
        'cubic_capacity': ['gte', 'lte'],
        'luggage_capacity': ['gte', 'lte'],
        'seats': ['exact'],
        'doors': ['exact'],
        'interior_color': ['exact', 'icontains'],
        'exterior_color': ['exact', 'icontains'],
        'country__name': ['exact', 'icontains'],
        'transmission': ['exact'],
        'fuel_type': ['exact'],
        'retail_value': ['gte', 'lte'],
    }
    search_fields = ['brand__name', 'model__name']
    ordering_fields = ['daily_base_price', 'registration_year', 'running_mileage']

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

        return queryset

class UserCarsListView(generics.ListAPIView):
    serializer_class = CarRentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the cars that belong to the authenticated user
        return CarRental.objects.filter(user=self.request.user)