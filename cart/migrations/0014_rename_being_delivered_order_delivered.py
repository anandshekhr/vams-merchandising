# Generated by Django 4.1.3 on 2023-04-09 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='being_delivered',
            new_name='delivered',
        ),
    ]
