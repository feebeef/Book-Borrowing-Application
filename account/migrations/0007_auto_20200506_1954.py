# Generated by Django 3.0.3 on 2020-05-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200506_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='idnum',
            field=models.IntegerField(default=0, unique=True, verbose_name='ID Number'),
        ),
    ]
