from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Order
from core.services.checkout import handle_addresses

User = get_user_model()

class HandleAddressesTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="pass"
        )
        self.order = Order.objects.create(
            user=self.user,
            ordered=False,
            ordered_date=timezone.now()
        )

    def test_creates_shipping_and_billing_addresses(self):
        data = {
            "shipping_address": "Main St",
            "shipping_address2": "",
            "shipping_country": "PL",
            "shipping_zip": "00-001",
            "shipping_city": "Warsaw",
            "billing_address": "Other St",
            "billing_address2": "",
            "billing_country": "PL",
            "billing_zip": "00-002",
            "billing_city": "Warsaw",
            "same_billing_address": False,
            "use_default_shipping": False,
            "use_default_billing": False
        }

        handle_addresses(self.order, self.user, data)

        self.order.refresh_from_db()

        self.assertIsNotNone(self.order.shipping_address)
        self.assertIsNotNone(self.order.billing_address)
        self.assertEqual(self.order.shipping_address.address_type, "S")
        self.assertEqual(self.order.billing_address.address_type, "B")