"""Import Django models and settings."""
from django.db import models
from django.conf import settings
from cloudwatch.models import Dimension


class Developer(models.Model):

    """
    Model representing a developer.

    Attributes:
        is_developer (bool): A flag indicating if the user is a developer.
        user (User): A one-to-one relationship with the User model from Django's auth system.
    """
        
    is_developer = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns:
            str: The username of the user associated with the developer.
        """
        return f'{self.user.username}'


class Bug(models.Model):
    """
    Model representing a bug report.

    This model stores information about a bug report, including
    a unique bug ID, whether it has been resolved, and timestamps
    for when it was created and last updated.

    Attributes:
        bug_id (str): A unique identifier for the bug.
        resolved (bool): Indicates whether the bug has been resolved.
        created_at (datetime): The timestamp for when the bug was created.
        updated_at (datetime): The timestamp for when the bug was last updated.
    """

    bug_id = models.CharField(max_length=255, primary_key=True, unique=True)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns:
            str: The bug_id.
        """
        return f'{self.bug_id}'
    
    def __json__(self):
        return {'name': self.dimension}


class BugOwner(models.Model):
    """
    Model to store the ownership of bugs by developers.

    This model represents the ownership of bugs by developers.
    Each BugOwner instance links a Developer to a Bug, indicating
    that the Developer is the owner of the Bug.
    """
    user = models.ForeignKey(Developer,
                             on_delete=models.RESTRICT)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='developers')
    created_at = models.DateTimeField(auto_now_add=True)

