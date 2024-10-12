from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta

from apps.users.models import User
from apps.package.models import Subscription
from apps.transactions.models import Transactions

class DashboardSummaryView(APIView):
    def get(self, request):
        now = timezone.now()
        past_month = now - timedelta(days=30)
        past_week = now - timedelta(days=7)

        # Total Users
        total_users = User.objects.count()
        users_last_month = User.objects.filter(date_joined__gte=past_month).count()
        user_growth = (users_last_month / total_users) * 100 if total_users > 0 else 0

        # Total Subscription Orders
        total_packages = Subscription.objects.count()
        packages_last_week = Subscription.objects.filter(created_at__gte=past_week).count()
        package_growth = (packages_last_week / total_packages) * 100 if total_packages > 0 else 0

        # Total Sales
        # total_sales = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0
        # sales_last_week = Transaction.objects.filter(created_at__gte=past_week).aggregate(total=Sum('amount'))['total'] or 0
        # sales_growth = ((total_sales - sales_last_week) / total_sales) * 100 if total_sales > 0 else 0

        # Pending Packages
        pending_packages = Subscription.objects.filter(is_activated=False,is_paid=True).count()
        pending_last_week = Subscription.objects.filter(is_activated=False,is_paid=True, created_at__gte=past_week).count()
        pending_growth = ((pending_packages - pending_last_week) / pending_packages) * 100 if pending_packages > 0 else 0

        data = {
            'total_users': {
                'value': total_users,
                'growth': round(user_growth, 1),
                'period': 'month'
            },
            'total_package_orders': {
                'value': total_packages,
                'growth': round(package_growth, 1),
                'period': 'week'
            },
            # 'total_sales': {
            #     'value': int(total_sales),
            #     'growth': round(sales_growth, 1),
            #     'period': 'week'
            # },
            'pending_packages': {
                'value': pending_packages,
                'growth': round(pending_growth, 1),
                'period': 'week'
            }
        }

        return Response(data, status=status.HTTP_200_OK)