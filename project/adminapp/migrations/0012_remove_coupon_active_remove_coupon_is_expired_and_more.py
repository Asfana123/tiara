# Generated by Django 5.0.1 on 2024-01-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0011_coupon_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='active',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='is_expired',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='type',
        ),
        migrations.AlterField(
            model_name='categoryoffer',
            name='discount_prcnt',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='dis_per',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='minimum_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='discount_prcnt',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='variant',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
