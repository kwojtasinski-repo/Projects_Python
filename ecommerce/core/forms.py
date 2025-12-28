from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES=(
    ('S','Stripe'),
    ('P','PayPal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    shipping_zip = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    billing_zip = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)

    same_billing_address  = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

    def clean(self):
        cleaned_data = super().clean()

        use_default_shipping = cleaned_data.get('use_default_shipping')
        use_default_billing = cleaned_data.get('use_default_billing')
        same_billing = cleaned_data.get('same_billing_address')

        shipping_address = cleaned_data.get('shipping_address')
        shipping_country = cleaned_data.get('shipping_country')
        shipping_zip = cleaned_data.get('shipping_zip')
        shipping_city = cleaned_data.get('shipping_city')

        billing_address = cleaned_data.get('billing_address')
        billing_country = cleaned_data.get('billing_country')
        billing_zip = cleaned_data.get('billing_zip')
        billing_city = cleaned_data.get('billing_city')

        payment_option = cleaned_data.get('payment_option')

        # 1️⃣ Shipping validation
        if not use_default_shipping:
            if not all([shipping_address, shipping_country, shipping_zip, shipping_city]):
                raise forms.ValidationError(
                    "Please complete the shipping address."
                )

        # 2️⃣ Billing validation
        if not same_billing and not use_default_billing:
            if not all([billing_address, billing_country, billing_zip, billing_city]):
                raise forms.ValidationError(
                    "Please complete the billing address."
                )

        # 3️⃣ Payment option sanity check
        if payment_option not in dict(PAYMENT_CHOICES):
            raise forms.ValidationError("Invalid payment option.")

class CouponForm(forms.Form):
    # bierze dane z formularza order_snippet po klasie form-control i placeholder itd
    code=forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Promo code',
            'aria-label': 'Recipient\'s username',
            'aria-describedby': 'basic-addon2'
    }))

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    email = forms.EmailField()

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
