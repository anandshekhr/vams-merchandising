# Generated by Django 4.1.3 on 2024-02-21 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sellerorders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerorder',
            name='customer_info',
        ),
        migrations.RemoveField(
            model_name='sellerorder',
            name='items',
        ),
        migrations.AddField(
            model_name='sellerorder',
            name='billing_address',
            field=models.TextField(default='', max_length=1000, verbose_name='Billing Address'),
        ),
        migrations.AddField(
            model_name='sellerorder',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Order Created at'),
        ),
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
        migrations.AddField(
            model_name='sellerorder',
            name='shipping_address',
            field=models.TextField(default='', max_length=1000, verbose_name='Shipping Address'),
        ),
    ]