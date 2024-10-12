from postfinancecheckout import Configuration
from postfinancecheckout.api import (
    TransactionServiceApi,
    TransactionPaymentPageServiceApi,
    TransactionCompletionServiceApi
)
from postfinancecheckout.models import LineItem, LineItemType, TransactionCreate
from .models import Payment, Transactions
from apps.package.models import Package, Subscription
import os


SPACE_ID = os.getenv("SPACE_ID")
USER_ID = os.getenv("USER_ID")
API_SECRET = os.getenv("API_SECRET")


def get_postfinance_config():
    config = Configuration(
        user_id=USER_ID,
        api_secret=API_SECRET,
        request_timeout=30,
    )
    return config


def check_transaction_status(transaction_id, config):
    api_instance = TransactionServiceApi(configuration=config)
    try:
        transaction = api_instance.read(SPACE_ID, transaction_id)
        return transaction.state
    except Exception as e:
        print(f"Exception when calling TransactionServiceApi->read: {e}")
        return None
    

def get_transaction_details(transaction_id):
    config = get_postfinance_config()
    transaction_service = TransactionServiceApi(configuration=config)
    
    try:
        transaction = transaction_service.read(space_id=SPACE_ID, id=transaction_id)
        return transaction
    except Exception as e:
        print(f"Exception when retrieving transaction: {e}")
        return None
    

def create_payment_url(payload):
    config = get_postfinance_config()
    transaction_service = TransactionServiceApi(configuration=config)
    transaction_payment_service = TransactionPaymentPageServiceApi(configuration=config)
    
    line_item = LineItem(
        name = payload.get("name"),
        unique_id=payload.get("unique_id"),
        quantity=payload.get("quantity"),
        amount_including_tax=payload.get("amount"),
        type=LineItemType.PRODUCT,
        donation=payload.get("donations"),
        user_id=payload.get("user_id"),
    )
    
    success_url = payload.get("success_url")
    cancel_url = payload.get("cancel_url")
    
    transaction = TransactionCreate(
        line_items = [line_item],
        auto_confirmation_enabled=True,
        currency=payload.get("currency"),
        success_url = success_url,
        failed_url = cancel_url
    )
    try:
        transaction_create = transaction_service.create(space_id=SPACE_ID, transaction=transaction)
        transaction_id = transaction_create.id
        payment_page_url = transaction_payment_service.payment_page_url(space_id=SPACE_ID, id=transaction_create.id)
        error = None
        return transaction_id, payment_page_url, error
    
    except Exception as error:
        return 0, None, error


def update_payment_record(transactions, postfinance):
    subscription = Subscription.objects.get(id=transactions.subscription.id)
    package_price = subscription.package.price
    donation = float(postfinance.authorization_amount) - float(package_price)

    data = {
        "transaction": transactions,
        "package_name": postfinance.line_items[0].to_dict().get("name", "") if len(postfinance.line_items) else "",
        "amount": postfinance.authorization_amount,
        "currency": postfinance.currency,
        "donations": donation,
        "status": str(postfinance.state),
        "original_amount": float(package_price),
        "failure_reason": postfinance.failure_reason,
        "internet_protocol_address": postfinance.internet_protocol_address,
        "internet_protocol_address_country": postfinance.internet_protocol_address_country,
        "invoice_merchant_reference": postfinance.invoice_merchant_reference,
    }

    is_payment_exists = Payment.objects.filter(transaction=transactions)
    if len(is_payment_exists):
        is_payment_exists.update(**data)
    else:
        Payment.objects.create(**data)
    

def manage_payment_status(transaction_id):
    # Get transaction detail based on transaction id
    postfinance = get_transaction_details(transaction_id)
    
    transaction_details = {
        'transaction_id': postfinance.id,
        'state': str(postfinance.state),
        'amount': postfinance.authorization_amount,
        'currency': postfinance.currency,
        'created_on': postfinance.created_on.isoformat(),
    }

    transactions = Transactions.objects.filter(transaction_id=transaction_id)

    # Handle payment status
    update_payment_record(transactions, postfinance)



