from .cart import Cart
from .forms import CouponApplyForm

def cart(request):
    return {
        'cart': Cart(request),
        'coupon_apply_form': CouponApplyForm()
    }