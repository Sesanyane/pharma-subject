from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from ..constants import CAPSULE, SYRUP, SOLUTION, TABLET, IM, IV
from pharma_subject.constants import SUPPOSITORY


class DispenseFormValidator(FormValidator):

    def clean(self):
        self.dispense_type = self.cleaned_data.get('dispense_type')
        self.validate_times_per_day()
        self.validate_total_volume()
        self.validate_tablet_n_capsule()
        self.validate_syrup_n_solution()
        self.validate_iv_n_im()
        
    def validate_times_per_day(self):
        
        responses = [TABLET, CAPSULE, SYRUP, SOLUTION , SUPPOSITORY]
        
        self.required_if(
                *responses,
                field='dispense_type',
                field_required='times_per_day',
                required_msg=(f'You have selected dispense type {self.dispense_type}, '
                              f'you should enter \'times_per_day\''),
                not_required_msg=(f'You have selected dispense type {self.dispense_type} '
                                  'you should NOT enter \'times_per_day\''))
        
    def validate_total_volume(self):
        
        responses = [IV, IM, SYRUP, SOLUTION ]
        
        self.required_if(
                *responses,
                field='dispense_type',
                field_required='total_volume',
                required_msg=(f'You have selected dispense type {self.dispense_type}, '
                              'you should enter \'total_volume\''),
                not_required_msg=(f'You have selected dispense type {self.dispense_type} '
                                  'you should NOT enter \'total_volume\''))
        
    def validate_tablet_n_capsule(self):
        responses = [TABLET, CAPSULE, SUPPOSITORY]
        required = ['number_of_tablets', 'total_number_of_tablets', ]
        for field in required:
            self.required_if(
                *responses,
                field='dispense_type',
                field_required=field,
                required_msg=(f'You have selected dispense type {self.dispense_type}, '
                              f'you should enter {field}'),
                not_required_msg=(f'You have selected dispense type {self.dispense_type} '
                                  f'you should NOT enter {field}'))
        
        

        if self.dispense_type in responses and (
            float(self.cleaned_data.get('total_number_of_tablets')) < float(
                self.cleaned_data.get('times_per_day')) * float(
                    self.cleaned_data.get('number_of_tablets'))):
            msg = {'total_number_of_tablets':
                   'Cannot have total number of tablets less than number of tablets by times per day'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_syrup_n_solution(self):
        responses = [SYRUP, SOLUTION]
        self.required_if(
            *responses,
            field='dispense_type',
            field_required='dose',
            required_msg=(f'You have selected dispense type {self.dispense_type},'
                          ' you should enter \'dose\''),
            not_required_msg=(f'You have selected dispense type {self.dispense_type},'
                              ' you should NOT enter \'dose\''))

    def validate_iv_n_im(self):
        responses = [IV, IM]
        fields = ['duration', 'visit_code']
        for field in fields:
            self.required_if(
                *responses,
                field='dispense_type',
                field_required=field,
                required_msg=(f'You have selected dispense type {self.dispense_type}, '
                              f'you should enter \'duration\''),
                not_required_msg=(f'You have selected dispense type {self.dispense_type},'
                                  f' you should NOT enter \'duration\''))
