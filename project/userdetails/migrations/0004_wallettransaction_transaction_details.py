# Generated by Django 5.0.1 on 2024-01-18 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdetails', '0003_remove_wishlist_product_wishlist_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransaction',
            name='transaction_details',
            field=models.CharField(default=None, max_length=20),
        ),
    ]