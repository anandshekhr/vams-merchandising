# Generated by Django 3.2.5 on 2023-10-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('size', models.CharField(blank=True, default='L', max_length=50, null=True, verbose_name='Item Size')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name_plural': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryPartnerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Courier Partner Name')),
                ('address', models.CharField(max_length=2000, verbose_name='Courier Partner Address')),
                ('contact_no', models.CharField(max_length=50, verbose_name='Courier Partner Contact No')),
                ('customer_care', models.CharField(max_length=50, verbose_name='Courier Partner Customer Care')),
                ('toll_free_number', models.CharField(max_length=50, verbose_name='Courier Partner Toll Free Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Courier Partner Email')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(blank=True, max_length=200, null=True)),
                ('tracking_id', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='Addition to cart date')),
                ('shipping_address', models.CharField(blank=True, max_length=250, null=True, verbose_name='shipping_address')),
                ('billing_address', models.CharField(blank=True, max_length=250, null=True, verbose_name='billing_address')),
                ('orderNote', models.CharField(blank=True, max_length=250, null=True, verbose_name='Order Note')),
                ('status', models.CharField(blank=True, choices=[('Shipped', 'SHIPPED'), ('Ordered', 'ORDERED'), ('In-transit', 'IN TRANSIT'), ('Out-For-Delivery', 'OUT FOR DELIVERY'), ('Delivered', 'DELIVERED'), ('Refund Requested', 'REFUND REQUESTED'), ('Refunded', 'REFUNDED')], default='ordered', max_length=255, null=True, verbose_name='Order Status')),
                ('ordered', models.BooleanField(default=False)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('shipped', models.BooleanField(default=False)),
                ('shipped_date', models.DateTimeField(auto_now_add=True)),
                ('out_for_delivery', models.BooleanField(default=False)),
                ('out_for_delivery_date', models.DateTimeField(auto_now_add=True)),
                ('delivered', models.BooleanField(default=False)),
                ('delivered_date', models.DateTimeField(auto_now_add=True)),
                ('refund_requested', models.BooleanField(default=False)),
                ('refund_requested_date', models.DateTimeField(auto_now_add=True)),
                ('refund_granted', models.BooleanField(default=False)),
                ('refund_granted_date', models.DateTimeField(auto_now_add=True)),
                ('refund_request_cancelled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instamojo_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendingPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Order ID')),
                ('order_payment_id', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Payment ID')),
                ('phone', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Buyer Phone Number')),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True, verbose_name='Buyer Email')),
                ('buyer_name', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Buyer Name')),
                ('amount', models.FloatField()),
                ('purpose', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Buyer Payment Purpose')),
                ('status', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Payment Status')),
                ('api_response', models.CharField(blank=True, default='', max_length=5000, null=True, verbose_name='Payment API Response')),
                ('created_at', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Payment Created At')),
                ('modified_at', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Payment Modified At')),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sid', models.CharField(default='', max_length=50, verbose_name='Order Reference Id')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_account_number', models.CharField(max_length=100, verbose_name='Bank Account No.')),
                ('ifsc_code', models.CharField(max_length=50, verbose_name='IFSC Code')),
                ('account_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Account Holder Name')),
                ('nick_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nick Name')),
            ],
            options={
                'verbose_name': 'UserBankAccount',
                'verbose_name_plural': 'UserBankAccounts',
            },
        ),
        migrations.CreateModel(
            name='VendorOrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50, verbose_name='Order ID')),
                ('order_item_size', models.CharField(max_length=50, verbose_name='Order Item Size')),
                ('order_item_qty', models.IntegerField(verbose_name='Order Item Qty')),
                ('order_amount', models.CharField(max_length=50, verbose_name='Order Amount')),
                ('payment_status', models.CharField(max_length=50, verbose_name='Payment Status')),
                ('delivery_address', models.TextField(verbose_name='Delivery Address')),
                ('order_packed', models.CharField(blank=True, max_length=50, null=True, verbose_name='Order Status: Packed')),
                ('order_shipped', models.CharField(blank=True, max_length=50, null=True, verbose_name='Order Status: Shipped')),
            ],
            options={
                'verbose_name': 'VendorOrderDetail',
                'verbose_name_plural': 'VendorOrderDetails',
            },
        ),
        migrations.CreateModel(
            name='VendorTransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50, verbose_name='Order ID')),
                ('order_receiving_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Order Received on')),
                ('order_completed_date', models.DateTimeField(blank=True, null=True, verbose_name='Order Completed on')),
                ('total_order_amount', models.FloatField(blank=True, null=True, verbose_name='Total Order Amount')),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled'), ('Transferred', 'Transferred')], default='Pending', max_length=50, verbose_name='Payment Status')),
                ('payment_transfer_date', models.DateField(blank=True, null=True, verbose_name='Payment Transfer Date')),
            ],
            options={
                'verbose_name': 'VendorTransactionDetail',
                'verbose_name_plural': 'VendorTransactionDetails',
            },
        ),
    ]
