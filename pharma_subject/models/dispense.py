from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
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

    drug = models.ForeignKey(
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
        return f'{self.subject_identifier} , {str(self.medication)}'
    
    @property
    def prescription(self):
        if self.dispense_type == TABLET:
            if self.number_of_tablets > 1:
                prescription = (
                    '{medication} {number_of_tablets} tablets {times_per_day} times per day '
                    '({total_number_of_tablets} tablets)'.format(
                        medication=self.medication.name,
                        number_of_tablets=self.number_of_tablets,
                        times_per_day=self.times_per_day,
                        total_number_of_tablets=self.total_number_of_tablets))
            else:
                prescription = (
                    '{medication} 1 tablet {times_per_day} time per day '
                    '({total_number_of_tablets} tablets)'.format(
                        medication=self.medication.name,
                        times_per_day=self.times_per_day,
                        total_number_of_tablets=self.total_number_of_tablets))
        if self.dispense_type == SYRUP:
            prescription = (
                '{medication} {dose} dose {times_per_day} times a day '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    dose=self.dose,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == SOLUTION:
            prescription = (
                '{medication} {dose} dose {times_per_day} times a day '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    dose=self.dose,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == IV:
            prescription = (
                '{medication} Intravenous {concentration} {duration} '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    duration=self.duration,
                    concentration=self.concentration,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == IM:
            prescription = (
                '{medication} IntraMuscular {concentration} {duration} '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    duration=self.duration,
                    concentration=self.concentration,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == SUPPOSITORY:
            prescription = (
                '{medication} {number_of_tablets} suppository {times_per_day} times per day '
                '({total_number_of_tablets} suppository)'.format(
                    medication=self.medication.name,
                    number_of_tablets=self.number_of_tablets,
                    times_per_day=self.times_per_day,
                    total_number_of_tablets=self.total_number_of_tablets))
        if self.dispense_type == CAPSULE:
            prescription = (
                '{medication} {number_of_tablets} capsules {times_per_day} times per day '
                '({total_number_of_tablets} capsules)'.format(
                    medication=self.medication.name,
                    number_of_tablets=self.number_of_tablets,
                    times_per_day=self.times_per_day,
                    total_number_of_tablets=self.total_number_of_tablets))
        return prescription

    
    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['drug', 'dispense_type'])
        return fields

    class Meta:
        app_label = 'pharma_subject'
        unique_together = ('subject_identifier', 'drug', 'prepared_date')

class DispenseRefill(SiteModelMixin, BaseUuidModel):
    
    dispense = models.ForeignKey(Dispense, on_delete=PROTECT)
    
    refill_datetime = models.DateTimeField()
    
    class Meta:
        app_label = 'pharma_subject'
        verbose_name = 'Dispense Refill'
        verbose_name_plural = 'Dispense Refills'
        unique_together = ('dispense', 'refill_datetime')