# Generated by Django 4.0.4 on 2023-08-10 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/20230810', verbose_name='Avatar'),
        ),
    ]