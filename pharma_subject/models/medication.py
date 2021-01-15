from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords

from .protocol import Protocol
from .stock import Stock


class Medication(SiteModelMixin, BaseUuidModel):

    name = models.CharField(max_length=200,
                            blank=True,
                            null=True)

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,)

    storage_instructions = models.TextField(
        max_length=200)

#     quantity = models.IntegerField(
#         default=1,
#         blank=False,
#         null=False)

#     stock = models.ForeignKey(
#         Stock,
#         on_delete=models.PROTECT)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'pharma_subject'
