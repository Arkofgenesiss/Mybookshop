from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path(_('<slug:category_slug>/'), views.book_list, name='book_list_by_category'),
    path(_('<int:id>/<slug:slug>/'), views.book_detail, name='book_detail'),
]