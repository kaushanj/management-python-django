"""
Imports the models module from Django's db package.
It also imports a custom ARNValidator from a module named validations
"""
from django.db import models
from .validations import ARNValidator


class Alarm(models.Model):

    """
    Model for creating alarms for specific AWS Lambda functions.

    Attributes:
    - STATISTIC_SAMPLE_COUNT: 'SampleCount'
    - STATISTIC_SUM: 'Sum'
    - STATISTIC_AVERAGE: 'Average'
    - STATISTIC_MINIMUM: 'Minimum'
    - STATISTIC_MAXIMUM: 'Maximum'
    - STATISTIC_CHOICES: List of statistic choices.
    - THRESHOLD_GREATER_THAN_OR_EQUAL: 'GreaterThanOrEqualToThreshold'
    - THRESHOLD_GREATER_THAN: 'GreaterThanThreshold'
    - THRESHOLD_LESS_THAN: 'LessThanThreshold'
    - THRESHOLD_LESS_THAN_OR_EQUAL: 'LessThanOrEqualToThreshold'
    - THRESHOLD_LESS_THAN_LOWER_OR_GREATER_THAN_UPPER: 'LessThanLowerOrGreaterThanUpperThreshold'
    - THRESHOLD_LESS_THAN_LOWER: 'LessThanLowerThreshold'
    - THRESHOLD_GREATER_THAN_UPPER: 'GreaterThanUpperThreshold'
    - THRESHOLD_CHOICES: List of threshold choices.
    - NAMESPACE_LAMBDA: 'AWS/Lambda'
    - NAMESPACE_EC2: 'AWS/EC2'
    - NAMESPACE_CHOICES: List of namespace choices (e.g., AWS/Lambda, AWS/EC2).
    - TREAT_DATA_AS_BREACHING: 'BREACHING'
    - TREAT_DATA_AS_NOTBREACHING: 'NOTBREACHING'
    - TREAT_DATA_AS_IGNORE: 'IGNORE'
    - TREAT_DATA_AS_MISSING: 'MISSING'
    - TREAT_DATA_CHOICES: List of choices for how to treat missing data.

    Fields:
    - alarm_id: SmallAutoField for the alarm ID.
    - name: CharField for the alarm name.
    - description: CharField for the alarm description.
    - statistic: CharField for the statistic used by the alarm (choices from STATISTIC_CHOICES).
    - threshold: PositiveSmallIntegerField for the threshold value.
    - comparison_operator: CharField for the comparison operator (choices from THRESHOLD_CHOICES).
    - period: PositiveSmallIntegerField for the period in seconds.
    - is_active: BooleanField indicating whether the alarm is active.
    - metric_name: CharField for the metric name.
    - namespace: CharField for the namespace (choices from NAMESPACE_CHOICES).
    - treat_missing_data: CharField for how to treat missing data (choices from TREAT_DATA_CHOICES).
    - evaluation_periods: PositiveSmallIntegerField for the number of evaluation periods.

    Methods:
    - __str__: Returns the name of the alarm.
    """

    STATISTIC_SAMPLE_COUNT = 'SampleCount'
    STATISTIC_SUM = 'Sum'
    STATISTIC_AVERAGE = 'Average'
    STATISTIC_MINIMUM = 'Minimum'
    STATISTIC_MAXIMUM = 'Maximum'

    STATISTIC_CHOICES = [
        (STATISTIC_SAMPLE_COUNT, 'SAMPLE_COUNT'),
        (STATISTIC_SUM, 'SUM'),
        (STATISTIC_AVERAGE, 'AVERAGE'),
        (STATISTIC_MINIMUM, 'MINIMUM'),
        (STATISTIC_MAXIMUM, 'MAXIMUM'),
    ]

    THRESHOLD_GREATER_THAN_OR_EQUAL = 'GreaterThanOrEqualToThreshold'
    THRESHOLD_GREATER_THAN = 'GreaterThanThreshold'
    THRESHOLD_LESS_THAN = 'LessThanThreshold'
    THRESHOLD_LESS_THAN_OR_EQUAL = 'LessThanOrEqualToThreshold'
    THRESHOLD_LESS_THAN_LOWER_OR_GREATER_THAN_UPPER = 'LessThanLowerOrGreaterThanUpperThreshold'
    THRESHOLD_LESS_THAN_LOWER = 'LessThanLowerThreshold'
    THRESHOLD_GREATER_THAN_UPPER = 'GreaterThanUpperThreshold'

    THRESHOLD_CHOICES = [
        (THRESHOLD_GREATER_THAN_OR_EQUAL, 'GREATER_THAN_OR_EQUAL'),
        (THRESHOLD_GREATER_THAN, 'GREATER_THAN'),
        (THRESHOLD_LESS_THAN, 'LESS_THAN'),
        (THRESHOLD_LESS_THAN_OR_EQUAL, 'LESS_THAN_OR_EQUAL'),
        (THRESHOLD_LESS_THAN_LOWER_OR_GREATER_THAN_UPPER,
         'LESS_THAN_LOWER_OR_GREATER_THAN_UPPER'),
        (THRESHOLD_LESS_THAN_LOWER, 'LESS_THAN_LOWER'),
        (THRESHOLD_GREATER_THAN_UPPER, 'GREATER_THAN_UPPER'),
    ]

    NAMESPACE_LAMBDA = 'AWS/Lambda'
    NAMESPACE_EC2 = 'AWS/EC2'

    NAMESPACE_CHOICES = [
        (NAMESPACE_LAMBDA, 'Lambda'),
        (NAMESPACE_EC2, 'EC2')
    ]

    TREAT_DATA_AS_BREACHING = 'breaching'
    TREAT_DATA_AS_NOTBREACHING = 'notBreaching'
    TREAT_DATA_AS_IGNORE = 'ignore'
    TREAT_DATA_AS_MISSING = 'missing'

    TREAT_DATA_CHOICES = [
        (TREAT_DATA_AS_BREACHING, 'breaching'),
        (TREAT_DATA_AS_NOTBREACHING, 'notBreaching'),
        (TREAT_DATA_AS_IGNORE, 'ignore'),
        (TREAT_DATA_AS_MISSING, 'missing'),
    ]

    alarm_id = models.SmallAutoField(
        primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    statistic = models.CharField(max_length=55, choices=STATISTIC_CHOICES)
    threshold = models.PositiveSmallIntegerField(null=False)
    comparison_operator = models.CharField(
        max_length=255, choices=THRESHOLD_CHOICES)
    period = models.PositiveSmallIntegerField(help_text="In seconds, greater than 10 seconds. ex: 10")
    is_active = models.BooleanField(default=True)
    metric_name = models.CharField(max_length=55, null=False)
    namespace = models.CharField(max_length=255, choices=NAMESPACE_CHOICES)
    treat_missing_data = models.CharField(
        max_length=255, choices=TREAT_DATA_CHOICES)
    evaluation_periods = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.name}'


