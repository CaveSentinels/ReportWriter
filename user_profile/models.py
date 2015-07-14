from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="profile")
    notify_report_accepted = models.BooleanField(default=True)
    notify_report_rejected = models.BooleanField(default=True)
    notify_report_commented = models.BooleanField(default=True)
    notify_report_submitted_for_review = models.BooleanField(default=True)
    notify_report_saved_enhancedCWEApplication = models.BooleanField(default=True)
    notify_report_reviewed = models.BooleanField(default=True)
    notify_report_inappropriate = models.BooleanField(default=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


