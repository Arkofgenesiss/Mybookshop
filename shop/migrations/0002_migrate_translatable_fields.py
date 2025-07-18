from django.db import migrations
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

def forwards_func(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    CategoryTranslation = apps.get_model('shop', 'CategoryTranslation')
    Book = apps.get_model('shop', 'Book')
    BookTranslation = apps.get_model('shop', 'BookTranslation')

    for obj in Category.objects.all():
        CategoryTranslation.objects.create(
            master_id=obj.pk,
            language_code=settings.LANGUAGE_CODE,
            name=obj.name,
            slug=obj.slug
        )

    for obj in Book.objects.all():
        BookTranslation.objects.create(
            master_id=obj.pk,
            language_code=settings.LANGUAGE_CODE,
            title=obj.title,
            slug=obj.slug,
            description=obj.description
        )

def backwards_func(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    CategoryTranslation = apps.get_model('shop', 'CategoryTranslation')
    Book = apps.get_model('shop', 'Book')
    BookTranslation = apps.get_model('shop', 'BookTranslation')

    # Восстанавливаем данные для Category
    for obj in Category.objects.all():
        try:
            translation = CategoryTranslation.objects.get(
                master_id=obj.pk,
                language_code=settings.LANGUAGE_CODE
            )
            obj.name = translation.name
            obj.slug = translation.slug
            obj.save()
        except ObjectDoesNotExist:
            pass

    # Восстанавливаем данные для Book
    for obj in Book.objects.all():
        try:
            translation = BookTranslation.objects.get(
                master_id=obj.pk,
                language_code=settings.LANGUAGE_CODE
            )
            obj.title = translation.title
            obj.slug = translation.slug
            obj.description = translation.description
            obj.save()
        except ObjectDoesNotExist:
            pass

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]