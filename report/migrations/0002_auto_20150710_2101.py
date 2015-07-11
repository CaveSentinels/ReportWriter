# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'Report', 'verbose_name_plural': 'Reports', 'permissions': (('can_approve', 'Can approve Report'), ('can_reject', 'Can reject Report'), ('can_edit_all', 'Can edit all Report'), ('can_view_all', 'Can view all Report'))},
        ),
        migrations.RemoveField(
            model_name='report',
            name='promoted',
        ),
    ]
