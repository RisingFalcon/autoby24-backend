from django.conf import settings
from django.core.mail import send_mail


def send_email_verification_otp(self, user):
    user_code_email, _ = user.get_or_create_verification_code()
    subject = "OTP for Email Verification"
    message = f"Your email verification OTP is: {user_code_email.code}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
