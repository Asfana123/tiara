# Generated by Django 4.2.7 on 2024-01-04 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='type',
            field=models.CharField(choices=[(1, 'First Order'), (2, 'Purchase Above 1000'), (3, 'Purchase Above 2000')], max_length=20),
        ),
    ]
