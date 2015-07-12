# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20150710_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='promoted',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'MUO is promoted to Enhanced CWE System'),
        ),
    ]
