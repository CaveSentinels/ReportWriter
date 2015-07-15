# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='url',
            field=models.CharField(max_length=2000, validators=[django.core.validators.URLValidator()]),
        ),
    ]
