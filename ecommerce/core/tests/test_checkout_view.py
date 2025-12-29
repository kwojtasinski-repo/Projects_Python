from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import Order

User = get_user_model()


class CheckoutViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="pass"
        )
        self.client.login(username="test", password="pass")

        self.order = Order.objects.create(
            user=self.user,
            ordered=False,
            ordered_date=timezone.now()
        )

    def test_invalid_post_renders_checkout(self):
        response = self.client.post(
            reverse("core:checkout"),
            data={}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout.html")
        self.assertTrue(response.context["form"].errors)

    def test_valid_post_redirects_to_payment(self):
        response = self.client.post(
            reverse("core:checkout"),
            data={
                "shipping_address": "Main St",
                "shipping_country": "PL",
                "shipping_zip": "00-001",
                "shipping_city": "Warsaw",

                "billing_address": "Other St",
                "billing_country": "PL",
                "billing_zip": "00-002",
                "billing_city": "Warsaw",

                "payment_option": "S",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/payment/stripe/", response.url)
