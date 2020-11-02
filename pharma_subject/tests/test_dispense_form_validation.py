from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import FEMALE

from model_mommy import mommy

from ..constants import IV
from ..form_validations import DispenseFormValidator
from ..models import Medication, Patient


class TestDispenseFormValidation(TestCase):

    def setUp(self):
        self.patient = mommy.make(
            Patient,
            subject_identifier='1234',
            initials='AD',
            gender=FEMALE,
            sid='123', )
        self.medication = mommy.make(
            Medication)
        self.options = {
            'patient': self.patient.id,
            'medication': self.medication.id,
            'dispense_type': IV,
            'number_of_tablets': None,
            'total_number_of_tablets': None,
            'dose': None,
            'total_volume': '3000mL',
            'infusion_number': 2,
            'duration': '2hours',
            'times_per_day': None,
            'concentration': '3mg/L',
            'weight': 2.6,
            'prepared_datetime': get_utcnow()}

    def test_form_valid(self):
        """
        Checks form saves successfully with all necessary field
        values completed.
        """
        form_validator = DispenseFormValidator(
            cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_iv_with_times_per_day(self):
        """
        Assert raises validation error if DISPENSE TYPE:IV is chosen with
        times per day included
        """
        self.options['times_per_day'] = 2
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('times_per_day', form_validator._errors)

    def test_iv_without_times_per_day(self):
        """
        Checks that no validation error raised if DISPENSE TYPE:IV is
        selected, with times per day not included
        """
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_iv_without_total_volume(self):
        """
        Assert raises validation error if DISPENSE TYPE:IV is chosen with
        total volume not included
        """
        self.options['total_volume'] = None
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('total_volume', form_validator._errors)

    def test_iv_with_total_volume(self):
        """
        Checks that no validation error raised if DISPENSE TYPE:IV is
        selected, with total volume not included
        """
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_iv_without_duration(self):
        """
        Assert raises validation error if DISPENSE TYPE:IV is chosen with
        duration not included
        """
        self.options['duration'] = None
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('duration', form_validator._errors)

    def test_iv_with_number_of_tablets(self):
        """
        Assert raises validation error if DISPENSE TYPE:IV is chosen with
        number of tablets included
        """
        self.options['number_of_tablets'] = 1
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('number_of_tablets', form_validator._errors)

    def test_iv_with_total_number_of_tablets(self):
        """
        Assert raises validation error if DISPENSE TYPE:IV is chosen with
        total number of tablets included
        """
        self.options['total_number_of_tablets'] = 30
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('total_number_of_tablets', form_validator._errors)

    def test_iv_without_concentration(self):
        """
        Assert raises validation error if DISPENSE TYPE:IV is chosen with
        concentration not included
        """
        self.options['concentration'] = None
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('concentration', form_validator._errors)

    def test_iv_with_dose(self):
        """
        Assert raises validation error if DISPENSE TYPE:IV is chosen with
        syrup dose included
        """
        self.options['dose'] = '5mL'
        form_validator = DispenseFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dose', form_validator._errors)
