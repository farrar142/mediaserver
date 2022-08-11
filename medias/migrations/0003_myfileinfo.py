# Generated by Django 3.2.13 on 2022-05-01 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_auto_20220501_0430'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyFileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='파일이름')),
                ('size', models.IntegerField(verbose_name='파일사이즈')),
                ('key', models.CharField(max_length=128, verbose_name='파일 키')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medias.myfiles')),
            ],
        ),
    ]