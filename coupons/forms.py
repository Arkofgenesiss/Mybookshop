from django import forms
from django.utils.translation import gettext_lazy as _

class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label=_('Coupon code'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter coupon code'),
            'class': 'form-control'
        }),
        help_text=_('Enter your discount coupon code if you have one')
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        return code.strip().upper()