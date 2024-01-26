# Generated by Django 5.0.1 on 2024-01-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0015_rename_discount_prcnt_categoryoffer_discount_prcntg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryoffer',
            name='discount_prcntg',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='minimum_amount',
        ),
        migrations.AddField(
            model_name='categoryoffer',
            name='discount_prcnt',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coupon',
            name='dis_per',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='discount_prcnt',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='variant',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
