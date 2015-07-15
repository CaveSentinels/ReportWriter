from django.db import models
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from signals import *


STATUS = [('draft', 'Draft'),
          ('in_review', 'In Review'),
          ('approved', 'Approved'),
          ('rejected', 'Rejected')]


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
    name = models.CharField(max_length=16, null=True, blank=True, db_index=True, default="-")
    title = models.CharField(max_length=128, db_index=True)
    description = models.TextField()
    cwes = models.ManyToManyField(CWE)
    misuse_case_id = models.IntegerField(null=True, blank=True)
    misuse_case = models.TextField(null=True, blank=True)
    use_case_id = models.IntegerField(null=True, blank=True)
    use_case = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=64, default='draft')
    promoted = models.BooleanField("MUO is promoted to Enhanced CWE System", default=False, db_index=True)


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
            self.reject_reason = reject_reason
            self.reviewed_by = reviewer
            self.save()
            # Send email
            report_rejected.send(sender=self, instance=self)

        else:
            raise ValueError("In order to approve an Report, it should be in 'in-review' state")

@receiver(post_save, sender=Report, dispatch_uid='report_post_save_signal')
def post_save_report(sender, instance, created, using, **kwargs):
    """ Set the value of the field 'name' after creating the object """
    if created:
        instance.name = "Report-{0:05d}".format(instance.id)
        instance.save()