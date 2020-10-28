from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from ..constants import CAPSULE, SYRUP, SOLUTION, TABLET, IM, IV


class DispenseFormValidator(FormValidator):

    def clean(self):
        self.validate_tablet_n_capsule()
        self.validate_syrup_n_solution()
        self.validate_iv_n_im()

    def validate_tablet_n_capsule(self):
        not_required = ['dose', 'total_volume', 'duration', ]
        responses = [TABLET, CAPSULE]
        dispense_type = self.cleaned_data.get('dispense_type')
        for field in not_required:
            self.validate_not_required(
                *responses,
                field='dispense_type',
                field_required=field,
                not_required_msg=(f'You have selected dispense type {dispense_type} '
                                  f'you should NOT enter {field}'))

        required = ['number_of_tablets', 'total_number_of_tablets',
                    'times_per_day', 'concentration', ]
        for field in required:
            self.validate_required(
                *responses,
                field='dispense_type',
                field_required=field,
                required_msg=f'You have selected dispense type {dispense_type}, you should enter {field}')

        if dispense_type in responses and (
            float(self.cleaned_data.get('total_number_of_tablets')) < float(
                self.cleaned_data.get('times_per_day')) * float(
                    self.cleaned_data.get('number_of_tablets'))):
            msg = {'total_number_of_tablets':
                   'Cannot have total number of tablets less than number of tablets by times per day'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_syrup_n_solution(self):
        required = ['dose', 'total_volume', 'concentration', 'times_per_day', ]
        responses = [SYRUP, SOLUTION]
        dispense_type = self.cleaned_data.get('dispense_type')
        for field in required:
            self.validate_required(
                *responses,
                field='dispense_type',
                field_required=field,
                required_msg=(f'You have selected dispense type {dispense_type},'
                              f' you should enter {field}'))

            not_required = ['number_of_tablets', 'total_number_of_tablets',
                            'duration', ]
            for field in not_required:
                self.validate_not_required(
                    *responses,
                    field='dispense_type',
                    field_required=field,
                    not_required_msg=(f'You have selected dispense type {dispense_type},'
                                      f' you should NOT enter {field}'))

    def validate_iv_n_im(self):
        not_required = ['dose', 'number_of_tablets', 'total_number_of_tablets',
                        'times_per_day', ]
        responses = [IV, IM]
        dispense_type = self.cleaned_data.get('dispense_type')
        for field in not_required:
            self.validate_not_required(
                *responses,
                field='dispense_type',
                field_required=field,
                not_required_msg=(f'You have selected dispense type {dispense_type},'
                                  f' you should NOT enter {field}'))

        required = ['total_volume', 'duration', 'concentration', 'infusion_number', ]
        for field in required:
            self.validate_required(
                *responses,
                field='dispense_type',
                field_required=field,
                required_msg=f'You have selected dispense type {dispense_type}, you should enter {field}')

    def validate_not_required(self, *responses, field=None, field_required=None,
                              not_required_msg=None, **kwargs):
        """Raises an exception or returns False.

        if field in responses then field_required is not required.
        """
        if field in self.cleaned_data and field_required in self.cleaned_data:
            if (self.cleaned_data.get(field) in responses and
                    self.cleaned_data.get(field_required)):
                msg = {field_required: not_required_msg or 'This field is not required.'}
                self._errors.update(msg)
                raise ValidationError(msg)
        return False

    def validate_required(self, *responses, field=None, field_required=None,
                          required_msg=None, **kwargs):
        """Raises an exception or returns False.

        if field in responses then field_required is required.
        """
        if field in self.cleaned_data and field_required in self.cleaned_data:
            if (self.cleaned_data.get(field) in responses and
                    not self.cleaned_data.get(field_required)):
                msg = {field_required: required_msg or 'This field is required.'}
                self._errors.update(msg)
                raise ValidationError(msg)
        return False
