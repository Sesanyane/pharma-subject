from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords

from .supplier import Supplier


class Stock(SiteModelMixin, BaseUuidModel):

    stock_id = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        unique=True)

    supplier = models.ForeignKey(
        Supplier,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    is_deleted = models.BooleanField(
        default=False)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
        app_label = 'pharma_subject'
