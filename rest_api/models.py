from django.db import models
from django.core.validators import URLValidator
from solo.models import SingletonModel

class RESTConfiguration(SingletonModel):
    url = models.CharField(validators=[URLValidator()], max_length=255)
    token = models.CharField(max_length=255)

    def __unicode__(self):
        return u"REST Configuration"

    class Meta:
        verbose_name = "REST Configuration"

