from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import PROVIDER_PAYPAL, STATUS_PAID, STATUS_PENDING, Item, Order, OrderItem, Address, Payment, Coupon, Refund, UserProfile
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
import stripe
from .services.checkout import handle_addresses
from .services.paypal import (
    execute_payment,
    create_payment
)
from core.services.stripe import process_stripe_payment
from django.conf import settings
from uuid import uuid4
import json

# Create your views here.

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            form = CheckoutForm()

            context = {'form': form,
                       'couponform': CouponForm(),
                       'order': order,
                       'DISPLAY_COUPON_FORM': True
            }
            
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context['default_shipping_address'] = shipping_address_qs[0]

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context['default_billing_address'] = billing_address_qs[0]

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No active order")
            return redirect("core:order-summary")

        if not form.is_valid():
            return render(self.request, "checkout.html", {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
            })

        handle_addresses(order, self.request.user, form.cleaned_data)

        payment = form.cleaned_data['payment_option']
        return redirect(
            'core:payment',
            payment_option='stripe' if payment == 'S' else 'paypal'
        )


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered = False)
        method = self.kwargs.get('payment_option').lower()
        print(method)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                #fetch the users
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context
                    context.update(
                        {
                            'card': card_list[0]
                        }
                    )
            
            if method == 'stripe':
                return render(self.request, "payment.html", context)
            elif method == 'paypal':
                return render(self.request, "payment_paypal.html", context)
        else:
            print(order)
            messages.warning(self.request, "You have not added the billing address")
            return redirect("core:checkout")


    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)

        if not form.is_valid():
            messages.warning(self.request, "Invalid data received")
            return redirect("/payment/stripe/")

        try:
            process_stripe_payment(
                order=order,
                user=self.request.user,
                userprofile=userprofile,
                token=form.cleaned_data.get("stripeToken"),
                save_card=form.cleaned_data.get("save"),
                use_default=form.cleaned_data.get("use_default"),
            )

            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            messages.warning(self.request, f"{e.error.message}")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, "Something went wrong. You were not charged. Please try again")

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.warning(self.request, "A serious error occurerd. We have been notified.")

        return redirect("/payment/stripe/")


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={'object': order}
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")



class ItemDetail(DetailView):
    model = Item
    template_name = "product.html"

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():#odniesienie item___slug bezposrednio do pola w sql
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("core:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("core:order-summary")
    #return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():#odniesienie item___slug bezposrednio do pola w sql
            order_item=OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            print("This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():#odniesienie item___slug bezposrednio do pola w sql
            order_item=OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            print("This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return  coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered = False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        context = {'form': form}
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                #store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")
            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exists.")
                return redirect("core:request-refund")

class PaypalCreatePaymentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)

        payment = Payment.objects.create(
            order=order,
            user=request.user,
            provider=PROVIDER_PAYPAL,
            provider_payment_id=f"pending_{uuid4().hex}",
            amount=order.get_total(),
            status=STATUS_PENDING,
        )

        if not settings.PAYMENTS_ENABLED:
            payment.provider_payment_id = f"dev_paypal_{payment.id}"
            payment.save(update_fields=["provider_payment_id"])
            return JsonResponse({
                "paymentID": payment.provider_payment_id,
                "approval_url": "/payment/paypal/execute/",
            })

        payment = create_payment(order)
        payment.provider_payment_id = f"dev_paypal_{payment.id}"
        payment.save(update_fields=["provider_payment_id"])

        approval_url = next(
            link.href for link in payment.links if link.rel == "approval_url"
        )

        return JsonResponse({
            "paymentID": payment.provider_payment_id,
            "approval_url": approval_url,
        })


class PaypalExecutePaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get("paymentID")
        payment = (
            Payment.objects
            .filter(
                provider=PROVIDER_PAYPAL,
                provider_payment_id=payment_id,
                status=STATUS_PENDING
            )
            .first()
        )

        if not payment:
            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        if payment.user != request.user:
            return redirect("/")

        messages.info(request, "Payment is not paid.")
        return redirect("/payment/paypal/")

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))

        payment_id = data.get("paymentID")
        payer_id = data.get("payerID")

        payment = get_object_or_404(
            Payment,
            provider=PROVIDER_PAYPAL,
            provider_payment_id=payment_id,
            status=STATUS_PENDING,
        )

        order = payment.order

        if order.user != request.user:
            return JsonResponse({"success": False}, status=403)

        if not settings.PAYMENTS_ENABLED:
            payment.status = STATUS_PAID
            payment.save(update_fields=["status"])

            order.ordered = True
            order.ordered_date = timezone.now()
            order.items.update(ordered=True)
            order.save(update_fields=["ordered", "ordered_date"])

            return JsonResponse({"success": True})

        paypal_payment = execute_payment(payment_id, payer_id)
        txn = paypal_payment.transactions[0]

        if txn.amount.total != f"{payment.amount:.2f}":
            return JsonResponse({"success": False}, status=400)

        payment.status = STATUS_PAID
        payment.save(update_fields=["status"])

        order.ordered = True
        order.ordered_date = timezone.now()
        order.items.update(ordered=True)
        order.save(update_fields=["ordered", "ordered_date"])

        return JsonResponse({"success": True})
