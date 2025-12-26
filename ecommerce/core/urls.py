from django.urls import path
from .views import (
    ItemDetail,
    CheckoutView,
    HomeView,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    Payment_Paypal
)

app_name = 'core'

urlpatterns = [
    # Home / products
    path('', HomeView.as_view(), name='home'),
    path('products/<slug>/', ItemDetail.as_view(), name='product'),

    # Cart
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),

    # Checkout / order
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),

    # Payment
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),

    # LEGACY — Paypal (to remove later)
    path('payment/reqfe/<payment_option>/', Payment_Paypal.as_view(), name='payment-paypal')
]
