from base.models import BaseModel
from signals import *
from django.db import models
from django.conf import settings
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

STATUS = [('draft', 'Draft'),
          ('in_review', 'In Review'),
          ('approved', 'Approved'),
          ('rejected', 'Rejected')]

MUO_STATUS = [('custom', 'Custom'), ('generic', 'Generic')]

class CWE(BaseModel):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "CWE"
        verbose_name_plural = "CWEs"

    def __unicode__(self):
        return "CWE-%s: %s" % (self.code, self.name)



class Report(BaseModel):
    name = models.CharField(max_length=16, null=True, blank=True, db_index=True, default="/")
    title = models.CharField(max_length=128, db_index=True)
    description = models.TextField()
    cwes = models.ManyToManyField(CWE, blank=True)

    misuse_case_id = models.IntegerField(null=True, blank=True)
    misuse_case_description = models.TextField(null=True, blank=True, verbose_name="Description")
    misuse_case_primary_actor = models.CharField(max_length=256, null=True, blank=True, verbose_name="Primary actor")
    misuse_case_secondary_actor = models.CharField(max_length=256, null=True, blank=True, verbose_name="Secondary actor")
    misuse_case_precondition = models.TextField(null=True, blank=True, verbose_name="Pre-condition")
    misuse_case_flow_of_events = models.TextField(null=True, blank=True, verbose_name="Flow of events")
    misuse_case_postcondition = models.TextField(null=True, blank=True, verbose_name="Post-condition")
    misuse_case_assumption = models.TextField(null=True, blank=True, verbose_name="Assumption")
    misuse_case_source = models.TextField(null=True, blank=True, verbose_name="Source")

    use_case_id = models.IntegerField(null=True, blank=True)
    use_case_description = models.TextField(null=True, blank=True, verbose_name="Description")
    use_case_primary_actor = models.CharField(max_length=256, null=True, blank=True, verbose_name="Primary actor")
    use_case_secondary_actor = models.CharField(max_length=256, null=True, blank=True, verbose_name="Secondary actor")
    use_case_precondition = models.TextField(null=True, blank=True, verbose_name="Pre-condition")
    use_case_flow_of_events = models.TextField(null=True, blank=True, verbose_name="Flow of events")
    use_case_postcondition = models.TextField(null=True, blank=True, verbose_name="Post-condition")
    use_case_assumption = models.TextField(null=True, blank=True, verbose_name="Assumption")
    use_case_source = models.TextField(null=True, blank=True, verbose_name="Source")

    osr = models.TextField(null=True, blank=True, verbose_name="Overlooked Security Requirement")

    status = models.CharField(choices=STATUS, max_length=64, default='draft')
    custom = models.CharField(max_length=16, null=True, blank=True)
    promoted = models.BooleanField("MUO is promoted to Enhanced CWE System", default=False, db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)


    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        # additional permissions
        permissions = (
            ('can_approve', 'Can approve Report'),
            ('can_reject', 'Can reject Report'),
            ('can_edit_all', 'Can edit all Report'),
            ('can_view_all', 'Can view all Report'),
        )


    def __unicode__(self):
        return self.name

    def action_submit(self):
        """
        This method change the status of the Report object to 'in_review'. This change
        # is allowed only if the current status is 'draft'. If the current status is not
        # 'draft', it raises the ValueError with appropriate message.
        """
        if self.status == 'draft':
            self.status = 'in_review'
            self.save()
            # Send email
            report_submitted_review.send(sender=self, instance=self)

        else:
            raise ValueError("You can only submit the report for review if it is 'draft' state")


    def action_approve(self, reviewer=None):
        """
        This method change the status of the Report object to 'approved'.This change
        is allowed only if the current status is 'in_review'. If the current status is not
        'in_review', it raises the ValueError with appropriate message.
        :param reviewer: User object that approved the Report
        :raise ValueError: if status not in 'in-review'
        """
        if self.status == 'in_review':
            self.status = 'approved'
            self.is_published = True
            self.reviewed_by = reviewer
            self.save()
            # Send email
            report_accepted.send(sender=self, instance=self)

        else:
            raise ValueError("In order to approve an Report, it should be in 'in-review' state")

    def action_save_in_draft(self):
        """
        This method change the status of the MUOContainer object to 'draft'. This change
        # is allowed only if the current status is 'rejected' or 'in_review'. If the current
        # status is not 'rejected' or 'in_review', it raises the ValueError with
        # appropriate message.
        """
        if self.status == 'rejected' or self.status == 'in_review':
            self.status = 'draft'
            self.save()
        else:
            raise ValueError("A report can only be moved back to draft state if it is either rejected or 'in-review' state")

    def action_reject(self, reject_reason, reviewer=None):
        """
        This method change the status of the report object to 'rejected'
        This change is allowed only if the current status is 'in_review' or 'approved'.
        If the current status is not 'in-review' or 'approved', it raises the ValueError
        with appropriate message.
        :param reject_reason: Message that contain the rejection reason provided by the reviewer
        :param reviewer: User object that approved the Report
        :raise ValueError: if status not in 'in-review'
        """
        if self.status == 'in_review' or self.status == 'approved':
            self.status = 'rejected'
            self.is_published = False
            self.reject_reason = reject_reason
            self.reviewed_by = reviewer
            self.save()
            # Send email
            report_rejected.send(sender=self, instance=self)

        else:
            raise ValueError("In order to approve an Report, it should be in 'in-review' state")

    def action_set_publish(self, should_publish):
        '''
        This method change the published status of the report as per the passed boolean variable value.
        :param should_publish: Publish status to be set on the report
        :return: Null
        '''
        if self.status == 'approved':
            if self.is_published != should_publish:
                self.is_published = should_publish
                self.save()

        else:
            raise ValueError("Report can only be published/unpublished if it is in approved state.")


