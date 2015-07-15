# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('token', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
    ]
