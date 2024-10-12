from django.urls import path
from .views import DashboardSummaryView

urlpatterns = [
    # ... other URL patterns ...
    path('admin-dashboard-summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]