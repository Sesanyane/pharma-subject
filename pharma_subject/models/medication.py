from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords

from .protocol import Protocol


class Medication(SiteModelMixin, BaseUuidModel):

    name = models.CharField(max_length=200)

    protocol = models.ForeignKey(Protocol, on_delete=models.PROTECT, )

    storage_instructions = models.TextField(max_length=200)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'pharma_subject'
