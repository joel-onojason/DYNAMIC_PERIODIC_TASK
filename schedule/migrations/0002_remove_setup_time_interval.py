# Generated by Django 3.2.12 on 2023-01-17 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setup',
            name='time_interval',
        ),
    ]
