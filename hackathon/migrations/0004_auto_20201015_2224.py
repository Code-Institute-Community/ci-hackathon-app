# Generated by Django 3.1.1 on 2020-10-15 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hackathon', '0003_auto_20201015_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackawardcategory',
            name='hackathon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='hackathon.hackathon'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hackawardcategory',
            name='winning_project',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hackathon.hackproject'),
        ),
        migrations.AddField(
            model_name='hackteam',
            name='hackathon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='hackathon.hackathon'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hackteam',
            name='project',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hackathon.hackproject'),
        ),
        migrations.CreateModel(
            name='HackProjectScoreCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(default='', max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hackprojectscorecategory_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Hack project score categories',
            },
        ),
        migrations.CreateModel(
            name='HackProjectScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hackprojectscore_created_by', to=settings.AUTH_USER_MODEL)),
                ('judge', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='hackathon.hackproject')),
                ('score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.hackprojectscorecategory')),
            ],
        ),
    ]