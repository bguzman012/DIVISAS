# Generated by Django 3.2.10 on 2022-12-16 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdivs', '0003_auto_20221216_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='ip_address',
            field=models.CharField(default='', max_length=20),
        ),
    ]
