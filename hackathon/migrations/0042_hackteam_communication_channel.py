# Generated by Django 3.1.3 on 2021-03-02 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0041_auto_20210301_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackteam',
            name='communication_channel',
            field=models.CharField(blank=True, default='', help_text='Usually a link to the Slack group IM, but can be a link to something else.', max_length=255),
        ),
    ]