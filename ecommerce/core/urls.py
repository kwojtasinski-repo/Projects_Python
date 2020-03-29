from django.urls import path, include
from .views import (ItemDetail, CheckoutView, HomeView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, PaymentView, AddCouponView, RequestRefundView, Payment_Paypal)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('products/<slug>/', ItemDetail.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('payment/reqfe/<payment_option>/', Payment_Paypal.as_view(), name='payment-paypal'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
    #path('', views.home, name='home'),
]
