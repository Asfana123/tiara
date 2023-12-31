# Generated by Django 4.2.7 on 2024-01-02 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('dis_per', models.IntegerField()),
                ('is_expired', models.BooleanField(default=False)),
                ('minimum_amount', models.IntegerField(default=100)),
                ('type', models.CharField(choices=[('first_order', 'First Order'), ('purchase_above_1000', 'Purchase Above 1000'), ('purchase_above_2000', 'Purchase Above 2000')], max_length=20)),
            ],
        ),
    ]
