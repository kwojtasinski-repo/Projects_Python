import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_payment(order):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": settings.PAYPAL_RETURN_URL,
            "cancel_url": settings.PAYPAL_CANCEL_URL,
        },
        "transactions": [{
            "amount": {
                "total": f"{order.get_total():.2f}",
                "currency": "USD",
            },
            "description": f"Order #{order.id}",
        }]
    })

    if not payment.create():
        raise Exception(payment.error)

    return payment


def execute_payment(payment_id, payer_id):
    payment = paypalrestsdk.Payment.find(payment_id)

    if not payment.execute({"payer_id": payer_id}):
        raise Exception(payment.error)

    return payment
