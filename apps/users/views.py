import requests
from allauth.socialaccount.models import SocialApp
from dj_rest_kit.views import BaseAPIView, BaseUUIDViewSet, APIView
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.core.paginator import Paginator
import uuid
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count,Q
from django.core.cache import cache
from geopy.geocoders import Nominatim
from rest_framework.pagination import PageNumberPagination
from geopy.distance import geodesic
from rest_framework.decorators import action
from django.db.models import Count, Case, When, IntegerField, F
# import 
from apps.users import models, filters
from apps.users import serializers
from apps.users.services import send_email_verification_otp
from base.globals import UserConstants,UserReviewConstants
from apps.vehicle import models as vehicle_models
from apps.package.models import Subscription


class UserRegistrationView(BaseAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        serializer = serializers.UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate OTP and Send Email
        user_verification_code, _ = user.get_or_create_verification_code()
        user_verification_code.save()
        send_email_verification_otp(self, user)

        refresh = RefreshToken.for_user(user)
        response = {
            "uuid": user.uuid,
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "is_email_verify": user.is_email_verify,
        }
        response.update(**serializer.data)
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(BaseAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user and not user.is_active:
            raise ValidationError({"is_active": "Your account is not active"})

        if not models.User.objects.filter(email=email).exists():
            raise ValidationError({"email": "Invalid Email"})

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            }

            response.update(**serializers.UserRegistrationSerializer(user).data)
            return Response(response)
        else:
            raise ValidationError({"password": "Invalid Password"})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def google_register(request):
    access_token = request.data.get("access_token")
    user_type = request.data.get("user_type", None)

    if not access_token:
        raise ValidationError({"access_token": "Access token not provided."})

    if not user_type:
        raise ValidationError({"user_type": "User type not provided."})

    # Get the Google SocialApp associated with your project
    try:
        SocialApp.objects.get(provider="google")
    except SocialApp.DoesNotExist:
        raise ValidationError({"access_token": "Access token not provided."})

    # Fetch user info from Google using the access token
    google_response = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
    )
    if google_response.status_code == 200:
        user_info = google_response.json()
        email = user_info.get("email")
        if not email:
            raise ValidationError({"email": "Email not found in Google response."})

        # Check if the user already exists in the database
        try:
            user = models.User.objects.get(email=email)
            raise ValidationError(
                {"google": "Google account is already registered."}
            )
        except models.User.DoesNotExist:
            # If the user doesn't exist, create a new user
            user, created = models.User.objects.get_or_create(
                email=email,
                is_google_verify=True,
                is_email_verify=True,
                user_type=user_type,
            )
            user.save()

        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        response = {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }
        response.update(**serializers.UserRegistrationSerializer(user).data)
        return Response(response)
    else:
        raise ValidationError({"error": "Failed to fetch user info from Google."})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def google_login(request):
    access_token = request.data.get("access_token")

    if not access_token:
        raise ValidationError({"access_token": "Access token not provided."})

    # Get the Google SocialApp associated with your project
    try:
        SocialApp.objects.get(provider="google")
    except SocialApp.DoesNotExist:
        raise ValidationError({"access_token": "Access token not provided."})

    # Fetch user info from Google using the access token
    google_response = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
    )
    if google_response.status_code == 200:
        user_info = google_response.json()
        email = user_info.get("email")
        if not email:
            raise ValidationError({"email": "Email not found in Google response."})

        # Check if the user exists in the database
        user = models.User.objects.filter(email=email).first()

        if user:
            # If the user exists, generate JWT token and return response
            refresh = RefreshToken.for_user(user)
            response = {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            }
            response.update(**serializers.UserRegistrationSerializer(user).data)
            return Response(response)
        else:
            raise ValidationError({"google": "User not registered with Google."})
    else:
        raise ValidationError({"error": "Failed to fetch user info from Google."})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def facebook_register(request):
    access_token = request.data.get("access_token")
    user_type = request.data.get("user_type", None)

    if not access_token:
        raise ValidationError({"access_token": "Access token not provided."})

    if not user_type:
        raise ValidationError({"user_type": "User type not provided."})

    # Get the Facebook SocialApp associated with your project
    try:
        SocialApp.objects.get(provider="facebook")
    except SocialApp.DoesNotExist:
        raise ValidationError({"access_token": "Access token not provided."})

    # Fetch user info from Facebook using the access token
    facebook_response = requests.get(
        f"https://graph.facebook.com/me?fields=id,birthday,first_name,last_name,about&access_token={access_token}"
    )

    if facebook_response.status_code == 200:
        user_info = facebook_response.json()
        facebook_id = user_info.get("id")
        first_name = user_info.get("first_name", "")
        last_name = user_info.get("last_name", "")
        dob = user_info.get("birthday")
        biography = user_info.get("about")

        # Check if the user already exists in the database
        try:
            user = models.User.objects.get(facebook_id=facebook_id)
            raise ValidationError(
                {"facebook": "Facebook account is already registered."}
            )
        except models.User.DoesNotExist:
            # If the user doesn't exist, create a new user
            user, created = models.User.objects.get_or_create(
                facebook_id=facebook_id,
                is_facebook_verify=True,
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                biography=biography,
            )
            user.save()

        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        response = {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }
        response.update(**serializers.UserRegistrationSerializer(user).data)
        return Response(response)
    else:
        raise ValidationError({"error": "Failed to fetch user info from Facebook."})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def facebook_login(request):
    access_token = request.data.get("access_token")

    if not access_token:
        raise ValidationError({"access_token": "Access token not provided."})

    # Get the Facebook SocialApp associated with your project
    try:
        SocialApp.objects.get(provider="facebook")
    except SocialApp.DoesNotExist:
        raise ValidationError({"access_token": "Access token not provided."})

    # Fetch user info from Facebook using the access token
    facebook_response = requests.get(
        f"https://graph.facebook.com/me?fields=id&access_token={access_token}"
    )

    if facebook_response.status_code == 200:
        user_info = facebook_response.json()
        facebook_id = user_info.get("id")

        # Check if the user exists in the database
        user = models.User.objects.filter(facebook_id=facebook_id).first()

        if user:
            # If the user exists, generate JWT token and return response
            refresh = RefreshToken.for_user(user)
            response = {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            }
            response.update(**serializers.UserRegistrationSerializer(user).data)
            return Response(response)
        else:
            raise ValidationError({"facebook": "User not registered with Facebook."})
    else:
        raise ValidationError({"error": "Failed to fetch user info from Facebook."})


