from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords

from .drug import Drug
from .protocol import Protocol
from .supplier import Supplier


class Stock(SiteModelMixin, BaseUuidModel):

    stock_id = models.CharField(
        verbose_name='Batch ID',
        max_length=30,
        blank=False,
        null=False,
        unique=True)

    expiry_date = models.DateField(
        verbose_name='Expiry Date')

    drug = models.ForeignKey(
        Drug,
        on_delete=models.SET_NULL,
        null=True)

    quantity = models.IntegerField()

    received_by = models.CharField(
        verbose_name='Received By',
        max_length=150,
        blank=False,
        null=False)

    supplier = models.CharField(
        verbose_name='Supplier',
        max_length=150,
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
        app_label = 'pharma_subject'
