# Generated by Django 4.1.3 on 2023-04-07 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_pendingpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(blank=True, default='L', max_length=50, null=True, verbose_name='Item Size'),
        ),
    ]