class ReportQuerySet(models.QuerySet):
    """
    Define custom methods for the Report QuerySet
    """
    def approved(self):
        from django.db.models import Q

        # Returns the queryset for all the approved Report
        if self.model == Report:
            return self.filter(Q(status='approved') | Q(is_published=True))

    def rejected(self):
        # Returns the queryset for all the rejected Report
        if self.model == Report:
            return self.filter(status='rejected')

    def draft(self):
        # Returns the queryset for all the draft Report
        if self.model == Report:
            return self.filter(status='draft')

    def in_review(self):
        # Returns the queryset for all the in review Report
        if self.model == Report:
            return self.filter(status='in_review')

    def custom(self):
        # Returns the queryset for all the custom Report
        if self.model == Report:
            return self.filter(is_custom=True)

    def published(self):
        # Returns the queryset for all the published Report
        if self.model == Report:
            return self.filter(is_published=True)

    def unpublished(self):
        # Returns the queryset for all the unpublished Report
        if self.model == Report:
            return self.filter(is_published=False)


class ReportManager(models.Manager):
    """
    Define custom methods that can be called on the Report
    """

    def get_queryset(self):
        return ReportQuerySet(self.model, using=self._db)

    def approved(self):
        return self.get_queryset().approved()

    def draft(self):
        return self.get_queryset().draft()

    def rejected(self):
        return self.get_queryset().rejected()

    def in_review(self):
        return self.get_queryset().in_review()

    def custom(self):
        return self.get_queryset().custom()



@receiver(post_save, sender=Report, dispatch_uid='report_post_save_signal')
def post_save_report(sender, instance, created, using, **kwargs):
    """ Set the value of the field 'name' after creating the object """
    if created:
        instance.name = "Report-{0:05d}".format(instance.id)
        instance.save()


STATUS = [('draft', 'Draft'),
          ('in_review', 'In Review'),
          ('approved', 'Approved'),
          ('rejected', 'Rejected')]

ISSUE_TYPES = [('incorrect', 'Incorrect Content'),
                ('spam', 'Spam'),
                ('duplicate', 'Duplicate')]

ISSUE_STATUS = [('open', 'Open'),
                 ('investigating', 'Investigating'),
                ('reopened','Re-opened'),
                 ('resolved', 'Resolved')]


class IssueReport(BaseModel):
    name = models.CharField(max_length=16, null=True, blank=True, db_index=True, default="/")
    description = models.TextField(null=True, blank=True)
    type = models.CharField(choices=ISSUE_TYPES, max_length=64)
    status = models.CharField(choices=ISSUE_STATUS, max_length=64, db_index=True, default='open')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='issue_reports')
    report_duplicate = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True)
    resolve_reason = models.TextField(null=True, blank=True, default="/")

    class Meta:
        verbose_name = "Issue Report"
        verbose_name_plural = "Issue Reports"

    def __unicode__(self):
        return self.name

    def action_investigate(self, reviewer= None):
        """
        This method change the status of the issue report object to 'investigating' and This change
        is allowed only if the current status is either open or re open.
        """
        if self.status in ('open','reopened'):
            self.status = 'investigating'
            self.reviewed_at = timezone.now()
            self.reviewed_by = reviewer
            self.save()

        else:
            raise ValueError("In order to investigate a report, it should be in open or re-open state")

    def action_resolve(self, resolve_reason, reviewer= None):
        """
        This method change the status of the issue report object to 'resolved' and This change
        is allowed only if the current status is 'investigating'.
        """
        if self.status == 'investigating':
            self.status = 'resolved'
            # Get the current date when it got resolved
            # TODO: This has to be used in future
            self.reviewed_by = reviewer
            self.reviewed_at = timezone.now()
            self.resolve_reason = resolve_reason
            self.save()
        else:
            raise ValueError("In order to resolve a report, it should be in investigating state")

    def action_reopen(self, reviewer=None):
        """
        This method change the status of the issue report object to 're open' and This change
        is allowed only if the current status is 'investigating' or 'resolved'.
        """
        if self.status == 'resolved':
            self.status = 'reopened'
            self.reviewed_by = reviewer
            self.reviewed_at = timezone.now()
            self.save()
        else:
            raise ValueError("In order to re open an issue it should be in resolved state")

    def action_open(self,reviewer= None):
        """
        This method change the status of the issue report object to 'open' and This change
        is allowed only if the current status is 'investigating'.
        """
        if self.status == 'investigating':
            self.status = 'open'
            self.reviewed_at = timezone.now()
            self.reviewed_by = reviewer
            self.save()
        else:
            raise ValueError("In order to open an issue it should be in open state")


@receiver(post_save, sender=IssueReport, dispatch_uid='issue_report_post_save_signal')
def post_save_issue_report(sender, instance, created, using, **kwargs):
    """ Set the value of the field 'name' after creating the object """
    if created:
        instance.name = "Issue/{0:05d}".format(instance.id)
        instance.save()
