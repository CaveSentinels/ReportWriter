# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='misusecase',
            name='misuse_case_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='misuse_case',
            field=models.ForeignKey(to='report.MisuseCase', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='use_case',
            field=models.ForeignKey(to='report.UseCase', null=True),
        ),
        migrations.AlterField(
            model_name='usecase',
            name='use_case_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
