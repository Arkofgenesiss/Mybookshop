from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_('name'), max_length=200, db_index=True),
        slug=models.SlugField(_('slug'), max_length=200, db_index=True, unique=True)
    )

    class Meta:
        # ordering commented for parler compatibility
        # ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:book_list_by_category',
                       args=[self.slug])


class Book(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=200, db_index=True),
        slug=models.SlugField(_('slug'), max_length=200, db_index=True),
        description=models.TextField(_('description'), blank=True)
    )

    category = models.ForeignKey(
        Category,
        related_name='books',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Category")
    )
    author = models.CharField(_('author'), max_length=200)
    cover = models.ImageField(_('cover'), upload_to='books/%Y/%m/%d', blank=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_('stock'), default=0)
    available = models.BooleanField(_('available'), default=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        ordering = ('-created',)
        # index_together commented for parler compatibility
        # index_together = (('id', 'slug'),)
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:book_detail',
                       args=[self.id, self.slug])