"""
Import the official AWS SDK for Python,
Django and models relared to cloudwatch.
"""
import boto3
from django.contrib import admin
from django.contrib.admin import TabularInline
from .models import Alarm, AlarmAction, AlermDimension, AlertSource, Dimension


def make_cloudwatch_alarm(obj):
    """
    Creates a CloudWatch alarm based on the provided `obj` instance.

    Parameters:
    - obj: An instance of the model representing the alarm configuration.

    The method retrieves necessary information from related models (AlarmAction, AlermDimension)
    and uses boto3 to create a CloudWatch alarm with the specified parameters.

    Returns:
    - None
    """

    actions = AlarmAction.objects.select_related(
        'arn').filter(alarm_id=obj.pk)
    alarm_dimensions = AlermDimension.objects.filter(alarm_id=obj.pk)
    ok_actions = [
        action.arn.value for action in actions if action.action == 'OK']
    alarm_actions = [
        action.arn.value for action in actions if action.action != "OK"]
    dimensions = [{"Value": alarm_dimension.dimension.value,
                   "Name": alarm_dimension.dimension.name}
                  for alarm_dimension in alarm_dimensions]

    client = boto3.client('cloudwatch')

    name = obj.name
    description = obj.description
    statistic = obj.statistic
    threshold = obj.threshold
    comparison_operator = obj.comparison_operator
    period = obj.period
    is_active = obj.is_active
    metric_name = obj.metric_name
    namespace = obj.namespace
    evaluation_periods = obj.evaluation_periods
    treat_missing_data = obj.treat_missing_data

    client.put_metric_alarm(
        AlarmName=name,
        AlarmDescription=description,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic=statistic,
        ComparisonOperator=comparison_operator,
        Threshold=threshold,
        Period=period,
        EvaluationPeriods=evaluation_periods,
        OKActions=ok_actions,
        AlarmActions=alarm_actions,
        Dimensions=dimensions,
        ActionsEnabled=is_active,
        TreatMissingData=treat_missing_data
    )


class ActionInline(TabularInline):
    """
    The ActionInline is used to display and edit AlarmAction instances inline 
    in the Django admin interface.

    This inline allows users to manage AlarmAction instances directly within the Alarm
    admin interface. It provides autocomplete fields for the 'action' and 'arn' fields
    and ensures that at least one AlarmAction instance is required (min_num=1).
    """

    autocomplete_fields = ['arn']
    model = AlarmAction
    extra = 0
    min_num = 1


class AlermDimensionInline(TabularInline):
    """
    Inline formset for managing related AlermDimension instances in the Alarm admin.

    This inline allows users to manage AlermDimension instances directly within the Alarm
    admin interface. It provides an autocomplete field for the 'dimension' field,
    ensuring that the user can easily select an existing dimension. It enforces
    the requirement that at least one AlermDimension instance is required (min_num=1)
    and allows up to 30 instances to be added (max_num=30).
    """

    autocomplete_fields = ['dimension']
    model = AlermDimension
    extra = 0
    min_num = 1
    max_num = 30


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    """
    Admin interface for the Alarm model, used to create AWS CloudWatch alarms.

    Attributes:
    - list_display: List of fields to display in the admin list view.
    - inlines: List of inline models to include in the admin interface.
    """

    list_display = ['alarm_id', 'name']
    inlines = [ActionInline, AlermDimensionInline]

    def response_post_save_add(self, request, obj):
        """
        Custom post-save method to handle the creation of CloudWatch alarms.

        Retrieves related AlarmAction and AlermDimension instances, extracts necessary information,
        and calls the make_cloudwatch_alarm method to create the CloudWatch alarm.

        Args:
        - request: The request object.
        - obj: The Alarm instance that was saved.

        Returns:
        - The response from the superclass method.
        """

        make_cloudwatch_alarm(obj)

        return super().response_post_save_add(request, obj)

    def response_post_save_change(self, request, obj):
        """
        Custom post-save method to handle the creation of CloudWatch alarms.

        Retrieves related AlarmAction and AlermDimension instances, extracts necessary information,
        and calls the make_cloudwatch_alarm method to create the CloudWatch alarm.

        Args:
        - request: The request object.
        - obj: The Alarm instance that was saved.

        Returns:
        - The response from the superclass method.
        """

        make_cloudwatch_alarm(obj)

        return super().response_post_save_change(request, obj)


@admin.register(AlertSource)
class AlertSourceAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the AlertSource model.

    This admin class customizes the appearance and behavior of the ARN model
    in the Django admin interface. It excludes the 'arn_id' field from the admin
    form, as it is automatically generated. It also adds a search field for the 'value'
    field, allowing administrators to search for ARN instances by their value.
    """

    exclude = ['arn_id']
    search_fields = ['value']


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Dimension model.

    This admin class customizes the appearance and behavior of the Dimension model
    in the Django admin interface. It specifies that the 'dimension_id' and 'value'
    fields should be displayed in the list view. It also adds a search field for the 'value'
    field, allowing administrators to search for Dimension instances by their value.
    """

    list_display = ['dimension_id', 'value']
    search_fields = ['value']
