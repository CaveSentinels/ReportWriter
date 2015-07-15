from django.db import models
from django.core.validators import URLValidator
from django.db import models
from solo.models import SingletonModel

class SiteConfiguration(SingletonModel):
    url = models.CharField(validators=[URLValidator()], max_length=2000)
    token = models.CharField(max_length=200)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"

