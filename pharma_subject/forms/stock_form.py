from django import forms
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_base.sites.forms import SiteModelFormMixin

from ..models import Stock


class StockForm(FormValidatorMixin, SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Stock
        fields = '__all__'