class AlertSource(models.Model):

    """
    Model for setting AWS resource AlertSource.

    Attributes:
    - arn_id: AutoField for the ARN ID.
    - value: CharField for the ARN value with a length of up to 255 characters, 
    validated using ARNValidator.

    Methods:
    - __str__: Returns the value of the ARN.
    """

    arn_id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, validators=[ARNValidator()])

    def __str__(self):
        return f'{self.value}'


class AlarmAction(models.Model):

    """
    Model representing an action associated with a specific alarm in an AWS CloudWatch setup.

    Attributes:
    - alarm: ForeignKey to the associated Alarm instance, with CASCADE deletion.
    - action: CharField for the action type, with choices from ACTION_CHOICES 
    and a default of ACTION_OK.
    - arn: ForeignKey to the associated ARN instance, with PROTECT deletion.

    Constants:
    - ACTION_OK: 'OK'
    - ACTION_ALARM: 'ALARM'
    - ACTION_INSUFFICIENT_DATA: 'INSUFFICIENT_DATA'
    - ACTION_CHOICES: List of choices for the action type.

    Each AlarmAction instance is uniquely identified by a combination of alarm, action, and arn.
    """

    class Meta:
        """
        Meta:
        - db_table: Custom name for the database table.
        - unique_together: Ensures the combination of alarm, action, and arn is unique.
        """
        db_table = 'cloudwatch_alarm_action'
        unique_together = [['alarm', 'action', 'arn']]

    ACTION_OK = 'OK'
    ACTION_ALARM = 'ALARM'
    ACTION_INSUFFICIENT_DATA = 'INSUFFICIENT_DATA'

    ACTION_CHOICES = [
        (ACTION_OK, ACTION_OK),
        (ACTION_ALARM, ACTION_ALARM),
        (ACTION_INSUFFICIENT_DATA, ACTION_INSUFFICIENT_DATA),
    ]

    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE)
    action = models.CharField(
        max_length=55, choices=ACTION_CHOICES, default=ACTION_OK)
    arn = models.ForeignKey(AlertSource, on_delete=models.PROTECT)


class Dimension(models.Model):
    """
    Model representing an alarm-affecting resource.

    Attributes:
    - dimension_id: SmallAutoField for the dimension ID.
    - name: CharField for the name, uniquely identifying the dimension.
    - value: CharField for the AWS resource ARN.

    Each Dimension instance is uniquely identified by its name.
    """

    dimension_id = models.SmallAutoField(
        primary_key=True, auto_created=True, unique=True)
    name = models.CharField(
        max_length=255, unique=True)
    value = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f'{self.value}'


class AlermDimension(models.Model):
    """
    Model representing a relationship between an Alarm and a Dimension in the context 
    of a CloudWatch alarm dimension.

    Attributes:
    - alarm: ForeignKey to the associated Alarm instance, with CASCADE deletion and 
    related_name 'dimension'.
    - dimension: ForeignKey to the associated Dimension instance, with PROTECT deletion.

    """


    class Meta:
        """
        Meta:
        - db_table: Custom name for the database table.
        """
        db_table = 'cloudwatch_alarm_dimension'

    alarm = models.ForeignKey(
        Alarm, on_delete=models.CASCADE, related_name='dimension')
    dimension = models.ForeignKey(Dimension, on_delete=models.PROTECT)
