# Generated by Django 2.2.4 on 2020-11-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonexam_app', '0002_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='start_date',
            field=models.DateField(),
        ),
    ]