class ChangePasswordView(BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            if not user.check_password(old_password):
                return Response(
                    {"message": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            request.session.flush()

            return Response(
                {"message": "Password reset successfully."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(BaseAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationAPIView(BaseAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        try:
            user = models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"email": "Invalid Email."}, status=status.HTTP_404_NOT_FOUND)

        models.VerificationCode.objects.filter(user=user).delete()
        send_email_verification_otp(self, user)

        response_data = {"message": "Email OTP sent successfully."}
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        code = request.data.get("code")

        user = models.User.objects.get(email=email)
        user_code = models.VerificationCode.objects.filter(user=user).first()

        if not user_code or code != user_code.code:
            raise ValidationError({"code": "Invalid Code"})

        user.is_email_verify = True
        user.save()
        user_code.delete()

        return Response({"message": "Email verification is successfully completed"}, status=status.HTTP_200_OK)


class ForgetPasswordAPI(BaseAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError({"password": "Passwords do not match"})

        try:
            user = models.User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            raise ValidationError({"email": "User not found"})

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = models.User.objects.get(email=email)
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.uuid))
                reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
                subject = 'Password Reset Request'
                context = {
                    'user': user,
                    'reset_link': reset_link,
                }
                email_html_message = render_to_string('emails/forgot_password.html', context)
                email = EmailMultiAlternatives(
                    subject = subject,
                    body = '',  # Plain text message
                    from_email = settings.EMAIL_HOST_USER,
                    to=[email],
                )
                email.attach_alternative(email_html_message, "text/html")
                email.send()
                # send_mail(
                #     'Password Reset Request',
                #     message,
                #     settings.DEFAULT_FROM_EMAIL,
                #     [user.email],
                #     fail_silently=False,
                # )
                return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = models.User.objects.get(uuid=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
                return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(BaseUUIDViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = filters.UserFilter
    http_method_names = ["get", "patch"]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated,], url_path="summary")
    def summary(self, request):
        user_id = self.request.query_params.get("user_id")
        
        total_vehicle = vehicle_models.Vehicle.objects.filter(user_id__uuid=user_id).count()
        package_counts = Subscription.objects.filter(user_id__uuid=user_id).aggregate(
            total_package=Count('id'),
            active_package=Count(Case(When(is_activated=True, then=1), output_field=IntegerField())),
            expired_package=Count(Case(When(is_expired=True, then=1), output_field=IntegerField())),
            paid_package=Count(Case(When(is_paid=True, then=1), output_field=IntegerField())),
            unpaid_package=Count(Case(When(is_paid=False, then=1), output_field=IntegerField()))
        )
        return Response({
            "total_package": package_counts["total_package"] if package_counts["total_package"] else 0,
            "active_package": package_counts["active_package"] if package_counts["active_package"] else 0,
            "expired_package": package_counts["expired_package"] if package_counts["expired_package"] else 0,
            "paid_package": package_counts["paid_package"] if package_counts["paid_package"] else 0,
            "unpaid_package": package_counts["unpaid_package"] if package_counts["unpaid_package"] else 0, 
            "favorites": 0,
            "total_vehicle": total_vehicle
        }, status=status.HTTP_200_OK)


class DealerPublicProfileView(APIView):
    def get(self, request, uuid):
        # Get the user by UUID or return 404 if not found
        user = get_object_or_404(models.User, uuid=uuid)
        
        # Check if the user is a dealer
        if user.user_type != UserConstants.DEALER:
            return Response({"error": "User is not a dealer"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate average rating and total reviews
        reviews = models.UserReview.objects.filter(dealer_id=user)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        total_reviews = reviews.count()
        
        # Prepare the dealer profile data
        dealer_profile = {
            "uuid": user.uuid,
            "dealership_name": user.dealership_name,
            "city": user.city.name if user.city else None,
            "country": user.country.name if user.country else None,
            "biography": user.biography,
            "rating": round(avg_rating, 1) if avg_rating else None,
            "total_review": total_reviews,
            "email": user.email,
            "whatsapp_number": user.whatsapp_number,
            "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
            "cover_image": request.build_absolute_uri(user.cover_image.url) if user.cover_image else None,
        }
        
        # Serialize the data
        serializer = serializers.DealerPublicProfileSerializer(dealer_profile)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_type = request.data.get('product_type')
        product_id = request.data.get('product_id')
        rating = request.data.get('rating')
        review_text = request.data.get('review_text', '')

        if not all([product_type, product_id, rating]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_type = int(product_type)
            if product_type not in dict(UserReviewConstants.get_review_category_choices()):
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid product type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = float(rating)
            if not (0 <= rating <= 5):
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid rating value"}, status=status.HTTP_400_BAD_REQUEST)

        # Determine the model based on the product type
        if product_type ==1:
            model = vehicle_models.Vehicle
        # elif product_type ==2:
        #     model = models.CarRental
        # elif product_type ==3:
        #     model = models.Bike        
        # elif product_type ==4:
        #     model = models.BikeRental        
        # elif product_type ==5:
        #     model = models.GarageRental       
        # elif product_type ==6:
        #     model = models.ComponentSell       
 
        else:
            return Response({"error": "Invalid product type for rating"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(model, uuid=product_id)

        # Check if the user has already reviewed this product
        existing_review = models.UserReview.objects.filter(
            dealer_id=product.user,
            client_id=request.user,
            product_type=product_type
        ).first()

        if existing_review:
            return Response({"error": "You have already reviewed this product"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the review
        review = models.UserReview.objects.create(
            dealer_id=product.user,
            client_id=request.user,
            product_type=product_type,
            product_id=product_id,
            rating=rating,
            review_text=review_text
        )

        serializer = serializers.UserReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DealerPagination(PageNumberPagination):
    page_size = 10  # Number of dealers per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class SearchDealerView(APIView):
    def get(self, request):
        # Get query parameters
        dealership_name =  request.query_params.get('dealership_name', '')
        city =  request.query_params.get('city', '')
        postal_code =  request.query_params.get('postal_code', '')
        radius =  request.query_params.get('radius')
        longitude =  request.query_params.get('longitude')
        latitude =  request.query_params.get('latitude')

        # Start with all dealer users
        dealers = models.User.objects.filter(user_type=UserConstants.DEALER)

        # Apply filters based on provided parameters
        if dealership_name:
            dealers = dealers.filter(dealership_name__icontains=dealership_name)
            # if not dealers.exists():
            #     return Response({"message": "No dealers found with the given name"}, status=status.HTTP_404_NOT_FOUND)
    
        if city:
            dealers = dealers.filter(city__name__icontains=city)
        if postal_code:
            dealers = dealers.filter(postal_code__icontains=postal_code)
        dealers_within_radius = []
        radius_search_performed = False

        # Geolocation-based search
        if all([radius, longitude, latitude]):
            try:
                radius = float(radius)
                user_location = (float(latitude), float(longitude))
                
                geolocator = Nominatim(user_agent="my_agent")
                
                
                for dealer in dealers:
                    if dealer.postal_code:
                        dealer_coords = self.get_coordinates(dealer.postal_code, geolocator)
                        if dealer_coords:
                            distance = geodesic(user_location, dealer_coords).km
                            print(distance)
                            if distance <= radius*1000:
                                dealers_within_radius.append((dealer, distance/1000))

                dealers_within_radius.sort(key=lambda x: x[1])
                dealers = [dealer for dealer, _ in dealers_within_radius]
                radius_search_performed = True
                print(dealers)
                
            except ValueError:
                return Response({"error": "Invalid geolocation parameters"}, status=status.HTTP_400_BAD_REQUEST)
        if not dealers:
            return Response({"message": "No dealer found"}, status=status.HTTP_404_NOT_FOUND)


        dealer_profiles = []

        if radius_search_performed and dealers_within_radius:
            for dealer, distance in dealers_within_radius:
                reviews = models.UserReview.objects.filter(dealer_id=dealer)
                avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
                total_reviews = reviews.count()

                profile = {
                    "uuid": dealer.uuid,
                    "dealership_name": dealer.dealership_name,
                    "city": dealer.city.name if dealer.city else None,
                    "country": dealer.country.name if dealer.country else None,
                    "biography": dealer.biography,
                    "postal_code": dealer.postal_code,
                    "rating": round(avg_rating, 1) if avg_rating else None,
                    "total_review": total_reviews,
                    "email": dealer.email,
                    "whatsapp_number": dealer.whatsapp_number,
                    "profile_picture": request.build_absolute_uri(dealer.profile_picture.url) if dealer.profile_picture else None,
                    "cover_image": request.build_absolute_uri(dealer.cover_image.url) if dealer.cover_image else None,
                    "distance": round(distance, 2),
                }
                dealer_profiles.append(profile)
        else:
            for dealer in dealers:
                reviews = models.UserReview.objects.filter(dealer_id=dealer)
                avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
                total_reviews = reviews.count()

                profile = {
                    "uuid": dealer.uuid,
                    "dealership_name": dealer.dealership_name,
                    "city": dealer.city.name if dealer.city else None,
                    "country": dealer.country.name if dealer.country else None,
                    "biography": dealer.biography,
                    "postal_code": dealer.postal_code,
                    "rating": round(avg_rating, 1) if avg_rating else None,
                    "total_review": total_reviews,
                    "email": dealer.email,
                    "whatsapp_number": dealer.whatsapp_number,
                    "profile_picture": request.build_absolute_uri(dealer.profile_picture.url) if dealer.profile_picture else None,
                    "cover_image": request.build_absolute_uri(dealer.cover_image.url) if dealer.cover_image else None,
                    "distance": 0,
                }
                dealer_profiles.append(profile)

        paginator = DealerPagination()
        paginated_dealers = paginator.paginate_queryset(dealer_profiles, request)
        
        # Serialize the data
        serializer = serializers.DealerPublicProfileSerializer(paginated_dealers, many=True)
        
        return paginator.get_paginated_response(serializer.data)

    def get_coordinates(self, postal_code, geolocator):
        # Try to get the coordinates from cache
        cache_key = f'geocode_{postal_code}'
        coords = cache.get(cache_key)
        
        if coords is None:
            try:

                location = geolocator.geocode(postal_code)
                if location:
                    coords = (location.latitude, location.longitude)

                    cache.set(cache_key, coords, 30 * 24 * 60 * 60)
                else:

                    cache.set(cache_key, None, 24 * 60 * 60) 
            except Exception as e:
                print(f"Error geocoding postal code {postal_code}: {str(e)}")
                return None
        
        return coords


@api_view(['POST'])
def send_direct_email_to_dealer(request):
    dealer_id = request.data.get('dealer_id')
    email = request.data.get('email')
    phone = request.data.get('phone')
    subject = request.data.get('subject')
    message = request.data.get('message')

    try:
        dealer = models.User.objects.get(uuid=uuid.UUID(dealer_id))
    except models.User.DoesNotExist:
        return Response({"error": "Dealer not found"}, status=status.HTTP_404_NOT_FOUND)

    user_email = dealer.email

    # Send email to the user
    send_mail(
        subject,
        message,
        'godartdelivery@gmail.com',
        [user_email],
        fail_silently=False,
    )

    return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
class UserSummaryView(APIView):
    def get(self, request):
        total_users = models.User.objects.count()
        private_users = models.User.objects.filter(user_type=UserConstants.PRIVATE).count()
        dealers = models.User.objects.filter(user_type=UserConstants.DEALER).count()
        suspended_users = models.User.objects.filter(is_suspended=True).count()

        summary_data = {
            "total_users": private_users + dealers,
            "private_users": private_users,
            "dealer_users": dealers,
            "suspended_users": suspended_users
        }

        return Response(summary_data, status=status.HTTP_200_OK)


class UserListView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', '')
        sort_by = request.query_params.get('sort', '-date_joined')  
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))

        users = models.User.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(country__name__icontains=search_query)
        ).order_by(sort_by)

        paginator = Paginator(users, per_page)
        page_obj = paginator.get_page(page)

        serializer = serializers.UserRegistrationSerializer(page_obj, many=True, fields=[
            'uuid', 'first_name', 'last_name', 'date_joined', 'country', 'user_type', 'is_suspended'
        ])

        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next() and page + 1 or None,
            'previous': page_obj.has_previous() and page - 1 or None,
            'page': page,
            'per_page': per_page,
            'total_pages': paginator.num_pages
        }, status=status.HTTP_200_OK)