from core.models import Address

def handle_addresses(order, user, data):
    # SHIPPING
    if data.get('use_default_shipping'):
        shipping = Address.objects.filter(
            user=user,
            address_type='S',
            default=True
        ).first()
    else:
        shipping = Address.objects.create(
            user=user,
            street_address=data['shipping_address'],
            apartment_address=data.get('shipping_address2'),
            country=data['shipping_country'],
            zip=data['shipping_zip'],
            city=data['shipping_city'],
            address_type='S',
            default=data.get('set_default_shipping', False)
        )

    # BILLING
    if data.get('same_billing_address'):
        billing = Address.objects.create(
            user=user,
            street_address=shipping.street_address,
            apartment_address=shipping.apartment_address,
            country=shipping.country,
            zip=shipping.zip,
            city=shipping.city,
            address_type='B'
        )
    elif data.get('use_default_billing'):
        billing = Address.objects.filter(
            user=user,
            address_type='B',
            default=True
        ).first()
    else:
        billing = Address.objects.create(
            user=user,
            street_address=data['billing_address'],
            apartment_address=data.get('billing_address2'),
            country=data['billing_country'],
            zip=data['billing_zip'],
            city=data['billing_city'],
            address_type='B',
            default=data.get('set_default_billing', False)
        )

    # -------- ASSIGN & SAVE ONCE --------
    order.shipping_address = shipping
    order.billing_address = billing
    order.save()

    return order
