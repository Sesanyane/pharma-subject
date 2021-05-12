from django.apps import apps as django_apps
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
                       'number_of_tablets',
                       'dose',
                       'times_per_day',
                       'total_number_of_tablets',
                       'total_volume',
                       'concentration',
                       'duration',
                       'weight',
                       'visit_code',
                       'prepared_datetime',),
            }), audit_fieldset_tuple)

    list_display = ('subject_identifier', 'medication', 'prepared_datetime',)

    readonly_fields = ('prepared_datetime',)

    search_fields = ('medication__name',)

    radio_fields = {'dispense_type': admin.VERTICAL}

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        patient_cls = django_apps.get_model('pharma_subject.patient')

        if request.GET.get('subject_identifier'):
            try:
                patient_obj = patient_cls.objects.get(subject_identifier=request.GET.get('subject_identifier'))
            except patient_cls.DoesNotExist:
                pass
            else:
                protocol = patient_obj.patient_site.protocol.name

                if protocol == 'HPTN 084':
                    old_fields = [field for field in fieldsets[0][1]['fields']]
                    old_fields.remove('step')
                    old_fields.remove('weight')
                    old_fields = old_fields + ['infusion_number', 'bmi', 'needle_size']
                    fieldsets[0][1].update(fields=tuple(old_fields))
                elif protocol == 'Tatelo':
                    old_fields = [field for field in fieldsets[0][1]['fields']]
                    old_fields.remove('visit_code')
                    old_fields = old_fields + ['step', ]
                    fieldsets[0][1].update(fields=tuple(old_fields))
        return fieldsets
