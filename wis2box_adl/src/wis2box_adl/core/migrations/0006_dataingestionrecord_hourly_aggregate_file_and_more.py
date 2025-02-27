# Generated by Django 5.0.6 on 2024-10-22 12:56

import django.core.validators
import wis2box_adl.core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_station_wmo_block_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataingestionrecord',
            name='hourly_aggregate_file',
            field=models.FileField(blank=True, null=True, upload_to=wis2box_adl.core.utils.get_station_directory_path),
        ),
        migrations.AddField(
            model_name='dataingestionrecord',
            name='is_hourly_aggregate',
            field=models.BooleanField(default=False, verbose_name='Is Hourly Aggregate'),
        ),
        migrations.AddField(
            model_name='network',
            name='wis2box_hourly_aggregate',
            field=models.BooleanField(default=True, help_text='Check this if you want only one record per hour to be uploaded to wis2box', verbose_name='Enable WIS2BOX Hourly Aggregation'),
        ),
        migrations.AddField(
            model_name='network',
            name='wis2box_hourly_aggregate_strategy',
            field=models.CharField(blank=True, choices=[('latest', 'Latest in the Hour')], default='latest', help_text='Method to use for aggregating hourly data for ingestion to WIS2BOX', max_length=255, null=True, verbose_name='WIS2BOX Hourly Aggregate Strategy'),
        ),
        migrations.AlterField(
            model_name='network',
            name='plugin_processing_enabled',
            field=models.BooleanField(default=True, help_text='If unchecked, the plugin will not run automatically', verbose_name='Plugin Auto Processing Enabled'),
        ),
        migrations.AlterField(
            model_name='network',
            name='plugin_processing_interval',
            field=models.PositiveIntegerField(default=15, help_text='How often the plugin should run, in minutes', validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)], verbose_name='Plugin Auto Processing Interval in Minutes'),
        ),
    ]
