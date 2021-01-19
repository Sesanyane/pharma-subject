from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import DamageForm
from ..models import Damage


@admin.register(Damage, site=pharma_subject_admin)
class DamageAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DamageForm

    fieldsets = (
        (None, {
            'fields': ('drug',
                       'reason',
                       'how_many',
                       'comment'),
            }), audit_fieldset_tuple)
