from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.conf import settings

class Coupon(TranslatableModel):
    translations = TranslatedFields(
        code=models.CharField(_('Coupon code'), max_length=50, unique=True),
        name=models.CharField(_('Coupon name'), max_length=100, blank=True)
    )

    valid_from = models.DateTimeField(
        _('Valid from'),
        help_text=_('Date and time when the coupon becomes active')
    )
    valid_to = models.DateTimeField(
        _('Valid to'),
        help_text=_('Date and time when the coupon expires')
    )
    discount = models.IntegerField(
        _('Discount percentage'),
        validators=[
            MinValueValidator(0, _('Discount cannot be less than 0%')),
            MaxValueValidator(100, _('Discount cannot be greater than 100%'))
        ],
        help_text=_('Percentage discount (from 0 to 100)')
    )
    active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Whether the coupon is currently active')
    )

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
        ordering = ['-valid_from']
        indexes = [
            models.Index(fields=['valid_from', 'valid_to']),
        ]

    def __str__(self):
        try:
            code = self.safe_translation_getattr('code', any_language=True)
            return f"{code} ({self.discount}%)"
        except Exception:
            return f"Coupon #{self.id or 'new'}"

    def is_valid(self):
        now = timezone.now()
        return (self.active and self.valid_from <= now <= self.valid_to)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        translation = self.get_current_language() or settings.LANGUAGE_CODE
        self.translations.filter(language_code=translation).update(
            code=self.code.upper() if hasattr(self, 'code') else ''
        )
