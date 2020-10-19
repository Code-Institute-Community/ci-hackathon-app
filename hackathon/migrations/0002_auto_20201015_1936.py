# Generated by Django 3.1.1 on 2020-10-15 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hackathon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackathon',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hackathon_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='HackAwardCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('display_name', models.CharField(default='', max_length=254)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hackawardcategory_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]