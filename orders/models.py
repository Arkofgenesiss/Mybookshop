from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from decimal import Decimal
from shop.models import Book
from coupons.models import Coupon
from parler.models import TranslatableModel, TranslatedFields


class Order(TranslatableModel):
    translations = TranslatedFields(
        first_name=models.CharField(_('first name'), max_length=50),
        last_name=models.CharField(_('last name'), max_length=50),
        address=models.CharField(_('address'), max_length=250),
        city=models.CharField(_('city'), max_length=100),
    )

    email = models.EmailField(_('email'))
    postal_code = models.CharField(_('postal code'), max_length=20)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    paid = models.BooleanField(_('paid'), default=False)

    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('coupon')
    )
    discount = models.IntegerField(
        _('discount'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_subtotal(self):
        return sum(item.get_cost() for item in self.items.all()) or Decimal('0')

    def get_discount_amount(self):
        if self.discount > 0:
            return self.get_subtotal() * (self.discount / Decimal('100'))
        return Decimal('0')

    def get_total_cost(self):
        total_cost = self.get_subtotal()
        return total_cost - total_cost * (self.discount / Decimal('100'))

    def get_absolute_url(self):
        return reverse('orders:order_detail', args=[self.id])

    def get_stripe_items(self):
        return [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.book.title,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': item.quantity,
        } for item in self.items.all()]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_('order')
    )
    book = models.ForeignKey(
        'shop.Book',
        related_name='order_items',
        on_delete=models.PROTECT,
        verbose_name=_('book')
    )
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        if self.price is None:  # Защита от None
            return Decimal('0')
        return self.price * self.quantity