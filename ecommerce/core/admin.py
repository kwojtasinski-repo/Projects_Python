from django.contrib import admin
from .models import (
    Item,
    OrderItem,
    Order,
    Payment,
    Coupon,
    Refund,
    Address,
    UserProfile,
)

# ---------- ACTIONS ----------

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = "Mark refund as accepted"


# ---------- PAYMENT INLINE (READ-ONLY) ----------

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    can_delete = False

    readonly_fields = (
        "provider",
        "provider_payment_id",
        "amount",
        "status",
        "timestamp",
        "user",
    )


# ---------- ORDER ADMIN ----------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "ordered",
        "payment_status",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
        "ordered_date",
        'billing_address',
        'shipping_address',
        'coupon',
    )

    list_display_links = [
        'user',
        'billing_address',
        'shipping_address',
    ]

    list_filter = (
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
    )

    search_fields = (
        "user__username",
        "ref_code",
        "payments__provider_payment_id",
    )

    readonly_fields = (
        "user",
        "ordered_date",
        "ref_code",
    )

    actions = [make_refund_accepted]

    inlines = [PaymentInline]

    def payment_status(self, obj):
        last_payment = obj.payments.order_by("-timestamp").first()
        if not last_payment:
            return "—"
        return last_payment.status

    payment_status.short_description = "Payment status"


# ---------- PAYMENT ADMIN (LEDGER / READ-ONLY) ----------

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "provider",
        "provider_payment_id",
        "user",
        "order",
        "amount",
        "status",
        "timestamp",
    )

    list_filter = ("provider", "status")
    search_fields = ("provider_payment_id", "user__username", "order__id")

    readonly_fields = (
        "order",
        "provider",
        "provider_payment_id",
        "user",
        "amount",
        "status",
        "timestamp",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ---------- OTHER ADMINS ----------

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "street_address",
        "city",
        "country",
        "address_type",
        "default",
    )
    list_filter = ("default", "address_type", "country")
    search_fields = ("user__username", "street_address", "city", "zip")


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(UserProfile)
