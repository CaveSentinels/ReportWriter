# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='misuse_case',
        ),
        migrations.RemoveField(
            model_name='report',
            name='use_case',
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_assumption',
            field=models.TextField(null=True, verbose_name=b'Assumption', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_description',
            field=models.TextField(null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_flow_of_events',
            field=models.TextField(null=True, verbose_name=b'Flow of events', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_postcondition',
            field=models.TextField(null=True, verbose_name=b'Post-condition', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_precondition',
            field=models.TextField(null=True, verbose_name=b'Pre-condition', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_primary_actor',
            field=models.CharField(max_length=256, null=True, verbose_name=b'Primary actor', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_secondary_actor',
            field=models.CharField(max_length=256, null=True, verbose_name=b'Secondary actor', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='misuse_case_source',
            field=models.TextField(null=True, verbose_name=b'Source', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='osr',
            field=models.TextField(null=True, verbose_name=b'Overlooked Security Requirement', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_assumption',
            field=models.TextField(null=True, verbose_name=b'Assumption', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_description',
            field=models.TextField(null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_flow_of_events',
            field=models.TextField(null=True, verbose_name=b'Flow of events', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_postcondition',
            field=models.TextField(null=True, verbose_name=b'Post-condition', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_precondition',
            field=models.TextField(null=True, verbose_name=b'Pre-condition', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_primary_actor',
            field=models.CharField(max_length=256, null=True, verbose_name=b'Primary actor', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_secondary_actor',
            field=models.CharField(max_length=256, null=True, verbose_name=b'Secondary actor', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='use_case_source',
            field=models.TextField(null=True, verbose_name=b'Source', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(default=b'/', max_length=16, null=True, db_index=True, blank=True),
        ),
    ]
