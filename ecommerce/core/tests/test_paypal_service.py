from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch

from core.models import Order

User = get_user_model()


class PaypalViewsTests(TestCase):

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

    @patch("core.views.create_payment")
    def test_create_payment_returns_approval_url(self, mock_create):
        fake_payment = type(
            "Payment",
            (),
            {
                "id": "pay_123",
                "links": [
                    type("Link", (), {
                        "rel": "approval_url",
                        "href": "https://paypal.test/approve"
                    })()
                ]
            }
        )
        mock_create.return_value = fake_payment

        response = self.client.post(
            reverse("core:paypal-create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("approval_url", response.json())

    @patch("core.views.execute_payment")
    def test_execute_payment_returns_success(self, mock_execute):
        response = self.client.post(
            reverse("core:paypal-execute"),
            data={
                "paymentID": "pay_123",
                "payerID": "payer_456"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
