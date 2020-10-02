from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow

from .patient import Patient
from .medication import Medication
from ..choices import DISPENSE_TYPES
from ..constants import TABLET


class Dispense(SiteModelMixin, BaseUuidModel):

    date_hierarchy = '-prepared_datetime'

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)

    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)

    dispense_type = models.CharField(
        max_length=15,
        choices=DISPENSE_TYPES,
        default=TABLET)

    infusion_number = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Only required if dispense type IV or IM is chosen')

    number_of_tablets = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=('Only required if dispense type TABLET, CAPSULES, '
                   'SUPPOSITORIES is chosen'))

    dose = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Only required if dispense type SYRUP or SOLUTION is chosen')

    times_per_day = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=('Only required if dispense type TABLET, CAPSULES, '
                   'SUPPOSITORIES, SYRUP is chosen'))

    total_number_of_tablets = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=('Only required if dispense type TABLET or SUPPOSITORY  is '
                   'chosen'))

    total_volume = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text='Only required if dispense type is SYRUP, IM, IV is chosen')

    concentration = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        help_text=('Only required if dispense type IV, IM, CAPSULES, SOLUTION,'
                   ' SUPPOSITORIES, TABLET is chosen'))

    duration = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text='Only required if dispense type IV or IM is chosen')

    weight = models.DecimalField(
        verbose_name='Weight in kg',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True,
        help_text='Only required if IV or IM is chosen')

    prepared_datetime = models.DateTimeField(default=get_utcnow)

    prepared_date = models.DateTimeField(default=get_utcnow, editable=False)

    def __str__(self):
        return str(self.patient)

    class Meta:
        app_label = 'pharma_subject'
        unique_together = ('patient', 'medication', 'prepared_date')
