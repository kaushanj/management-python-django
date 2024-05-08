"""
Testing woth pytest package.
Test Alarm admin
"""
import pytest
from django.contrib.admin.sites import AdminSite
from cloudwatch.admin import AlarmAdmin, make_cloudwatch_alarm
from cloudwatch.models import Alarm

@pytest.fixture
def alarm_admin():
    """
    Fixture to create an instance of AlarmAdmin for testing.
    """
    admin_site = AdminSite()
    return AlarmAdmin(Alarm, admin_site)

@pytest.mark.django_db
class TestAlarmAdmin:
    """
    Test cases for the AlarmAdmin class.
    """

    def test_list_display(self, alarm_admin):
        """
        Test the list_display attribute of AlarmAdmin.
        """
        list_display = alarm_admin.get_list_display(None)
        assert list_display == ['alarm_id', 'name']

    def test_create_and_save_alarm(self, alarm_admin, alarm_model_instance):
        """
        Test creating and saving an alarm using AlarmAdmin.
        """
        alarm_admin.save_model(
            obj=alarm_model_instance, request=None, form=None, change=False)

        updated_instance = Alarm.objects.get(pk=alarm_model_instance.pk)

        assert updated_instance.period == 10
        assert updated_instance.pk > 0

    @pytest.mark.skip(reason="Don't call every time run test. It will create aws cloudwatch alarm.")
    def test_creating_cloud_watch_alarm(self, alarm_model_instance):
        """
        Test creating a CloudWatch alarm.
        """
        try:
            make_cloudwatch_alarm(obj=alarm_model_instance)
            assert True
        except Exception:
            assert False
    
    @pytest.mark.skip(reason="Don't call every time run test. It will create aws cloudwatch alarm.")
    def test_inactivate_cloud_watch_alarm(self, alarm_model_instance):
        """
        Test creating and change CloudWatch alarm.
        """
        try:
            make_cloudwatch_alarm(obj=alarm_model_instance)
            alarm_model_instance.is_active = False
            make_cloudwatch_alarm(alarm_model_instance)
            assert True
        except Exception:
            assert False
    
