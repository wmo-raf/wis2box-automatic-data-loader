# Generated by Django 5.1.4 on 2025-01-10 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkconnection',
            name='is_daily_data',
            field=models.BooleanField(default=False, help_text='Check to mark data from this connection as daily data', verbose_name='Is Daily Data'),
        ),
        migrations.AlterField(
            model_name='dispatchchannelparametermapping',
            name='channel_unit',
            field=models.ForeignKey(blank=True, help_text='Unit of the parameter in the channel. Leave empty if the same', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unit', verbose_name='Channel Unit'),
        ),
    ]
