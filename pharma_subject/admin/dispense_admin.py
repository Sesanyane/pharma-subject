from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import pharma_subject_admin
from ..forms import DispenseForm
from ..models import Dispense
from .modeladmin_mixins import ModelAdminMixin


@admin.register(Dispense, site=pharma_subject_admin)
class DispenseAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DispenseForm

    fieldsets = (
        (None, {
            'fields': ('patient',
                       'medication',
                       'dispense_type',
                       'infusion_number',
                       'number_of_tablets',
                       'dose',
                       'times_per_day',
                       'total_number_of_tablets',
                       'total_volume',
                       'concentration',
                       'duration',
                       'weight',
                       'prepared_datetime', ),
            }), audit_fieldset_tuple)

    list_display = ('patient', 'medication', 'prepared_datetime', )

    search_fields = ('medication__name', )

    radio_fields = {'dispense_type': admin.VERTICAL}
