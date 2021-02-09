# Generated by Django 3.1.1 on 2020-10-20 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hackathon', '0010_merge_20201020_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackproject',
            name='created_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='hackprojects', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hackproject',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hackproject_mentor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hackprojectscore',
            name='created_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='hackprojectscores', to=settings.AUTH_USER_MODEL),
        ),
    ]
