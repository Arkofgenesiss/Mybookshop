from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import csv
from .models import Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from coupons.models import Coupon
from shop.models import Book
from parler.admin import TranslatableAdmin


def export_to_csv(modeladmin, request, queryset):

    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
    writer = csv.writer(response)

    fields = [
        'ID', _('First name'), _('Last name'), _('Email'),
        _('Address'), _('Postal code'), _('City'),
        _('Paid'), _('Created'), _('Updated'),
        _('Coupon code'), _('Discount'), _('Total cost')
    ]
    writer.writerow(fields)

    for obj in queryset:
        data_row = [
            obj.id,
            obj.first_name,
            obj.last_name,
            obj.email,
            obj.address,
            obj.postal_code,
            obj.city,
            obj.paid,
            obj.created.strftime('%d/%m/%Y'),
            obj.updated.strftime('%d/%m/%Y'),
            obj.coupon.code if obj.coupon else '',
            f"{obj.discount}%" if obj.coupon else '0%',
            f"${obj.get_total_cost():.2f}"
        ]
        writer.writerow(data_row)
    return response
export_to_csv.short_description = _('Export to CSV')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']
    extra = 0
    fields = ['book', 'price', 'quantity', 'get_cost']
    readonly_fields = ['get_cost']

    def get_cost(self, obj):
        return f"${obj.get_cost():.2f}"
    get_cost.short_description = _('Total')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'book':
            kwargs['queryset'] = Book.objects.filter(available=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change and obj.book:
            obj.price = obj.book.price
        super().save_model(request, obj, form, change)

@admin.register(Order)
class OrderAdmin(TranslatableAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'city', 'paid']
    list_filter = ['paid', 'created', 'updated', 'coupon']
    list_select_related = ['coupon']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    readonly_fields = ['created', 'updated', 'total_cost_display']
    search_fields = ['translations__first_name', 'translations__last_name', 'email', 'translations__city', 'coupon__code']

    fieldsets = (
        (_('Customer information'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Shipping information'), {
            'fields': ('address', 'postal_code', 'city')
        }),
        (_('Order information'), {
            'fields': ('paid', ('created', 'updated'), 'total_cost_display')
        }),
        (_('Coupon information'), {
            'fields': ('coupon', 'discount'),
            'classes': ('collapse',)
        }),
    )


    def customer_info(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_info.short_description = _('Customer')

    def created_short(self, obj):
        return obj.created.strftime('%d %b %Y')
    created_short.short_description = _('Created')

    def total_cost(self, obj):
        return f"${obj.get_total_cost():.2f}"
    total_cost.short_description = _('Total')

    def total_cost_display(self, obj):
        if obj.coupon:
            return format_html(
                "<div style='color:green;'>{}<br><small>{}: {} ({}% {})</small></div>",
                f"${obj.get_total_cost():.2f}",
                _('Discount applied'),
                obj.coupon.code,
                obj.discount,
                _('off')
            )
        return f"${obj.get_total_cost():.2f}"
    total_cost_display.short_description = _('Total with discount')

    def coupon_info(self, obj):
        if obj.coupon:
            return format_html(
                "{}<br><small>{}% {}</small>",
                obj.coupon.code,
                obj.discount,
                _('off')
            )
        return "-"
    coupon_info.short_description = _('Coupon')

    def order_detail_link(self, obj):
        return format_html(
            '<a href="{}" class="button">{} &rarr;</a>',
            reverse('orders:orders_order_detail', args=[obj.id]),
            _('View details')
        )
    order_detail_link.short_description = ''

    def save_model(self, request, obj, form, change):
        if obj.discount > 100:
            raise ValidationError(_('Discount cannot exceed 100%.'))
        super().save_model(request, obj, form, change)

@staff_member_required
def admin_order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    return render(request,
                'admin/orders/order/detail.html',
                {'order': order})