# Generated by Django 5.0.3 on 2024-06-24 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ifscCodeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=500, verbose_name='Bank')),
                ('ifsc', models.CharField(max_length=50, verbose_name='IFSC')),
                ('micr', models.CharField(blank=True, max_length=50, null=True, verbose_name='MICR Code')),
                ('branch', models.CharField(blank=True, max_length=100, null=True, verbose_name='Branch')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('city1', models.CharField(blank=True, max_length=50, null=True, verbose_name='City1')),
                ('city2', models.CharField(blank=True, max_length=50, null=True, verbose_name='City2')),
                ('state', models.CharField(blank=True, max_length=100, null=True, verbose_name='State')),
                ('std_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Std Code')),
                ('contact', models.CharField(blank=True, max_length=50, null=True, verbose_name='Contact')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified Date')),
                ('bank_code', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Bank Code')),
                ('rtgs', models.BooleanField(default=True, verbose_name='RTGS')),
            ],
            options={
                'verbose_name': 'ifscCodeDetail',
                'verbose_name_plural': 'ifscCodeDetails',
            },
        ),
    ]
