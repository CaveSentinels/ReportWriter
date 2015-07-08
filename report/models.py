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

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=Report, dispatch_uid='report_post_save_signal')
def post_save_report(sender, instance, created, using, **kwargs):
    """ Set the value of the field 'name' after creating the object """
    if created:
        instance.name = "Report-{0:05d}".format(instance.id)
        instance.save()