from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import SiteForm
from ..models import Site


@admin.register(Site, site=pharma_subject_admin)
class SiteAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SiteForm

    fieldsets = (
        (None, {
            'fields': ('protocol',
                       'name',
                       'site_code',
                       'telephone_number',),
            }), audit_fieldset_tuple)

    list_display = ('protocol', 'site_code', 'telephone_number',)

    search_fields = ('site_code', 'telephone_number',)
