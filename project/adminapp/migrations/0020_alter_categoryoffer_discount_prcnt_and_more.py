# Generated by Django 5.0.1 on 2024-01-25 04:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0019_alter_categoryoffer_discount_prcnt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='discount_prcnt',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='discount_prcnt',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]