from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators.form_validator_mixin import FormValidatorMixin

from ..models import Dispense
from ..form_validations import DispenseFormValidator


class DispenseForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = DispenseFormValidator

    class Meta:
        model = Dispense
        fields = '__all__'
