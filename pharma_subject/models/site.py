from django.db import models
from django.core.validators import RegexValidator

from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_validators import TelephoneNumber

from .protocol import Protocol


class Site(SiteModelMixin, BaseUuidModel):

    protocol = models.ForeignKey(
        Protocol, on_delete=models.PROTECT, related_name='sites')

    name = models.CharField(
        max_length=25)

    site_code = models.CharField(
        max_length=20,
        validators=[RegexValidator('[\d]+', 'Invalid format.')])

    telephone_number = models.CharField(
        max_length=7,
        validators=[TelephoneNumber, ],)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.site_code}, Protocol: {self.protocol.name}'

    class Meta:
        app_label = 'pharma_subject'
