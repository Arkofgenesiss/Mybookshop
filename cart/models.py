from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.utils import timezone


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True, verbose_name=_("Name")),
        slug=models.SlugField(max_length=200, db_index=True, unique=True, verbose_name=_("Slug"))
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Book(TranslatableModel):
    created = models.DateTimeField(default=timezone.now)
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name=_("Title")),
        description=models.TextField(blank=True, verbose_name=_("Description")))

    author = models.CharField(max_length=100, verbose_name=_("Author"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    cover = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name=_("Cover"))
    created = models.DateTimeField(null=True, blank=True)
    available = models.BooleanField(default=True, verbose_name=_("Available"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('bookshop:book_detail', args=[self.id])

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ('-created',)