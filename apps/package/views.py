import csv
from io import TextIOWrapper
import pandas as pd
from dj_rest_kit.views import BaseUUIDViewSet
from django.db import transaction
from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.package import models, serializers, filters
from apps.users import models as user_models
from apps.users.models import User
from django.utils import timezone
from rest_framework.exceptions import APIException
from django.db.models import Count, Case, When, IntegerField
from apps.vehicle.models import Vehicle


class PackageViewSet(BaseUUIDViewSet):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    filterset_class = filters.PackageFilter
    # permission_classes = [AllowAny]
    
    
class CustomPackageViewSet(BaseUUIDViewSet):
    queryset = models.CustomPackage.objects.all()
    serializer_class = serializers.CustomPackageSerializer
    filterset_class = filters.CustomPackageFilter
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser], url_path="manage-package")
    def manage_package(self, request):
        package_uuid = self.request.data.get("package", "")
        package_status = self.request.data.get("status", "")
        price = self.request.data.get("price", 0)
        change_date = timezone.now()

        try:
            package = models.CustomPackage.objects.get(uuid=package_uuid)
            package.status = package_status
            if package_status == 1:
                package.is_active = True
            else:
                package.is_active = False
            package.status_change_date = change_date
            package.price = price
            package.save()

            message = "Custom package has been accepted."
            if package_status == 0:
                message = "Custom package has been rejected."
            if package_status == 2:
                message = "Custom package has been updated to pending."
            package = models.CustomPackage.objects.get(uuid=package_uuid)
            return Response({
                "package_uuid": package.uuid,
                "message": message, "created_on": package.created_on, "status": package.status,
                "price": package.price, "status_change_date": package.status_change_date,
                "is_active": package.is_active
            }, status=status.HTTP_200_OK)

        except models.CustomPackage.DoesNotExist as err:
            return Response({"error": "Custom package not found."}, status=status.HTTP_404_NOT_FOUND)


