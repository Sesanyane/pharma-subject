from django import forms
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_base.sites.forms import SiteModelFormMixin

from ..models import Drug


class DrugForm(FormValidatorMixin, SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Drug
        fields = '__all__'
