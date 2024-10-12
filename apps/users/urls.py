from django.urls import include, path
from rest_framework import routers

from apps.users import views

router = routers.DefaultRouter(trailing_slash=False)
router.register("user-profile", views.UserProfileViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("register-via-email", views.UserRegistrationView.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("change-password", views.ChangePasswordView.as_view()),
    path('forget-password', views.ForgetPasswordAPI.as_view(), name='forget-password'),
    path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset_password'),
    path('email-otp', views.EmailVerificationAPIView.as_view(), name='verify-otp'),
    # social login
    path("register-via-google", views.google_register),
    path("login-via-google", views.google_login),
    path("register-via-facebook", views.facebook_register),
    path("login-via-facebook", views.facebook_login),
    # dealer profile
    path('dealer-profile/<uuid:uuid>', views.DealerPublicProfileView.as_view(), name='dealer-public-profile'),
    # add rating
    path('add-rating', views.AddRatingView.as_view(), name='add-rating'),
    # search dealers
    path('search-dealers/', views.SearchDealerView.as_view(), name='search-dealers'),
    path('email-dealer/', views.send_direct_email_to_dealer, name='send_email_to_dealer'),
    path('users-summary/', views.UserSummaryView.as_view(), name='user-summary'),
    path('users-list/', views.UserListView.as_view(), name='user-list'),
]
