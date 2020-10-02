from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import ProtocolForm
from ..models import Protocol


@admin.register(Protocol, site=pharma_subject_admin)
class ProtocolAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ProtocolForm

    fieldsets = (
        (None, {
            'fields': ('number',
                       'name', ),
            }), audit_fieldset_tuple)

    list_display = ('name', 'number', )

    search_fields = ('name', 'number', )
