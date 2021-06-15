from django.db import models
from django.db.models.deletion import PROTECT
from django.core.validators import RegexValidator
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin

from .search_slug_model_mixin import SearchSlugModelMixin
from .drug import Drug
from ..choices import DISPENSE_TYPES
from ..constants import TABLET


class Dispense(NonUniqueSubjectIdentifierFieldMixin,
               SiteModelMixin, SearchSlugModelMixin,
               BaseUuidModel):

    date_hierarchy = '-prepared_datetime'

    visit_code = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        help_text='Only required if dispense type IV or IM is chosen')

    medication = models.ForeignKey(
        Drug,
        on_delete=models.PROTECT,
        verbose_name='Medication')

    dispense_type = models.CharField(
        max_length=15,
        choices=DISPENSE_TYPES,
        default=TABLET)

    infusion_number = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Only required if dispense type IV or IM is chosen')

    number_of_tablets = models.DecimalField(
        blank=True,
        null=True,
        max_digits=3,
        decimal_places=1,
        validators=[RegexValidator('^[0-9]+\.(5?0?)?$',
                                   message=('Invalid format only allows full numbers '
                                            'of halves(.5).'))],
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
        max_length=25)

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

    bmi = models.DecimalField(
        verbose_name='BMI',
        decimal_places=1,
        max_digits=3,
        blank=True,
        null=True,
        help_text='Only required if IV or IM is chosen for HPTN 084')

    step = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text='Only required if IV or IM is chosen for Tatelo')

    needle_size = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text='Only required if IV or IM is chosen for HPTN 084')

    prepared_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_future])

    def __str__(self):
        return f'{self.subject_identifier} , {str(self.medication)}'

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['medication', 'dispense_type'])
        return fields

    class Meta:
        app_label = 'pharma_subject'
        unique_together = ('subject_identifier', 'medication', 'prepared_datetime')


class DispenseRefill(SiteModelMixin, BaseUuidModel):

    dispense = models.ForeignKey(Dispense, on_delete=PROTECT)

    refill_datetime = models.DateTimeField()

    class Meta:
        app_label = 'pharma_subject'
        verbose_name = 'Dispense Refill'
        verbose_name_plural = 'Dispense Refills'
        unique_together = ('dispense', 'refill_datetime')
