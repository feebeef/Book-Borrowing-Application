# Generated by Django 3.0.3 on 2020-05-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200506_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='id_num',
        ),
        migrations.AddField(
            model_name='account',
            name='idnum',
            field=models.IntegerField(default=0, verbose_name='ID Number'),
            preserve_default=False,
        ),
    ]
