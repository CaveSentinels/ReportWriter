# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notify_report_accepted', models.BooleanField(default=True)),
                ('notify_report_rejected', models.BooleanField(default=True)),
                ('notify_report_commented', models.BooleanField(default=True)),
                ('notify_report_submitted_for_review', models.BooleanField(default=True)),
                ('notify_report_saved_enhancedCWEApplication', models.BooleanField(default=True)),
                ('notify_report_reviewed', models.BooleanField(default=True)),
                ('notify_report_inappropriate', models.BooleanField(default=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
