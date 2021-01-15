from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import SupplierForm
from ..models import Supplier


@admin.register(Supplier, site=pharma_subject_admin)
class SupplierAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SupplierForm

    fieldsets = (
        (None, {
            'fields': ('name',
                       'phone',
                       'address',
                       'email',
                       'description',
                       'vat_num'),
            }), audit_fieldset_tuple)

    list_display = ('name', 'phone', )

    search_fields = ('name', )
