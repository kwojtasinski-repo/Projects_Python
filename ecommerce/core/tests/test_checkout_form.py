from django.test import TestCase
from core.forms import CheckoutForm


class CheckoutFormTests(TestCase):

    def test_valid_checkout_form(self):
        form = CheckoutForm(data={
            "shipping_address": "Main St",
            "shipping_country": "PL",
            "shipping_zip": "00-001",
            "shipping_city": "Warsaw",

            "billing_address": "Other St",
            "billing_country": "PL",
            "billing_zip": "00-002",
            "billing_city": "Warsaw",

            "payment_option": "S",
        })

        self.assertTrue(form.is_valid())

    def test_missing_shipping_country_is_invalid(self):
        form = CheckoutForm(data={
            "shipping_address": "Main St",
            "shipping_zip": "00-001",
            "shipping_city": "Warsaw",
            "payment_option": "S",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("shipping_country", form.errors)

    def test_same_billing_address_skips_billing_validation(self):
        form = CheckoutForm(data={
            "shipping_address": "Main St",
            "shipping_country": "PL",
            "shipping_zip": "00-001",
            "shipping_city": "Warsaw",

            "same_billing_address": True,
            "payment_option": "S",
        })

        self.assertTrue(form.is_valid())

    def test_use_default_shipping_skips_shipping_fields(self):
        form = CheckoutForm(data={
            "use_default_shipping": True,
            "use_default_billing": True,
            "payment_option": "S",
        })

        self.assertTrue(form.is_valid())
