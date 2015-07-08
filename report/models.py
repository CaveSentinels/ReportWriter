from django.db import models
from base.models import BaseModel


STATUS = [('draft', 'Draft'),
          ('in_review', 'In Review'),
          ('approved', 'Approved'),
          ('rejected', 'Rejected')]


RANKING = [('excellent', 'Excellent'),
           ('great', 'Great'),
           ('good', 'Good'),
           ('normal', 'Normal'),
           ('average', 'Average'),
           ('low', 'Low'),
           ('manual', 'Manual')]


class Category(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        # override default permissions to add 'view' permission that give readonly access rights
        #default_permissions = ('add', 'change', 'delete', 'view')

    def __unicode__(self):
        return self.name


class CWE(BaseModel):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "CWE"
        verbose_name_plural = "CWEs"
        # override default permissions to add 'view' permission that give readonly access rights
        #default_permissions = ('add', 'change', 'delete', 'view')

    def __unicode__(self):
        return "CWE-%s: %s" % (self.code, self.name)


class MisuseCase(BaseModel):
    name = models.CharField(max_length=16, null=True, blank=True, db_index=True, default="-")
    misuse_case_id = models.IntegerField(null=True, blank=True)  # ID of the misuse case from the Enhanced CWE System
    misuse_case_description = models.TextField()

    class Meta:
        verbose_name = "Misuse Case"
        verbose_name_plural = "Misuse Cases"


class UseCase(BaseModel):
    name = models.CharField(max_length=16, null=True, blank=True, db_index=True, default="-")
    use_case_id = models.IntegerField(null=True, blank=True)  # ID of the use case from the Enhanced CWE System
    use_case_description = models.TextField()
    osr_description = models.TextField()

    class Meta:
        verbose_name = "Use Case"
        verbose_name_plural = "Use Cases"


class Report(BaseModel):
    name = models.CharField(max_length=16, null=True, blank=True, db_index=True, default="-")
    title = models.CharField(max_length=128, db_index=True)
    description = models.TextField()
    module_name = models.CharField(max_length=128)
    references = models.TextField(null=True, blank=True)
    targets = models.TextField(null=True, blank=True)
    platforms = models.TextField(null=True, blank=True)
    architectures = models.TextField(null=True, blank=True)
    reliability = models.CharField(max_length=128, choices=RANKING, default='normal')
    development = models.TextField(null=True, blank=True)
    #  TODO null = True has to be removed from cwes, misuse_case and use_case
    cwes = models.ManyToManyField(CWE)
    misuse_case = models.ForeignKey(MisuseCase, null=True)
    use_case = models.ForeignKey(UseCase, null=True)
    status = models.CharField(choices=STATUS, max_length=64, default='draft')
    is_generic = models.BooleanField(default=False, db_index=True)
