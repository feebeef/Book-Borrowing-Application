# Generated by Django 3.0.3 on 2020-05-05 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20200505_2109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookreservation',
            options={'ordering': ['-date_reservation']},
        ),
    ]
