from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock, patch
from core.models import Order, OrderItem, Item
from core.services.stripe import process_stripe_payment

User = get_user_model()

class ProcessStripePaymentTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="pass"
        )

        self.userprofile = self.user.userprofile

        self.item = Item.objects.create(
            title="Test item",
            price=10
        )

        self.order = Order.objects.create(
            user=self.user,
            ordered=False,
            ordered_date=timezone.now()
        )
        
        self.order_item = OrderItem.objects.create(
            user=self.user,
            item=self.item,
            ordered=False,
            quantity=2
        )

        self.order.items.add(self.order_item)

    @patch("core.services.stripe.charge_customer")
    def test_process_stripe_payment_marks_order_as_paid(self, mock_charge):
        mock_charge.return_value = {"id": "ch_123"}

        process_stripe_payment(
            order=self.order,
            user=self.user,
            userprofile=self.userprofile,
            token="ch_123",
            save_card=False,
            use_default=False,
        )

        self.order.refresh_from_db()
        self.order_item.refresh_from_db()
        self.assertTrue(self.order.ordered)
        self.assertIsNotNone(self.order.payment)
        self.assertEqual(self.order.payment.stripe_charge_id, "ch_123")
        self.assertTrue(self.order_item.ordered)

    def test_process_stripe_payment_requires_keywords(self):
        with self.assertRaises(TypeError):
            process_stripe_payment(
                self.order,
                self.user,
                self.userprofile,
                "tok_test"
            )

    @patch("core.services.stripe.attach_card_to_customer")
    @patch("core.services.stripe.get_or_create_customer")
    @patch("core.services.stripe.charge_customer")
    def test_save_card_creates_customer_and_attaches_card(
        self,
        mock_charge,
        mock_get_customer,
        mock_attach_card,
    ):
        mock_charge.return_value = {"id": "ch_test_456"}

        fake_customer = MagicMock()
        fake_customer.id = "cus_123"
        mock_get_customer.return_value = fake_customer

        process_stripe_payment(
            order=self.order,
            user=self.user,
            userprofile=self.userprofile,
            token="tok_test",
            save_card=True,
            use_default=False,
        )

        mock_get_customer.assert_called_once_with(
            userprofile=self.userprofile,
            email=self.user.email
        )

        mock_attach_card.assert_called_once_with(
            fake_customer,
            "tok_test"
        )

    @patch("core.services.stripe.attach_card_to_customer")
    @patch("core.services.stripe.get_or_create_customer")
    @patch("core.services.stripe.charge_customer")
    def test_use_default_card_does_not_use_token(
        self,
        mock_charge,
        mock_get_customer,
        mock_attach_card,
    ):
        fake_customer = MagicMock()
        fake_customer.id = "cus_999"
        mock_get_customer.return_value = fake_customer
        mock_charge.return_value = {"id": "ch_test_789"}

        process_stripe_payment(
            order=self.order,
            user=self.user,
            userprofile=self.userprofile,
            token="tok_should_not_be_used",
            save_card=False,
            use_default=True,
        )

        mock_charge.assert_called_once_with(
            order=self.order,
            user=self.user,
            token=None,
            customer=fake_customer,
        )

        mock_attach_card.assert_not_called()