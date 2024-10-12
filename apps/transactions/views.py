from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import action
from django.db.models import Sum, Case, When, DecimalField, F
from .models import (
    Transactions, 
    Donation,
    Payment
)
from dj_rest_kit.views import BaseUUIDViewSet
from .utils import (
    get_transaction_details,
    create_payment_url,
    update_payment_record,
)
from apps.package.models import Subscription
from .serializers import (
    PaymentSerializer,
    TransactionSerializer,
    DonationSerializer,TransactionListSerializer
)
from .filters import TransactionFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users.models import User
from apps.package.permissions import IsAdminUser
from django.utils import timezone
import os
from django.core.paginator import Paginator

class TransactionsViewset(BaseUUIDViewSet):
    queryset = Transactions.objects.all().order_by("-creation_date")
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]
    filterset_class = TransactionFilter

    @action(detail=False, methods=['post'], url_path='payment-url')
    def payment_url(self, request):
        request_data = request.data
        subscription_id = request_data.get("subscription_id", "")
        # user_id = request_data.get("user_id", "")
        user_id = self.request.user.uuid
        donations = request_data.get("donation", 0)
        if subscription_id:
            try:
                subscription = Subscription.objects.get(uuid=subscription_id)
                if subscription.is_paid and not subscription.is_expired:
                    return Response({"message": f"Subscription with ID: {subscription_id} is already paid."}, status=status.HTTP_200_OK)
                
                package_price = float(subscription.package.price) if subscription.package_category == 1 else float(subscription.custom_package.price)
                amount_to_paid = package_price + donations
                payload = {
                    "name": subscription.package.name if subscription.package_category == 1 else subscription.custom_package.name,
                    "unique_id": subscription_id,
                    "quantity": 1,
                    "amount": amount_to_paid,
                    "currency": os.getenv("CURRENCY"),
                    "donation": donations,
                    "user_id": user_id,
                    # "success_url": request.build_absolute_uri('payment-success'),
                    "success_url": "https://dev.autoby24.ch/payment-success",
                    "cancel_url": request.build_absolute_uri('payment-cancel')
                }
                transaction_id, payment_page_url, error = create_payment_url(payload)

                # Error in payment page url generation
                if error:
                    return Response({"message": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Success payment page url generation
                transaction = Transactions.objects.create(
                    subscription=subscription,
                    user=request.user,
                    transaction_id=transaction_id
                )
                if transaction:
                    return Response({
                        "payment_page_url": payment_page_url,
                        "transaction_id": transaction_id,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        "message": "Something went wrong, please try again."
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Subscription.DoesNotExist as err:
                return Response({"message": "Invalid subscription ID"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as err:
                return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "subscription Id is missing"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='payment-success', permission_classes=[], authentication_classes=[])
    def payment_success(self, request):
        return Response({
            "message": "Transaction has been completed successfully."
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='payment-cancel', permission_classes=[], authentication_classes=[])
    def payment_cancel(self, request):
        return Response({
            "message": "Transaction has been canceled."
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='check-payment-status', permission_classes=[], authentication_classes=[])
    def check_payment_status(self, request):
        transaction_id = request.query_params.get("transaction_id")
        if transaction_id:
            try:
                is_payment_succeed = False
                message = "Payment for this subscription has been failed."
                transactions = Transactions.objects.get(transaction_id=transaction_id)
                subscription = transactions.subscription
                post_finance_details = get_transaction_details(transaction_id)
                subscription = Subscription.objects.get(pk=subscription.id)

                transaction_details = {
                    'transaction_id': post_finance_details.id,
                    'state': str(post_finance_details.state),
                    'amount': post_finance_details.authorization_amount,
                    'currency': post_finance_details.currency,
                    'created_on': post_finance_details.created_on.isoformat(),
                }

                if subscription.is_paid and not subscription.is_expired:
                    return Response({"message": f"Transaction for subscription: {subscription.uuid} has been completed.", 
                            "transaction": transaction_details}, 
                        status=status.HTTP_200_OK)
                
                # Handle payment status
                update_payment_record(transactions, post_finance_details)

                if str(post_finance_details.state) == "TransactionState.FULFILL":
                    is_payment_succeed = True
                    message = "Payment for this subscription has been completed."
                    # Mark subscription as paid
                    subscription.is_paid = True
                    subscription.is_activated = True
                    package_validity_days = subscription.package.validity if subscription.package_category == 1 else subscription.custom_package.validity
                    if package_validity_days > 0:
                        subscription.expiry_date = timezone.now().date() + timezone.timedelta(days=package_validity_days)
                    subscription.save()

                    # Mark transaction as paid
                    transactions.status = "paid"
                    transactions.save()
                else:
                    # Mark subscription paid as False
                    subscription.is_paid = False
                    subscription.save()

                    # Mark transaction status as failed
                    if str(post_finance_details.state) == "TransactionState.FAILED":
                        transactions.status = "failed"
                        transactions.save()

                if is_payment_succeed:
                    return Response({
                        "message": message,
                        "transaction": transaction_details
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": message
                    }, status=status.HTTP_402_PAYMENT_REQUIRED)

            except Transactions.DoesNotExist as err:
                return Response({"error": "Invalid transaction ID"})
            except Exception as err:
                return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Transaction ID is missing"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='transaction-details')
    def transaction_details(self, request):
        transaction_id = request.query_params.get("transaction_id", "")
        if not transaction_id:
            return JsonResponse({'error': f"Transaction ID is missing."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            transactions = Transactions.objects.get(transaction_id=transaction_id)
            transaction_id = transactions.transaction_id
            transaction = get_transaction_details(transaction_id)
            if transaction:
                return JsonResponse({
                    'transaction_id': transaction.id,
                    'state': str(transaction.state),
                    'amount': transaction.authorization_amount,
                    'currency': transaction.currency,
                    'created_on': transaction.created_on.isoformat(),
                })
            else:
                return JsonResponse({'error': f"Transaction not found {transaction_id}"}, status=status.HTTP_404_NOT_FOUND)
        except Transactions.DoesNotExist as err:
            return JsonResponse({'error': f"Transaction not found for transaction ID: {transaction_id}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["get"], url_path="user-summary")
    def user_summary(self, request):
        user_id = self.request.query_params.get("user_id")
        if not user_id:
            user_id = self.request.user.uuid

        payment_aggregates = Payment.objects.filter(transaction__user_id__uuid=user_id).aggregate(
            total_spent=Sum(
                Case(
                    When(transaction__status="completed", then=F('amount')),
                    output_field=DecimalField()
                )
            ),
            total_pending=Sum(
                Case(
                    When(transaction__status="pending", then=F('amount')),
                    output_field=DecimalField()
                )
            )
        )

        total_spent = payment_aggregates['total_spent'] if payment_aggregates['total_spent'] else 0
        total_pending = payment_aggregates['total_pending'] if payment_aggregates['total_pending'] else 0
        return Response({
            "total_spent_amount": total_spent,
            "total_pending_amount": total_pending
        }, status=status.HTTP_200_OK)


class DonationViewset(BaseUUIDViewSet):

    @action(detail=False, methods=['post'], url_path='payment-url')
    def payment_url(self, request):
        data = request.data
        user_id = data.get("user_id", "")
        amount = data.get("amount", 0)
        if user_id:
            try:
                user = User.objects.get(uuid=user_id)
                
                payload = {
                    "name": f"Donation given by {user.name}",
                    "unique_id": user_id,
                    "quantity": 1,
                    "amount": float(amount),
                    "currency": os.getenv("CURRENCY"),
                    "success_url": request.build_absolute_uri('donation-success'),
                    "cancel_url": request.build_absolute_uri('donation-cancel')
                }
                transaction_id, payment_page_url, error = create_payment_url(payload)

                # Handle donation
                Donation.objects.create(
                    transaction_id = transaction_id,
                    currency = os.getenv("CURRENCY"),
                    status = "Pending",
                    amount = amount
                )

                # Error in payment page url generation
                if error:
                    return Response({"message": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({
                        "payment_page_url": payment_page_url,
                        "transaction_id": transaction_id
                    }, status=status.HTTP_201_CREATED)
                
            except User.DoesNotExist as err:
                return Response({"message": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User Id is missing"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='donation-success', permission_classes=[], authentication_classes=[])
    def donation_success(self, request):
        return Response({
            "message": "Transaction has been completed successfully."
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='donation-cancel', permission_classes=[], authentication_classes=[])
    def donation_cancel(self, request):
        return Response({
            "message": "Transaction has been canceled."
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='check-donation-status', permission_classes=[], authentication_classes=[])
    def check_donation_status(self, request):
        transaction_id = request.query_params.get("transaction_id", "")
        if not transaction_id:
            return JsonResponse({'error': "Transaction ID is missing."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Get transaction detail based on transaction id
            transaction = get_transaction_details(transaction_id)

            # Check payment state, if state is FULFILL, mark is_paid of subscription to true.
            try:
                donation = Donation.objects.get(transaction_id=transaction_id)
                donation.status = str(transaction.state)
                donation.amount = transaction.authorization_amount
                donation.currency = transaction.currency
                donation.creation_date = transaction.created_on.isoformat()
                donation.failure_reason = transaction.failure_reason
                donation.internet_protocol_address = transaction.internet_protocol_address
                donation.internet_protocol_address_country = transaction.internet_protocol_address_country
                donation.invoice_merchant_reference = transaction.invoice_merchant_reference
                donation.save()

                if str(transaction.state) == "TransactionState.FULFILL":
                    is_payment_succeed = True
                    message = "Donation has been completed."
                else:
                    # Mark transaction status as failed
                    if str(transaction.state) == "TransactionState.FAILED":
                        is_payment_succeed = True
                        message = "Donation has not been completed."

            except Donation.DoesNotExist as err:
                return Response({"message": "Invalid transaction id!"}, status=status.HTTP_404_NOT_FOUND)

            if is_payment_succeed:
                return Response({
                    "message": message
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": message
                }, status=status.HTTP_402_PAYMENT_REQUIRED)
            
        except Transactions.DoesNotExist as err:
            return JsonResponse({'error': f"Invalid transaction id: {transaction_id}"}, status=status.HTTP_404_NOT_FOUND)


class PaymentViewset(BaseUUIDViewSet):
    parser_classes = [IsAdminUser]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]


class TransactionListView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', '')
        sort_by = request.query_params.get('sort', '-creation_date')  # Default sort by newest
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 9))  # 9 items per page as shown in the image

        transactions = Transactions.objects.select_related('user', 'subscription').filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(transaction_id__icontains=search_query)
        ).order_by(sort_by)

        paginator = Paginator(transactions, per_page)
        page_obj = paginator.get_page(page)

        serializer = TransactionListSerializer(page_obj, many=True)
        
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next() and page + 1 or None,
            'previous': page_obj.has_previous() and page - 1 or None,
            'page': page,
            'per_page': per_page,
            'total_pages': paginator.num_pages
        }, status=status.HTTP_200_OK)