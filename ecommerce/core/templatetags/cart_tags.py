from django import template
from django.db.models import Sum
from core.models import OrderItem

register = template.Library()

@register.filter
def cart_item_count(user):
    if not user.is_authenticated:
        return 0

    return (
        OrderItem.objects
        .filter(user=user, ordered=False)
        .aggregate(total=Sum("quantity"))
        .get("total")
        or 0
    )

