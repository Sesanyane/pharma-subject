from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators.form_validator_mixin import FormValidatorMixin

from ..models import Dispense, DispenseRefill
from ..form_validations import DispenseFormValidator


class DispenseForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = DispenseFormValidator

    class Meta:
        model = Dispense
        fields = '__all__'


class DispenseRefillForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = DispenseRefill
        fields = '__all__'
