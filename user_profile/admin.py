from django.contrib import admin
from base.admin import BaseAdmin
from models import *


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdmin):
    fields = ['user',
              'notify_report_accepted',
              'notify_report_rejected',
              'notify_report_commented',
              'notify_report_submitted_for_review',
              'notify_report_saved_enhancedCWEApplication',
              'notify_report_reviewed'
              ]


