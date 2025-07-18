from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order
from coupons.forms import CouponApplyForm


class OrderCreateForm(forms.ModelForm):
    coupon_code = forms.CharField(
        required=False,
        label=_('Coupon code'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter coupon code if you have one')
        })
    )

    class Meta:
        model = Order
        fields = ['email', 'postal_code']  # Только непереводимые поля
        labels = {
            'email': _('Email'),
            'postal_code': _('Postal code'),
        }

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)

        # Добавляем translatable поля вручную
        self.fields['first_name'] = forms.CharField(
            label=_('First name'),
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        self.fields['last_name'] = forms.CharField(
            label=_('Last name'),
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        self.fields['address'] = forms.CharField(
            label=_('Address'),
            widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        )
        self.fields['city'] = forms.CharField(
            label=_('City'),
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

        # Добавляем CSS классы ко всем полям
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            order.save()
            translation = order.get_current_language() or settings.LANGUAGE_CODE
            order.translations.create(
                language_code=translation,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city']
            )
        return order