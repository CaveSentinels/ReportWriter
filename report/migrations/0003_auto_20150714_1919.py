# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20150714_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='cwes',
            field=models.ManyToManyField(to='report.CWE', blank=True),
        ),
    ]
