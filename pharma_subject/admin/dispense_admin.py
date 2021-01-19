from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import pharma_subject_admin
from ..forms import DispenseForm, DispenseRefillForm
from ..models import Dispense, DispenseRefill
from .modeladmin_mixins import ModelAdminMixin


class DispenseRefillInlineAdmin(TabularInlineMixin, admin.TabularInline):

    model = DispenseRefill
    form = DispenseRefillForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': [
                'refill_datetime',
                'user_created',
                'user_modified',
                'created',
                'modified']}
         ),)


@admin.register(Dispense, site=pharma_subject_admin)
class DispenseAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DispenseForm

    inlines = [DispenseRefillInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_identifier',
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
                       'prepared_datetime',
                       'step',
                       'needle_size'),
            }), audit_fieldset_tuple)

    list_display = ('subject_identifier', 'medication', 'prepared_datetime',)

    search_fields = ('medication__name',)

    radio_fields = {'dispense_type': admin.VERTICAL}
