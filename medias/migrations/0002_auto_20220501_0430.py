# Generated by Django 3.2.13 on 2022-05-01 04:30

from django.db import migrations, models
import medias.models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfiles',
            name='origin',
            field=models.CharField(default='default', max_length=100, verbose_name='출처'),
        ),
        migrations.AlterField(
            model_name='myfiles',
            name='file',
            field=models.FileField(null=True, upload_to=medias.models.save_directory),
        ),
    ]
