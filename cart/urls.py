from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path(_('add/') + '<int:book_id>/', views.cart_add, name='cart_add'),
    path(_('remove/') + '<int:book_id>/', views.cart_remove, name='cart_remove'),
    path(_('apply/'), views.coupon_apply, name='coupon_apply'),
]