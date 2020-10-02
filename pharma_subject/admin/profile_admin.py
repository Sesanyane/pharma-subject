from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import ProfileForm
from ..models import Profile


@admin.register(Profile, site=pharma_subject_admin)
class ProfileAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ProfileForm

    fieldsets = (
        (None, {
            'fields': ('user',
                       'initials', ),
            }), audit_fieldset_tuple)

    list_display = ('initials', 'user', )

    search_fields = ('initials', )
