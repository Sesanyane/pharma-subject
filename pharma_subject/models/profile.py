from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin


class Profile(SiteModelMixin, BaseUuidModel):

    user = models.OneToOneField(User, on_delete=models.PROTECT)

    initials = models.CharField(
        max_length=4,
        validators=[RegexValidator(r'^[A-Z]{2,4}$', message='Use CAPS, 2-4 letters')],)

    class Meta:
        app_label = 'pharma_subject'
