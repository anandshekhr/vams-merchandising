# Generated by Django 4.0.4 on 2023-09-01 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_vendorbankaccountdetail'),
        ('cart', '0003_remove_order_received_remove_order_received_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorTransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50, verbose_name='Order ID')),
                ('order_receiving_date', models.DateField(auto_now=True, verbose_name='Order Received on')),
                ('order_completed_date', models.DateField(verbose_name='Order Completed on')),
                ('total_order_amount', models.FloatField(blank=True, null=True, verbose_name='Total Order Amount')),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled'), ('Transferred', 'Transferred')], default='Pending', max_length=50, verbose_name='Payment Status')),
                ('payment_transfer_date', models.DateField(blank=True, null=True, verbose_name='Payment Transfer Date')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.vendordetail', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'VendorTransactionDetail',
                'verbose_name_plural': 'VendorTransactionDetails',
            },
        ),
        migrations.CreateModel(
            name='VendorOrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50, verbose_name='Order ID')),
                ('order_item', models.CharField(max_length=50, verbose_name='Order Item')),
                ('order_item_size', models.CharField(max_length=50, verbose_name='Order Item Size')),
                ('order_item_qty', models.IntegerField(verbose_name='Order Item Qty')),
                ('order_amount', models.CharField(max_length=50, verbose_name='Order Amount')),
                ('payment_status', models.CharField(max_length=50, verbose_name='Payment Status')),
                ('delivery_address', models.TextField(verbose_name='Delivery Address')),
                ('order_packed', models.CharField(blank=True, max_length=50, null=True, verbose_name='Order Status: Packed')),
                ('order_shipped', models.CharField(blank=True, max_length=50, null=True, verbose_name='Order Status: Shipped')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.vendordetail', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'VendorOrderDetail',
                'verbose_name_plural': 'VendorOrderDetails',
            },
        ),
    ]