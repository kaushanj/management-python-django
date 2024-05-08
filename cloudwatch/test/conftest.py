import pytest
from model_bakery import baker
from cloudwatch.models import Alarm


@pytest.fixture
def alarm_model_instance():
    return baker.make(Alarm, statistic=Alarm.STATISTIC_AVERAGE, comparison_operator=Alarm.THRESHOLD_GREATER_THAN_OR_EQUAL,
                      period=10, metric_name='Errors', treat_missing_data=Alarm.TREAT_DATA_AS_MISSING)
