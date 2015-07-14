from django.db import models
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    name = models.CharField(max_length=16, null=True, blank=True, db_index=True, default="/")
    title = models.CharField(max_length=128, db_index=True)
    description = models.TextField()
    cwes = models.ManyToManyField(CWE)

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
    promoted = models.BooleanField("MUO is promoted to Enhanced CWE System", default=False, db_index=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=Report, dispatch_uid='report_post_save_signal')
def post_save_report(sender, instance, created, using, **kwargs):
    """ Set the value of the field 'name' after creating the object """
    if created:
        instance.name = "Report-{0:05d}".format(instance.id)
        instance.save()