class AdvertisementViewSet(BaseUUIDViewSet):
    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdvertisementSerializer
    filterset_class = filters.AdvertisementFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def import_data(self, request):
        subscription_id = request.data.get('subscription_id')
        user_id = request.data.get('user_id')

        if not subscription_id or not user_id:
            return Response({'error': 'Both subscription_id and user_id are required'}, status=400)

        try:
            subscription = models.Subscription.objects.get(uuid=subscription_id)
            user = User.objects.get(uuid=user_id)
        except models.Subscription.DoesNotExist:
            return Response({'error': 'Invalid subscription ID'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user_id'}, status=400)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'File is required'}, status=400)

        # Process the file
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                return Response({'error': 'Unsupported file format'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        advertisements = []
        for index, row in df.iterrows():
            advertisement = models.Advertisement(
                subscription=subscription,
                user=user,
                title=row.get('title'),
                link=row.get('link'),
                is_active=row.get('is_active', False) in ['1', 'true', 'True']
            )
            advertisements.append(advertisement)

        # Use bulk_create to insert all advertisements in a single query
        with transaction.atomic():
            models.Advertisement.objects.bulk_create(advertisements)

        return Response({'message': 'Data imported successfully'}, status=200)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def export_data(self, request):
        # Fetch advertisements based on package_id and user_id
        subscription_id = request.query_params.get('subscription_id')
        user_id = request.query_params.get('user_id')

        if not subscription_id or not user_id:
            return Response({'error': 'Both subscription_id and user_id are required'}, status=400)

        try:
            subscription = models.Subscription.objects.get(uuid=subscription_id)
        except models.Subscription.DoesNotExist:
            return Response({'error': 'Invalid subscription_id'}, status=400)

        advertisements = models.Advertisement.objects.filter(subscription__uuid=subscription_id, user__uuid=user_id)

        # Create a workbook and add advertisements data to it
        wb = Workbook()
        ws = wb.active
        ws.append(['title', 'link', 'is_active'])  # Add headers

        for ad in advertisements:
            ws.append([ad.title, ad.link, ad.is_active])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{subscription.response_message}_advertisement_data.xlsx"'
        wb.save(response)
        return response

class AdvertisementImageView(BaseUUIDViewSet):
    serializer_class = serializers.AdvertisementImageSerializer
    queryset = models.AdvertisementImage.objects.all()
    http_method_names = ["delete"]


class PublicAdvertisementList(BaseUUIDViewSet):
    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.PublicAdvertisementSerializer
    permission_classes = [AllowAny]
    filterset_class = filters.PublicAdvertisementFilter

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get(self, request):
        advertisements = self.get_queryset()
        serializer = self.get_serializer(advertisements, many=True)
        return Response(serializer.data)


class SubscriptionViewSet(BaseUUIDViewSet):
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    filterset_class = filters.SubscriptionFilter
    http_method_names = ["get", "post","delete"]

    def perform_create(self, serializer):
        data = self.request.data
        package_category = data.get("package_category")
        package = data.get("package")
        custom_package = data.get("custom_package")
        
        if package_category == 1:
            is_valid_package = models.Package.objects.filter(uuid=package).count()
            if not is_valid_package:
                raise APIException("Not a valid package")
                
        if package_category == 2:
            is_valid_package = models.CustomPackage.objects.filter(uuid=custom_package).count()
            if not is_valid_package:
                raise APIException("Not a valid custom package")

        serializer.save()
        return serializer.data

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser], url_path="activate-subscription")
    def activate_subscription(self, request):
        subscription_uuid = self.request.data.get("subscription_uuid", "")
        package_category = self.request.data.get("package_category", 1)
        if subscription_uuid:
            try:
                record = models.Subscription.objects.get(uuid=subscription_uuid)

                if record.is_activated:
                    return Response({
                        "message": "This subscription is already activated.","activation_date": record.activation_date
                    }, status=status.HTTP_200_OK)
                
                # Check subscription is paid or not. Only paid subscription will be activated.
                if not record.is_paid:
                    return Response({"error": "Payment for this subscription is pending."}, status=status.HTTP_402_PAYMENT_REQUIRED)
                # Get validity of package
                package_validity_days = record.package.validity if record.package_category == 1 else record.custom_package.validity
                record.is_activated = True
                record.activation_date = timezone.now()
                if package_validity_days > 0:
                    record.expiry_date = timezone.now().date() + timezone.timedelta(days=package_validity_days)
                record.save()

                record = models.Subscription.objects.get(uuid=subscription_uuid)

                return Response({
                    "message": "Subscription activated successfully.", 
                    "subscription_uuid": subscription_uuid,
                    "activation_date": record.activation_date
                    },status=status.HTTP_200_OK)
            except models.Subscription.DoesNotExist:
                return Response({"error": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Subscription uuid is missing."}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser], url_path="paid-subscription")
    def paid_subscription(self, request):
        """
        Get paid subscription list
        """
        queryset = self.get_queryset()
        queryset = queryset.filter(is_paid=True)
        try:
            data = self.serializer_class(queryset, many=True).data
            return Response(
                {
                    "record": data
                },
                status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response({
                "message": f"Something went wrong, {err}",
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated,], url_path="summary")
    def summary(self, request):
        subscription_id = self.request.query_params.get("subscription_id")
        vehicle_counts = Vehicle.objects.filter(subscription__uuid=subscription_id).aggregate(
            total_vehicle=Count('id'),
            active_vehicle=Count(Case(When(status=1, then=1), output_field=IntegerField())),
            under_review_vehicle=Count(Case(When(status=2, then=1), output_field=IntegerField())),
            rejected_vehicle=Count(Case(When(status=0, then=1), output_field=IntegerField())),
            sold_vehicle=Count(Case(When(is_sold=True, then=1), output_field=IntegerField()))
        )
        return Response({
            "total_vehicle": vehicle_counts["total_vehicle"],
            "active_vehicle": vehicle_counts["active_vehicle"],
            "under_review": vehicle_counts["under_review_vehicle"],
            "rejected_vehicle": vehicle_counts["rejected_vehicle"],
            "sold_vehicle": vehicle_counts["sold_vehicle"],
        }, status=status.HTTP_200_OK)


class PackageBookmarkViewSet(BaseUUIDViewSet):
    queryset = models.PackageBookMark.objects.all()
    serializer_class = serializers.PackageBookMarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
