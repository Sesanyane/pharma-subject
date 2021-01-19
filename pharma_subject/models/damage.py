from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_managers import HistoricalRecords

from .drug import Drug


class Damage(SiteModelMixin, BaseUuidModel):

    drug = models.ForeignKey(
        Drug,
        on_delete=models.SET_NULL,
        verbose_name='Affected Drug',
        null=True)

    reason = models.CharField(
        verbose_name='Reason',
        max_length=200,
        blank=True,
        null=True)

    how_many = models.IntegerField(
        verbose_name='How Many Affected',
        max_length=20)

    comment = models.CharField(
        verbose_name='Comment',
        max_length=200,
        blank=True,
        null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = 'Damage'
        verbose_name_plural = 'Damaged'
        app_label = 'pharma_subject'
