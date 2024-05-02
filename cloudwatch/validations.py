"""
imports the RegexValidator class from Django's core.validators module
"""
from django.core.validators import RegexValidator


class ARNValidator(RegexValidator):
    """
    Validator for AWS ARN (Amazon Resource Name).

    This validator checks whether a given value matches the format of an AWS ARN.
    An AWS ARN (Amazon Resource Name) is a unique identifier for AWS resources.
    The format of an ARN is 'arn:aws:service:region:account-id:resource-id'.

    The regex pattern used in this validator matches the format of an ARN for an
    AWS Connect instance. It ensures that the ARN starts with 'arn:aws:connect:'
    followed by a specific pattern for the AWS account ID and instance ID.

    Example ARN pattern:
    arn:aws:connect:us-west-2:123456789012:instance/abcdef12-3456-7890-abcd-ef1234567890
    """

    regex = r'^arn:aws:(sns:[a-z0-9-]+:\d{12}:[a-zA-Z0-9-_]+|[a-z0-9-]+:[a-z0-9-]+:\d{12}:[a-z0-9]+:[a-zA-Z0-9-_]+)$'
    message = "Invalid AWS ARN"
    code = 'Invalid_ARN'
