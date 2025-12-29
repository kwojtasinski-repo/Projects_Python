import stripe
from django.conf import settings
from core.models import Payment, Order, UserProfile

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

    payment = Payment.objects.create(
        stripe_charge_id=charge["id"],
        user=user,
        amount=order.get_total()
    )

    order.items.update(ordered=True)
    order.ordered = True
    order.payment = payment
    order.save()

    return payment
