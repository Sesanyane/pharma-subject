from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords


class Supplier(SiteModelMixin, BaseUuidModel):

    name = models.CharField(
        max_length=150,
        null=False,
        blank=False)

    phone = models.CharField(
        max_length=12,
        blank=False,
        null=False,
        unique=True)

    address = models.CharField(
        max_length=200,
        blank=False,
        null=False)

    email = models.EmailField(
        max_length=254,
        unique=True)

    description = models.TextField()

    vat_num = models.CharField(
        max_length=15,
        unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        app_label = 'pharma_subject'
