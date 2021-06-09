from django.apps import apps as django_apps
from django.contrib import admin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import pharma_subject_admin
from ..forms import DispenseForm, DispenseRefillForm
from ..models import Dispense, DispenseRefill
from .modeladmin_mixins import ModelAdminMixin
from edc_fieldsets.fieldlist import Fieldlist

from django.core.exceptions import ObjectDoesNotExist


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
class DispenseAdmin(ModelAdminMixin, FieldsetsModelAdminMixin,
                    admin.ModelAdmin):
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

    conditional_fieldlists = {
        'HPTN 084': Fieldlist(insert_fields=('bmi', 'needle_size'),
                               remove_fields=('weight',), insert_after='duration',
                               section=None),
         'Tatelo': Fieldlist(insert_fields=('step',),
                             remove_fields=('visit_code',),
                             insert_after='duration',
                             section=None)
         }

    def get_key(self, request, obj=None):
        return self.get_instance(request)

    def get_instance(self, request):
        """Returns the instance that provides the key
        for the "conditional" dictionaries.
        """
        patient_cls = django_apps.get_model('pharma_subject.patient')
        if request.GET.get('subject_identifier'):
            try:
                patient_obj = patient_cls.objects.get(
                    subject_identifier=request.GET.get('subject_identifier'))
            except patient_cls.DoesNotExist:
                raise
            else:
                return patient_obj.patient_site.protocol.name.upper()
