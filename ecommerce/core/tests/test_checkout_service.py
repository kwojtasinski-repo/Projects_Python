from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Order, Address
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

    def test_uses_default_shipping_address(self):
        Address.objects.create(
            user=self.user,
            address_type="S",
            default=True,
            street_address="Default St",
            city="X",
            zip="00-000",
            country="PL"
        )

        data = {
            "use_default_shipping": True,
            "same_billing_address": True
        }

        handle_addresses(self.order, self.user, data)

        self.assertEqual(
            self.order.shipping_address.street_address,
            "Default St"
        )

    def test_same_billing_address(self):
        data = {
            "shipping_address": "Main St",
            "shipping_address2": "",
            "shipping_country": "PL",
            "shipping_zip": "00-001",
            "shipping_city": "Warsaw",
            "same_billing_address": True,
            "use_default_shipping": False
        }

        handle_addresses(self.order, self.user, data)

        self.assertEqual(
            self.order.billing_address.street_address,
            self.order.shipping_address.street_address
        )
        self.assertEqual(
            self.order.billing_address.city,
            self.order.shipping_address.city
        )
        self.assertEqual(
            self.order.billing_address.zip,
            self.order.shipping_address.zip
        )
        self.assertEqual(
            self.order.billing_address.country,
            self.order.shipping_address.country
        )

    def test_uses_default_billing_address(self):
        Address.objects.create(
            user=self.user,
            address_type="B",
            default=True,
            street_address="Default Billing St",
            city="Y",
            zip="00-003",
            country="PL"
        )

        data = {
            "use_default_billing": True,
            "use_default_shipping": False,
            "shipping_address": "Main St",
            "shipping_address2": "",
            "shipping_country": "PL",
            "shipping_zip": "00-001",
            "shipping_city": "Warsaw"
        }

        handle_addresses(self.order, self.user, data)

        self.assertEqual(
            self.order.billing_address.street_address,
            "Default Billing St"
        )
        self.assertEqual(
            self.order.billing_address.city,
            "Y"
        )
        self.assertEqual(
            self.order.billing_address.zip,
            "00-003"
        )
        self.assertEqual(
            self.order.billing_address.country,
            "PL"
        )
