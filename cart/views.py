from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Book
from .cart import Cart
from .forms import CartAddBookForm
from coupons.models import Coupon
from django.utils import timezone
from .forms import CouponApplyForm
from django.http import JsonResponse

@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            book=book,
            quantity=cd['quantity'],
            override_quantity=cd['update']
        )
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'total_items': cart.__len__(),
            'total_price': str(cart.get_total_price())  # Преобразуем в строку
        })
    return redirect('cart:cart_detail')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddBookForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            }
        )
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    })

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')