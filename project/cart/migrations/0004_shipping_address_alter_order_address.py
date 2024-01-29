# Generated by Django 5.0.1 on 2024-01-15 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_order_products_remove_orderitem_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping_address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('phone_No', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='cart.address'),
        ),
    ]