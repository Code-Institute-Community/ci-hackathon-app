# Generated by Django 3.1.13 on 2024-10-08 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0054_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='isReadOnly',
        ),
    ]
