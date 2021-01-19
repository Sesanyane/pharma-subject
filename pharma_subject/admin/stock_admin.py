from django.contrib import admin
from edc_base.utils import get_utcnow
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import StockForm
from ..models import Stock


@admin.register(Stock, site=pharma_subject_admin)
class StockAdmin(ModelAdminMixin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.received_by = request.user.username
            obj.received_date = get_utcnow()
        super().save_model(request, obj, form, change)

    form = StockForm

    fieldsets = (
        (None, {
            'fields': ('stock_id',
                       'expiry_date',
                       'drug',
                       'quantity',
                       'supplier',),
            }), audit_fieldset_tuple)

    list_display = ('stock_id', 'supplier',)

    search_fields = ('stock_id',)
