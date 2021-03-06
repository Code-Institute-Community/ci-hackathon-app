# Generated by Django 3.1.3 on 2021-01-16 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0026_hackproject_technologies_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackproject',
            name='project_image_url',
            field=models.URLField(blank=True, default='', help_text="URL for an image displayed on the team's page next to the project information."),
        ),
        migrations.AddField(
            model_name='hackproject',
            name='screenshot_image_url',
            field=models.URLField(blank=True, default='', help_text="URL for a project screenshot displayed on the team's page underneath the project information"),
        ),
        migrations.AddField(
            model_name='hackteam',
            name='header_image_url',
            field=models.URLField(blank=True, default='', help_text="URL for a header image displayed at the top of the team's page"),
        ),
    ]
