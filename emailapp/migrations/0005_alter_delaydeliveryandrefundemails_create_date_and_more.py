# Generated by Django 4.1.3 on 2024-04-24 07:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailapp', '0004_alter_delaydeliveryandrefundemails_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delaydeliveryandrefundemails',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 24, 12, 38, 5, 862464), null=True),
        ),
        migrations.AlterField(
            model_name='paymentsemails',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 24, 12, 38, 5, 862023), null=True),
        ),
        migrations.AlterField(
            model_name='promotionalemails',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 24, 12, 38, 5, 862342), null=True),
        ),
        migrations.AlterField(
            model_name='userregisteredemails',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 24, 12, 38, 5, 862161), null=True),
        ),
    ]