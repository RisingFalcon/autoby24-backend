from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from apps.vehicle.models import Vehicle
from apps.package.models import Package
from .serializers import (
    PurchaseNotificationSerializer, 
    SellpostApprovedNotificationSerializer,
    PaymentSuccessfullNotificationSerializer,
)
# Create your views here.


class PurchaseNotification(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = PurchaseNotificationSerializer(data=request.data)
        if serializer.is_valid():
            package_name = serializer.validated_data['package_name']
            order_number = serializer.validated_data['order_number']
            total_amount = serializer.validated_data['total_amount']
            purchase_date = serializer.validated_data['date']
            subject = 'Purchase Notification'
            
            user = request.user
            recipient = user.email

            context = {
                'package_name': package_name,
                'order_number': order_number,
                'total_amount': total_amount,
                'purchase_date': purchase_date,
                'user': user,
                }
            email_html_message = render_to_string('emails/purchase_notification.html', context)
            
            # Create the email object
            email = EmailMultiAlternatives(
                subject = subject,
                body = '',  # Plain text message
                from_email = settings.EMAIL_HOST_USER,
                to=[recipient],
            )
            # Attach the HTML message
            email.attach_alternative(email_html_message, "text/html")
            # Send the email
            email.send()
            return Response({'status': 'Email sent for purchase notification'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WelcomeNotification(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # serializer = PurchaseNotificationSerializer(data=request.data)
        subject = 'Welcome to autoby24!'
            
        user = request.user
        recipient = user.email

        context = {
            'user': user,
            }
        email_html_message = render_to_string('emails/welcome_notification.html', context)
            
        # Create the email object
        email = EmailMultiAlternatives(
            subject = subject,
            body = '',  # Plain text message
            from_email = settings.EMAIL_HOST_USER,
            to=[recipient],
            )
            # Attach the HTML message
        email.attach_alternative(email_html_message, "text/html")
        # Send the email
        email.send()
        return Response({'status': 'Email sent for welcome notification'}, status=status.HTTP_200_OK)
    # return Response('', status=status.HTTP_400_BAD_REQUEST)

class PasswordUpdateNotification(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # serializer = PurchaseNotificationSerializer(data=request.data)
        subject = 'Your autoby24 Password Has Been Changed'
            
        user = request.user
        recipient = user.email

        context = {
            'user': user,
            }
        email_html_message = render_to_string('emails/password_update_notification.html', context)
            
        # Create the email object
        email = EmailMultiAlternatives(
            subject = subject,
            body = '',  # Plain text message
            from_email = settings.EMAIL_HOST_USER,
            to=[recipient],
            )
            # Attach the HTML message
        email.attach_alternative(email_html_message, "text/html")
        # Send the email
        email.send()
        return Response({'status': 'Email sent for password update notification'}, status=status.HTTP_200_OK)
    # return Response('', status=status.HTTP_400_BAD_REQUEST)

class SellpostApprovedNotification(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = SellpostApprovedNotificationSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data['post_id']
            try:
                vehicle = Vehicle.objects.get(uuid=post_id)
            except Vehicle.DoesNotExist:
                return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
            subject = 'Your Vehicle Post Has Been Approved!'
            
            user = request.user
            recipient = user.email

            context = {
                'user': user,
                'vehicle': vehicle
                }
            email_html_message = render_to_string('emails/sellpost_approved_notification.html', context)
            
            # Create the email object
            email = EmailMultiAlternatives(
                subject = subject,
                body = '',  # Plain text message
                from_email = settings.EMAIL_HOST_USER,
                to=[recipient],
                )
            # Attach the HTML message
            email.attach_alternative(email_html_message, "text/html")
            # Send the email
            email.send()
            return Response({'status': 'Email sent for sell post approved notification'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentSuccessfullNotification(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = PaymentSuccessfullNotificationSerializer(data=request.data)
        if serializer.is_valid():
            package_id = serializer.validated_data['package_id']
            try:
                package = Package.objects.get(uuid=package_id)
            except Package.DoesNotExist:
                return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
            subject = 'Payment Successful - Your Package Details'
            
            user = request.user
            recipient = user.email

            context = {
                'user': user,
                'package': package
                }
            email_html_message = render_to_string('emails/payment_successfull.html', context)
            
            # Create the email object
            email = EmailMultiAlternatives(
                subject = subject,
                body = '',  # Plain text message
                from_email = settings.EMAIL_HOST_USER,
                to=[recipient],
                )
            # Attach the HTML message
            email.attach_alternative(email_html_message, "text/html")
            # Send the email
            email.send()
            return Response({'status': 'Email sent for payment successfull'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


