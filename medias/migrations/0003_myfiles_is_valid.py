# Generated by Django 4.0.5 on 2022-07-15 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_myfiles_reg_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfiles',
            name='is_valid',
            field=models.BooleanField(default=True, verbose_name='인증 완료됨'),
        ),
    ]
