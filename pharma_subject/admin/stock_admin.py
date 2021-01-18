from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import TabularInlineMixin

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import pharma_subject_admin
from ..forms import StockForm, StockItemForm
from ..models import Stock, StockItem


class StockItemAdmin(TabularInlineMixin, admin.TabularInline):
    model = StockItem
    form = StockItemForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': ('medication',
                       'quantity',
                       'protocol',
                       'code',
                       'stock'),
            }),)

    list_display = ('medication',)

    search_fields = ('medication',)


@admin.register(Stock, site=pharma_subject_admin)
class StockAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = StockForm
    inlines = [StockItemAdmin]

    fieldsets = (
        (None, {
            'fields': ('stock_id',
                       'supplier'),
            }), audit_fieldset_tuple)

    list_display = ('stock_id', 'supplier',)

    search_fields = ('stock_id',)
