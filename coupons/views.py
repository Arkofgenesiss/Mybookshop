from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                translations__code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
            messages.success(request, _('Coupon was successfully applied'))
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, _('Invalid coupon code'))

    return redirect('cart:cart_detail')
# Create your views here.
