# Generated by Django 3.0.3 on 2020-05-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200506_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookreservation',
            name='date_returned',
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='due_back',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
    ]