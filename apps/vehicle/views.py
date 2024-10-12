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
from django.db.models import Count, Case, When, IntegerField, Q


class BrandViewSet(BaseUUIDViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    filterset_class = filters.BrandFilter
    permission_classes = [AllowAny]


class ModelViewSet(BaseUUIDViewSet):
    queryset = models.Model.objects.all()
    serializer_class = serializers.ModelSerializer
    filterset_class = filters.ModelFilter
    permission_classes = [AllowAny]


class BodyTypeViewSet(BaseUUIDViewSet):
    queryset = models.BodyType.objects.all()
    serializer_class = serializers.BodyTypeSerializer
    filterset_class = filters.BodyTypeFilter
    permission_classes = [AllowAny]


class ColourViewSet(BaseUUIDViewSet):
    queryset = models.Colour.objects.all()
    serializer_class = serializers.BodyColourSerializer
    filterset_class = filters.BodyColourFilter
    permission_classes = [AllowAny]


class VehicleViewSet(BaseUUIDViewSet):
    serializer_class = serializers.VehicleSerializer
    filterset_class = filters.VehicleFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('name', 'min_price',)

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

        return Response({"message": f"{instance.brand.name} updated successfully", "data": serializer.data})


    def get_queryset(self):
        queryset = models.Vehicle.objects.select_related("brand", "model", "body_type", "user",
                                                      "subscription").all()
        vehicle_type = self.request.query_params.get('vehicle_type')
        if vehicle_type in ['1', '2']:
            queryset = queryset.filter(vehicle_type=int(vehicle_type))
        return queryset

    @action(detail=True, methods=['get'])
    def related_vehicles(self, request, uuid=None):
        vehicle = self.get_object()
        related_vehicles = self.get_queryset().filter(user=vehicle.user).exclude(uuid=vehicle.uuid)
        if not related_vehicles.exists():
            return Response({"vehicle": "No related vehicles found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(related_vehicles, many=True)
        return Response(serializer.data)
    
    # @action(detail=True, methods=['post'])
    # def customer_enquiry(self, request, uuid=None):
    #     vehicle = self.get_object()
    #     data = request.data.copy()
    #     data['vehicle'] = vehicle.uuid
    #     serializer = serializers.VehicleCustomerEnquirySerializer(data=data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #
    #         # Send an email with the enquiry details
    #         subject = f"New Enquiry for Vehicle {vehicle.uuid}"
    #         message = (
    #             f"Name: {data['name']}\n"
    #             f"Email: {data['email']}\n"
    #             f"Phone Number: {data['phone_number']}\n"
    #             f"Subject: {data['subject']}\n"
    #             f"Message: {data['message']}\n"
    #             f"Vehicle ID: {vehicle.uuid}"
    #         )
    #         from_email = 'godartdelivery@gmail.com'
    #         recipient_list = ['thevampire0817@gmail.com']
    #         send_mail(subject, message, from_email, recipient_list)
    #
    #         return Response({'message': 'Enquiry received and email sent'})
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['post'], url_path='add-from-history')
    # def copy_vehicles(self, request):
    #     vehicle_uuids = request.data.get('vehicle_uuids', [])
    #
    #     if not vehicle_uuids:
    #         return Response({"error": "No vehicle UUIDs provided"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     new_vehicles = []
    #     for new_uuid in vehicle_uuids:
    #         try:
    #             vehicle = models.Vehicle.objects.get(uuid=new_uuid)
    #             vehicle.pk = None  # This will create a new instance
    #             vehicle.uuid = uuid.uuid4()
    #             vehicle.is_active = True  # Set default values for new instances
    #             vehicle.is_sold = False
    #             vehicle.save()
    #             new_vehicles.append(vehicle)
    #         except models.Vehicle.DoesNotExist:
    #             return Response({"error": f"Vehicle with UUID {new_uuid} does not exist"},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = self.get_serializer(new_vehicles, many=True)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['post'], url_path='add-from-history')
    def add_from_history(self, request):
        vehicle_uuids = request.data.get('vehicle_uuids', [])
        subscription_id = request.data.get('subscription_id')

        if not vehicle_uuids:
            return Response({"error": "No vehicle UUIDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not subscription_id:
            return Response({"error": "No Subscription ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscription = Subscription.objects.get(uuid=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription with provided ID does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        is_custom_package = False
        if subscription.custom_package:
            is_custom_package = True

        # Check remaining vehicles
        total_vehicles_allowed = subscription.package.number_of_vehicle if subscription.package \
            else subscription.custom_package.number_of_vehicle if subscription.custom_package \
            else 0
        vehicles_created = models.Vehicle.objects.filter(user=request.user, subscription__uuid=subscription_id, is_sold=False).count()
        remaining_vehicles = total_vehicles_allowed - vehicles_created
        
        if remaining_vehicles <= 0:
            return Response({"error": "No remaining vehicle slots in the package"}, status=status.HTTP_400_BAD_REQUEST)

        new_vehicles = []
        for vehicle_uuid in vehicle_uuids:
            if remaining_vehicles <= 0:
                break

            try:
                vehicle = models.Vehicle.objects.get(uuid=vehicle_uuid)
                vehicle.pk = None  # This will create a new instance
                vehicle.uuid = uuid.uuid4()
                vehicle.subscription = subscription
                vehicle.is_active = False  # Set default values for new instances
                vehicle.is_sold = False
                vehicle.comment = ""
                vehicle.status = 2
                vehicle.is_featured = False
                vehicle.save()
                new_vehicles.append(vehicle)
                remaining_vehicles -= 1
            except models.Vehicle.DoesNotExist:
                return Response({"error": f"Vehicle with UUID {vehicle_uuid} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_vehicles:
            return Response({"error": "No vehicles were copied due to package limits"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(new_vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser], url_path='activate-vehicle')
    def activate_vehicle(self, request):
        subscription_uuid = self.request.data.get("subscription_uuid", "")
        vehicle_uuid = self.request.data.get("vehicle_uuid", "")
        vehicle_status = self.request.data.get("status", 2)
        comment = self.request.data.get("comment")

        if vehicle_status == 0 and comment == "":
            return Response({
                "error": "Comment is missing for vehicle rejection."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not subscription_uuid and not vehicle_uuid:
            return Response({
                "error": "Subscription uuid and Vehicle uuid is missing."
            }, status=status.HTTP_400_BAD_REQUEST)
        if subscription_uuid and not vehicle_uuid:
            return Response({
                "error": "Vehicle uuid is missing."
            }, status=status.HTTP_400_BAD_REQUEST)
        if vehicle_uuid and not subscription_uuid:
            return Response({
                "error": "Subscription uuid is missing."
            }, status=status.HTTP_400_BAD_REQUEST)
        if vehicle_status == None:
            return Response({
                "error": "Vehicle status is missing."
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Subscription.objects.get(uuid=subscription_uuid)
            vehicle = models.Vehicle.objects.get(uuid=vehicle_uuid)
            message = ""
            if vehicle_status == 2:
                message = "Vehicle has been updated to pending."
            if vehicle_status == 0:
                message = "Vehicle has been rejected."
            if vehicle_status == 1:
                message = "Vehicle has been accepted."

            if subscription.is_paid:
                if vehicle_status == 1:
                    vehicle.is_active = True
                else:
                    vehicle.is_active = False
                vehicle.activation_date = timezone.now()
                vehicle.status = vehicle_status
                vehicle.comment = comment
                vehicle.save()
                vehicle = models.Vehicle.objects.get(uuid=vehicle_uuid)
                return Response({"message": message, "subscription_uuid": subscription_uuid, "vehicle_uuid": vehicle_uuid, 
                    "activation_date": vehicle.activation_date, "comment": vehicle.comment}, 
                    status=status.HTTP_200_OK)
            else:
                return Response({"error": "Payment for this subscription is pending."}, status=status.HTTP_402_PAYMENT_REQUIRED)    

        except Subscription.DoesNotExist as err:
            return Response({"error": "Subscription doesn't exists."}, status=status.HTTP_404_NOT_FOUND)
        except models.Vehicle.DoesNotExist as err:
            return Response({"error": "Vehicle doesn't exists."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='sold-vehicle')
    def vehicle_sold(self, request):
        vehicle_uuid = self.request.query_params.get("vehicle_id")
        try:
            vehicle = models.Vehicle.objects.get(uuid=vehicle_uuid)
            if vehicle.is_sold:
                return Response({"error": "Vehicle already marked as sold!"}, status=status.HTTP_400_BAD_REQUEST)
            vehicle.is_sold = True
            vehicle.save()
            return Response({"message": "Vehicle has been marked as sold."}, status=status.HTTP_200_OK)
        except models.Vehicle.DoesNotExist as err:
            return Response({"error": "Vehicle doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='vehicle-summary')
    def vehicle_summary(self, request):
        subscription_uuid = self.request.query_params.get("subscription")
        vehicles = models.Vehicle.objects.filter(subscription__uuid=subscription_uuid)
        if not subscription_uuid:
            vehicles = models.Vehicle.objects.all()
        vehicle_counts = vehicles.aggregate(
            total_vehicle=Count('id'),
            accepted_vehicle=Count(Case(When(status=1, then=1), output_field=IntegerField())),
            rejected_vehicle=Count(Case(When(status=0, then=1), output_field=IntegerField())),
            pending_vehicle=Count(Case(When(status=2, then=1), output_field=IntegerField()))
        )

        return Response({
            "total_vehicle": vehicle_counts['total_vehicle'],
            "accepted_vehicle": vehicle_counts['accepted_vehicle'],
            "rejected_vehicle": vehicle_counts['rejected_vehicle'],
            "pending_vehicle": vehicle_counts['pending_vehicle']
        })




class VehicleImageView(BaseUUIDViewSet):
    serializer_class = serializers.VehicleImageSerializer
    queryset = models.VehicleImage.objects.all()
    http_method_names = ["delete"]


class VehicleWishlistViewSet(BaseUUIDViewSet):
    queryset = models.VehicleWishlists.objects.select_related("vehicle", "user").all()
    serializer_class = serializers.VehicleWishlistSerializer
    http_method_names = ["delete", "post", "get"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
class VehicleTypeNumberViewSet(BaseUUIDViewSet):
    queryset = models.VehicleTypeNumber.objects.all()
    serializer_class = serializers.VehicleTypeNumberSerializer
    filterset_class = filters.VehicleTypeFilter
    http_method_names = ["delete", "post", "get","put"]
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        serializer.save()
        return serializer.data

    def get_queryset(self):
        queryset = super().get_queryset()
        vehicle_type_number = self.request.query_params.get('vehicle_type_number', None)
        if vehicle_type_number is not None:
            queryset = queryset.filter(vehicle_type_number=vehicle_type_number)

        registration_year = self.request.query_params.get('first_registration_year', None)
        if registration_year is not None:
            queryset = queryset.filter(first_registration_year=registration_year)
        return queryset


@api_view(['POST'])
def send_email_to_user(request):
    vehicle_id = request.data.get('vehicle_id')
    email = request.data.get('email')
    phone = request.data.get('phone')
    subject = request.data.get('subject')
    message = request.data.get('message')

    try:
        vehicle = models.Vehicle.objects.get(uuid=uuid.UUID(vehicle_id))
    except models.Vehicle.DoesNotExist:
        return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

    user_email = vehicle.user.email

    # Send email to the user
    send_mail(
        subject,
        message,
        'godartdelivery@gmail.com',
        [user_email],
        fail_silently=False,
    )

    return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)


class RatingViewSet(BaseUUIDViewSet):
    queryset = models.Rating.objects.select_related("vehicle", "user").all()
    serializer_class = serializers.RatingSerializer
    http_method_names = ["delete", "post", "get", "put"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get("vehicle"):
            queryset = self.queryset.filter(vehicle=self.request.query_params.get("vehicle"))
        return queryset
