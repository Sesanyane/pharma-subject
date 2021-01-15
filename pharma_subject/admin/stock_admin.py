from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import MedicationForm, StockForm
from ..models import Medication, Stock


# class MedicationAdmin(TabularInlineMixin, admin.TabularInline):
#     model = Medication
#     form = MedicationForm
#     extra = 1
#
#     fieldsets = (
#         (None, {
#             'fields': (
#                 'name',
#                 'protocol',
#                 'storage_instructions',
#                 'quantity',
#             )}),
#         )


@admin.register(Stock, site=pharma_subject_admin)
class StockAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = StockForm
#     inlines = [MedicationAdmin]

    fieldsets = (
        (None, {
            'fields': ('stock_id',
                       'supplier',
                       'is_deleted'),
            }), audit_fieldset_tuple)

    list_display = ('stock_id', 'supplier',)

    search_fields = ('stock_id',)
