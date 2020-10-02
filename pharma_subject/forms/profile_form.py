from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators.form_validator_mixin import FormValidatorMixin

from ..models import Profile


class ProfileForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
