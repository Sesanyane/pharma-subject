from django.core.validators import RegexValidator
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow, formatted_age
from edc_constants.choices import GENDER
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin

from .site import Site
from .search_slug_model_mixin import SearchSlugModelMixin


class PatientManager(models.Manager):
    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class Patient(UniqueSubjectIdentifierFieldMixin, SiteModelMixin,
              SearchSlugModelMixin, BaseUuidModel):

    initials = models.CharField(
        max_length=5,
        validators=[RegexValidator(r'^[A-Z]{2,3}$', message='Use CAPS, 2-3 letters')],
        help_text='Format is AA or AAA')

    gender = models.CharField(
        max_length=2,
        choices=GENDER)

    consent_datetime = models.DateTimeField(
        default=get_utcnow,
        editable=False)

    patient_site = models.ForeignKey(Site, on_delete=models.PROTECT)

    objects = PatientManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier}, ({self.initials}), Site {self.patient_site.site_code}'

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['initials', 'gender', 'patient_site'])
        return fields

    class Meta:
        app_label = 'pharma_subject'
