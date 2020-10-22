# Generated by Django 3.1.1 on 2020-10-22 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, choices=[('code_institute', 'Code Institute')], default='code_institute', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_display_name', models.CharField(default='', max_length=80)),
                ('user_type', models.CharField(choices=[('', 'Select Post Category'), ('participant', 'Participant'), ('staff', 'Staff'), ('admin', 'Admin')], default='', max_length=20)),
                ('current_lms_module', models.CharField(choices=[('', 'Select Learning Stage'), ('programme_preliminaries', 'Programme Preliminaries'), ('programming_paradigms', 'Programming Paradigms'), ('html_fundamentals', 'HTML Fundamentals'), ('css_fundamentals', 'CSS Fundamentals'), ('user_centric_frontend_development', 'User Centric Frontend Development'), ('javascript_fundamentals', 'Javascript Fundamentals'), ('interactive_frontend_development', 'Interactive Frontend Development'), ('python_fundamentals', 'Python Fundamentals'), ('practical_python', 'Practical Python'), ('data_centric_development', 'Data Centric Development'), ('full_stack_frameworks with django', 'Full Stack Frameworks with Django'), ('alumni', 'Alumni'), ('staff', 'Staff')], default='', max_length=35)),
                ('organisation', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.organisation')),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]