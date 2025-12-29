from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import OrderItem, Item
from django.template import Context, Template

User = get_user_model()

class CartItemCountTemplateFilterTests(TestCase):

    def test_cart_item_count_sums_quantity(self):
        user = User.objects.create_user(username="test", password="pass")
        item = Item.objects.create(title="Test", price=10)

        OrderItem.objects.create(
            user=user,
            item=item,
            quantity=3,
            ordered=False
        )
        OrderItem.objects.create(
            user=user,
            item=item,
            quantity=2,
            ordered=False
        )

        tpl = Template(
            "{% load cart_tags %}{{ user|cart_item_count }}"
        )
        rendered = tpl.render(Context({"user": user}))

        self.assertEqual(rendered, "5")
