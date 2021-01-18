from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import DrugForm
from ..models import Drug


@admin.register(Drug, site=pharma_subject_admin)
class DrugAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DrugForm

    fieldsets = (
        (None, {
            'fields': ('name',
#                        'quantity',
                       'protocol',
                       'storage_instructions'),
            }), audit_fieldset_tuple)

    list_display = ('name', 'protocol',)

    search_fields = ('name',)
