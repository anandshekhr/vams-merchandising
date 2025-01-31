# Generated by Django 5.0.3 on 2024-06-24 04:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0003_initial'),
        ('sellerorders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerorder',
            name='customer_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='sellerorder',
            name='order_item',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cart.cart', verbose_name='Order Item'),
        ),
    ]
