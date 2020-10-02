from django import forms
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_base.sites.forms import SiteModelFormMixin


from ..models import Patient


class PatientForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'
