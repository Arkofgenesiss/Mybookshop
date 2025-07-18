from django.contrib import admin
from parler.admin import TranslatableAdmin
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _

@admin.register(Coupon)
class CouponAdmin(TranslatableAdmin):
    list_display = ['get_code', 'get_name', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['translations__code', 'translations__name']
    date_hierarchy = 'valid_from'

    fieldsets = (
        (None, {
            'fields': ('code', 'name', 'active')
        }),
        (_('Validity'), {
            'fields': ('valid_from', 'valid_to'),
        }),
        (_('Discount'), {
            'fields': ('discount',),
        }),
    )

    def get_code(self, obj):
        return obj.code
    get_code.short_description = _('Code')
    get_code.admin_order_field = 'translations__code'

    def get_name(self, obj):
        return obj.name
    get_name.short_description = _('Name')
    get_name.admin_order_field = 'translations__name'