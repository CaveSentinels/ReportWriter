from django.dispatch import receiver
from report.signals import *
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from user_profile.models import *
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from report.models import *
from django_comments.signals import comment_was_posted
import constants


"""
All of these methods are the handlers for the signals defined in signals.py in the
Report Writing Application.
They create the email body by fetching the parameters and send the email
"""

# This method will send an email when a Report gets accepted
@receiver(report_accepted)
def on_report_accepted(sender, instance, **kwargs):
    if instance.created_by and instance.created_by.profile.notify_report_accepted:
        subject = constants.REPORT_ACCEPTED_SUBJECT
        action = constants.ACCEPTED
        notify_owner(instance, subject, action)

    report_type = ContentType.objects.get(app_label='report', model='report')
    # First filter the permission which has to be checked from the list of permission in the report
    perm = Permission.objects.filter(codename__in=('can_approve', 'can_reject'), content_type = report_type)
    # The user might have the permission either as a user or in a group of which he is a part, so check both
    users = User.objects.filter(profile__notify_report_submitted_for_review=True)\
                        .filter(Q(groups__permissions__in=perm) | Q(user_permissions__in=perm))
    emails = [user.email for user in users]
    subject = constants.REPORT_APPROVED_SUBJECT
    action = constants.APPROVED
    notify_reviewers(instance, subject, action, emails)

# This method will send an email when a Report gets rejected
@receiver(report_rejected)
def on_report_rejected(sender, instance, **kwargs):
    if instance.created_by and instance.created_by.profile.notify_report_rejected:
        subject = constants.REPORT_REJECTED_SUBJECT
        action = constants.REJECTED
        notify_owner(instance, subject, action)

# This method will send an email when a Report is marked as inappropriate/duplicate
@receiver(report_inappropriate)
def on_report_inappropriate(sender, instance, **kwargs):
    if instance.created_by and instance.created_by.profile.notify_report_inappropriate:
        subject = constants.REPORT_INAPPROPRIATE_SUBJECT
        action = constants.INAPPROPRIATE
        notify_owner(instance, subject, action)


@receiver(report_submitted_review)
def on_report_submitted_for_review(sender,instance, **kwargs):
    report_type = ContentType.objects.get(app_label='report', model='report')
    # First filter the permission which has to be checked from the list of permission in the report
    perm = Permission.objects.filter(codename__in=('can_approve', 'can_reject'), content_type = report_type)
    # The user might have the permission either as a user or in a group of which he is a part, so check both
    users = User.objects.filter(profile__notify_report_submitted_for_review=True)\
                        .filter(Q(groups__permissions__in=perm) | Q(user_permissions__in=perm))
    emails = [user.email for user in users]
    subject = constants.REPORT_SUBMITTED_FOR_REVIEW_SUBJECT
    action = constants.SUBMITTED
    notify_reviewers(instance, subject, action, emails)


# This method will send an email when the Report is commented upon
@receiver(comment_was_posted)
def on_muo_commented(sender, comment, request, **kwargs):
    if comment.content_type == ContentType.objects.get_for_model(Report):
        instance = comment.content_object
        if instance.created_by and instance.created_by.profile.notify_muo_commented:
            subject = constants.REPORT_COMMENTED_SUBJECT
            action = constants.COMMENTED
            notify_owner(instance, subject, action)

@receiver(report_saved_enhancedCWEApplication)
def on_report_saved(sender,instance, **kwargs):
    """
    TODO Handler will be written when this user story is implemented
    """

"""
This method is called when we have to send the email after fixing all the parameters
"""
def notify_owner(instance, subject, action):
    user = instance.created_by
    report_name = instance.name
    send_mail(subject, get_template('emailer/report_action.html').render(
        Context({
            'full_name': user.get_full_name() or user.username,
            'report_name': report_name,
            'action': action,
        })
    ), constants.SENDER_EMAIL, [user.email], fail_silently=True)

"""
This method is called when we have to send bulk email to many recipients
"""
def notify_reviewers(instance, subject, action, emails):
    if emails:
        send_mail(subject, get_template('emailer/report_action_bulk.html').render(
            Context({
                'report_name': instance.name,
                'action': action,
                })
            ), constants.SENDER_EMAIL, emails, fail_silently=True)














