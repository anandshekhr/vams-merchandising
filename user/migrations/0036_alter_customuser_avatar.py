# Generated by Django 4.0.4 on 2023-08-11 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/20230811', verbose_name='Avatar'),
        ),
    ]
