# Generated by Django 3.1.1 on 2020-10-25 19:47

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(default='Code Institute', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('slack_display_name', models.CharField(default='', max_length=80)),
                ('user_type', models.CharField(choices=[('', 'Select Post Category'), ('participant', 'Participant'), ('staff', 'Staff'), ('admin', 'Admin')], default='', max_length=20)),
                ('current_lms_module', models.CharField(choices=[('', 'Select Learning Stage'), ('programme_preliminaries', 'Programme Preliminaries'), ('programming_paradigms', 'Programming Paradigms'), ('html_fundamentals', 'HTML Fundamentals'), ('css_fundamentals', 'CSS Fundamentals'), ('user_centric_frontend_development', 'User Centric Frontend Development'), ('javascript_fundamentals', 'Javascript Fundamentals'), ('interactive_frontend_development', 'Interactive Frontend Development'), ('python_fundamentals', 'Python Fundamentals'), ('practical_python', 'Practical Python'), ('data_centric_development', 'Data Centric Development'), ('full_stack_frameworks with django', 'Full Stack Frameworks with Django'), ('alumni', 'Alumni'), ('staff', 'Staff')], default='', max_length=35)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_organisation', to='accounts.organisation')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
