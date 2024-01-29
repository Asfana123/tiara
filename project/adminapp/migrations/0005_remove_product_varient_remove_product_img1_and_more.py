# Generated by Django 5.0.1 on 2024-01-13 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_alter_coupon_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='varient',
        ),
        migrations.RemoveField(
            model_name='product',
            name='img1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='img2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='img3',
        ),
        migrations.RemoveField(
            model_name='product',
            name='img4',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(default='None', max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('stock', models.IntegerField(default=0)),
                ('img1', models.ImageField(blank=True, upload_to='product_images')),
                ('img2', models.ImageField(blank=True, upload_to='product_images')),
                ('img3', models.ImageField(blank=True, upload_to='product_images')),
                ('img4', models.ImageField(blank=True, upload_to='product_images')),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.product')),
            ],
        ),
        migrations.DeleteModel(
            name='Varient_color',
        ),
    ]