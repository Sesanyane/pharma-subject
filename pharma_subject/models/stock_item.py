from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords

from .protocol import Protocol
from .stock import Stock


class StockItem(SiteModelMixin, BaseUuidModel):

    drug_name = models.CharField(
        verbose_name='Drug Name',
        max_length=200,
        blank=True,
        null=True)

    code = models.CharField(
        verbose_name='Code',
        max_length=250,
        blank=True,
        null=True,)

    quantity = models.IntegerField(
        default=1,
        blank=False,
        null=False)

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,)

    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.drug_name

    class Meta:
        app_label = 'pharma_subject'
