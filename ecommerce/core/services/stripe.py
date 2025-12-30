from uuid import uuid4
import stripe
from django.conf import settings
from core.models import PROVIDER_STRIPE, STATUS_PAID, STATUS_PENDING, Payment, Order, UserProfile

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_or_create_customer(userprofile, email):
    if userprofile.stripe_customer_id:
        return stripe.Customer.retrieve(userprofile.stripe_customer_id)

    customer = stripe.Customer.create(email=email)
    userprofile.stripe_customer_id = customer["id"]
    userprofile.one_click_purchasing = True
    userprofile.save()

    return customer


def attach_card_to_customer(customer, token):
    customer.sources.create(source=token)


def charge_customer(order, user, token=None, customer=None):
    amount = int(order.get_total() * 100)

    if customer:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            customer=customer.id
        )
    else:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token
        )

    return charge


def process_stripe_payment(
    *,
    order: Order,
    user,
    userprofile: UserProfile,
    token: str | None,
    save_card: bool = False,
    use_default: bool = False,
) -> Payment:
    if not settings.PAYMENTS_ENABLED:
        # DEV / MOCK PAYMENT
        payment = Payment.objects.create(
            order=order,
            provider_payment_id=f"dev_charge_{uuid4().hex}",
            user=user,
            amount=order.get_total(),
            provider=PROVIDER_STRIPE,
            status=STATUS_PENDING,
        )

        payment.status = STATUS_PAID
        payment.save(update_fields=["status"])
        order.items.update(ordered=True)
        order.ordered = True
        order.save()

        return payment

    customer = None

    if save_card or use_default:
        customer = get_or_create_customer(
            userprofile=userprofile,
            email=user.email
        )

    if save_card:
        attach_card_to_customer(customer, token)

    charge = charge_customer(
        order=order,
        user=user,
        token=None if use_default else token,
        customer=customer if use_default else None
    )

    if charge["status"] != "succeeded":
        raise ValueError("Stripe charge failed")

    if charge["amount"] != int(order.get_total() * 100):
        raise ValueError("Amount mismatch")

    if charge["currency"] != "usd":
        raise ValueError("Currency mismatch")

    payment = Payment.objects.create(
        provider_payment_id=charge["id"],
        user=user,
        amount=order.get_total(),
        provider=PROVIDER_STRIPE,
        status=STATUS_PENDING,
    )

    payment.status = STATUS_PAID
    payment.save(update_fields=["status"])
    order.items.update(ordered=True)
    order.ordered = True
    order.save()

    return payment
