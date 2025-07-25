# Generated by Django 5.2.3 on 2025-07-12 20:34

import django.core.validators
import django.db.models.deletion
import parler.fields
import parler.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(help_text='Date and time when the coupon becomes active', verbose_name='Valid from')),
                ('valid_to', models.DateTimeField(help_text='Date and time when the coupon expires', verbose_name='Valid to')),
                ('discount', models.IntegerField(help_text='Percentage discount (from 0 to 100)', validators=[django.core.validators.MinValueValidator(0, 'Discount cannot be less than 0%'), django.core.validators.MaxValueValidator(100, 'Discount cannot be greater than 100%')], verbose_name='Discount percentage')),
                ('active', models.BooleanField(default=True, help_text='Whether the coupon is currently active', verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
                'ordering': ['-valid_from'],
                'indexes': [models.Index(fields=['valid_from', 'valid_to'], name='coupons_cou_valid_f_cf442c_idx')],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CouponTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Coupon code')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Coupon name')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='coupons.coupon')),
            ],
            options={
                'verbose_name': 'Coupon Translation',
                'db_table': 'coupons_coupon_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
