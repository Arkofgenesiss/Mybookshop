from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from .models import Category, Book
from cart.forms import CartAddBookForm

def book_list(request, category_slug=None):
    language = get_language()
    category = None
    categories = Category.objects.all()
    books = Book.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug
        )
        books = books.filter(category=category)

    cart_book_form = CartAddBookForm()

    return render(request, 'shop/book/list.html', {
        'category': category,
        'categories': categories,
        'books': books,
        'cart_book_form': cart_book_form
    })

def book_detail(request, id, slug):
    language = get_language()
    book = get_object_or_404(
        Book,
        id=id,
        translations__language_code=language,
        translations__slug=slug,
        available=True
    )
    cart_book_form = CartAddBookForm()
    return render(request, 'shop/book/detail.html', {
        'book': book,
        'cart_book_form': cart_book_form
    })