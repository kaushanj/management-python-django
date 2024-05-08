from django.test import TestCase
from django.core.exceptions import ValidationError
from cloudwatch.validations import ARNValidator

from model_bakery import baker

from cloudwatch.models import AlertSource, Alarm


class TestValidator(TestCase):

    def test_arnvalidator_with_invalid_value(self):
        alert = AlertSource(name="Test Alert", value='invalid arn')
        with self.assertRaisesRegex(ValidationError, ARNValidator.message):
            alert.full_clean()

    def test_arnvalidator_should_not_raised(self):
        try:
            alert = AlertSource(
                name="Test Alert", value='arn:aws:lambda:ap-southeast-2:058188477434:function:ErrorLogFunctionPython')
            alert.full_clean()
        except ValidationError:
            self.fail(
                "Valid value should not raise a ValidationError. Its a valide ARNValidator")


class TestAlertSourceModel(TestCase):

    def test_fail_validation_in_value_property(self):

        alert = AlertSource(name="Test Alert", value='invalid arn')
        with self.assertRaises(ValidationError):
            alert.full_clean()

    def test_create_model_create_successfully(self):
        try:
            alert = AlertSource(
                name="Test Alert", value='arn:aws:lambda:ap-southeast-2:058188477434:function:ErrorLogFunctionPython')
            alert.full_clean()
        except ValidationError:
            self.fail(
                "Valid value should not raise a ValidationError. Its a valide AlertSource model data")


class TestAlerModel(TestCase):

    def test_create_model_successfully(self):

        alert_instance = baker.make(Alarm, statistic=Alarm.STATISTIC_AVERAGE, comparison_operator=Alarm.THRESHOLD_GREATER_THAN_OR_EQUAL,
                                    period=10, metric_name='Errors', treat_missing_data=Alarm.TREAT_DATA_AS_MISSING)
        assert alert_instance.pk > 0
