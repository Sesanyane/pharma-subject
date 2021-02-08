from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords

from .drug import Drug
from .supplier import Supplier
from ..choices import CONTAINER_TYPES


class Stock(SiteModelMixin, BaseUuidModel):

    stock_id = models.CharField(
        verbose_name='Batch ID',
        max_length=30,
        blank=False,
        null=False,
        unique=True)

    drug = models.ForeignKey(
        Drug,
        on_delete=models.SET_NULL,
        null=True)

    type = models.CharField(
        verbose_name='Drug container type',
        choices=CONTAINER_TYPES,
        max_length=50)

    volume = models.IntegerField(
        verbose_name='Volume or number of tablets per container received')

    quantity = models.IntegerField(
        verbose_name='Total received',
        help_text='i.e overall number of tablets, vial, packs etc.')

    received_by = models.CharField(
        verbose_name='Received By',
        max_length=150,
        blank=False,
        null=False)

    received_date = models.DateTimeField()

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
        app_label = 'pharma_subject'
