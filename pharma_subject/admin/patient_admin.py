from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import PatientForm
from ..models import Patient


@admin.register(Patient, site=pharma_subject_admin)
class PatientAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PatientForm

    fieldsets = (
        (None, {
            'fields': ('subject_identifier',
                       'initials',
                       'gender',
                       'sid',
                       'patient_site'),
            }), audit_fieldset_tuple)

    radio_fields = {'gender': admin.VERTICAL}

    list_display = ('subject_identifier', 'initials', 'gender')

    search_fields = ('subject_identifier', 'initials',)
