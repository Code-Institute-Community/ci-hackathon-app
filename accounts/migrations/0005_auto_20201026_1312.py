# Generated by Django 3.1.1 on 2020-10-26 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_merge_20201025_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(default='Code Institute', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_organisation', to='accounts.organisation'),
        ),
    ]
