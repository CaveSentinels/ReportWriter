# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CWE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('code', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'CWE',
                'verbose_name_plural': 'CWEs',
            },
        ),
        migrations.CreateModel(
            name='MisuseCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('name', models.CharField(default=b'-', max_length=16, null=True, db_index=True, blank=True)),
                ('misuse_case_id', models.IntegerField()),
                ('misuse_case_description', models.TextField()),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Misuse Case',
                'verbose_name_plural': 'Misuse Cases',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('name', models.CharField(default=b'-', max_length=16, null=True, db_index=True, blank=True)),
                ('title', models.CharField(max_length=128, db_index=True)),
                ('description', models.TextField()),
                ('module_name', models.CharField(max_length=128)),
                ('references', models.TextField(null=True, blank=True)),
                ('targets', models.TextField(null=True, blank=True)),
                ('platforms', models.TextField(null=True, blank=True)),
                ('architectures', models.TextField(null=True, blank=True)),
                ('reliability', models.CharField(default=b'normal', max_length=128, choices=[(b'excellent', b'Excellent'), (b'great', b'Great'), (b'good', b'Good'), (b'normal', b'Normal'), (b'average', b'Average'), (b'low', b'Low'), (b'manual', b'Manual')])),
                ('development', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'draft', max_length=64, choices=[(b'draft', b'Draft'), (b'in_review', b'In Review'), (b'approved', b'Approved'), (b'rejected', b'Rejected')])),
                ('is_generic', models.BooleanField(default=False, db_index=True)),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('cwes', models.ManyToManyField(to='report.CWE')),
                ('misuse_case', models.ForeignKey(to='report.MisuseCase')),
                ('modified_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UseCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('name', models.CharField(default=b'-', max_length=16, null=True, db_index=True, blank=True)),
                ('use_case_id', models.IntegerField()),
                ('use_case_description', models.TextField()),
                ('osr_description', models.TextField()),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Use Case',
                'verbose_name_plural': 'Use Cases',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='use_case',
            field=models.ForeignKey(to='report.UseCase'),
        ),
    ]
