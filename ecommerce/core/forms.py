from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

LABELS = {
    'shipping_address': 'Shipping address',
    'shipping_country': 'Shipping country',
    'shipping_zip': 'Shipping ZIP code',
    'shipping_city': 'Shipping city',
    'billing_address': 'Billing address',
    'billing_country': 'Billing country',
    'billing_zip': 'Billing ZIP code',
    'billing_city': 'Billing city',
}

PAYMENT_CHOICES=(
    ('S','Stripe'),
    ('P','PayPal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(
        blank_label='(select country)'
    ).formfield(
        required=False,
        widget=CountrySelectWidget(attrs={'class': 'custom-select'})
    )
    shipping_zip = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(
        blank_label='(select country)'
    ).formfield(
        required=False,
        widget=CountrySelectWidget(attrs={'class': 'custom-select'})
    )
    billing_zip = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=PAYMENT_CHOICES
    )

    def clean(self):
        cleaned = super().clean()

        use_default_shipping = cleaned.get('use_default_shipping')
        use_default_billing = cleaned.get('use_default_billing')
        same_billing = cleaned.get('same_billing_address')

        if not use_default_shipping:
            self._require_fields(
                cleaned,
                ['shipping_address', 'shipping_country', 'shipping_zip', 'shipping_city'],
                prefix='shipping'
            )

        if not same_billing and not use_default_billing:
            self._require_fields(
                cleaned,
                ['billing_address', 'billing_country', 'billing_zip', 'billing_city'],
                prefix='billing'
            )

        return cleaned

    def _require_fields(self, data, fields, prefix):
        for field in fields:
            if not data.get(field):
                label = LABELS.get(
                    field,
                    field.replace('_', ' ').capitalize()
                )
                self.add_error(field, f"{label} is required.")

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
