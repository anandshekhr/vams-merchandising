# Generated by Django 5.0.3 on 2024-06-24 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryPartnerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'DeliveryPartnerDetail',
                'verbose_name_plural': 'DeliveryPartnerDetails',
            },
        ),
        migrations.CreateModel(
            name='PincodeDetail',
            fields=[
                ('pincode', models.IntegerField(primary_key=True, serialize=False, verbose_name='Pincode')),
                ('locality', models.CharField(blank=True, max_length=500, null=True, verbose_name='Locality')),
                ('city', models.CharField(blank=True, max_length=500, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=500, null=True, verbose_name='State')),
                ('can_deliver_here', models.BooleanField(default=True, verbose_name='Can Deliver Here')),
                ('can_pickup', models.BooleanField(default=True, verbose_name='Can Pick Up')),
                ('is_fraud_detected', models.BooleanField(default=False, verbose_name='Fraud Detection')),
                ('is_blocked', models.BooleanField(default=False, verbose_name='Blocked')),
                ('min_days_to_deliver', models.IntegerField(default=4, verbose_name='Min Days to Deliver')),
                ('max_days_to_deliver', models.IntegerField(default=14, verbose_name='Max Days to Deliver')),
                ('usual_days_to_deliver', models.IntegerField(default=7, verbose_name='usual Days to Deliver')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Remarks')),
                ('delivery_partners', models.ManyToManyField(to='delivery.deliverypartnerdetail')),
            ],
            options={
                'verbose_name': 'PincodeDetail',
                'verbose_name_plural': 'PincodeDetails',
            },
        ),
    ]
