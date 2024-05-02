"""
Admin configuration for Bug-related models.

This module contains the admin configurations for Bug-related models:
- Bugs
- BugOwner
- Developer
"""

from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Bugs, BugOwner, Developer




class BugOwnerInline(TabularInline):
    """
    Inline editor for BugOwner model in the Django admin.

    This class provides an inline editor for the BugOwner model,
    allowing BugOwner instances to be edited inline with the parent model.
    """

    autocomplete_fields = ['user']
    model = BugOwner
    extra = 1

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "user":
    #         kwargs["queryset"] = Developer.objects.filter(user__username='dev')
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Developer model.

    This class configures the Django admin interface for the Developer model.
    It specifies the fields to be displayed in the list view (`list_display`)
    and the fields to be searched (`search_fields`).
    """
    search_fields = ['user_username']
    list_display = ['user_id', 'user']


@admin.register(Bugs)
class BugAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Bugs model.

    This class configures the Django admin interface for the Bugs model.
    It specifies the fields to be displayed in the list view (`list_display`),
    and defines a method `developers` to show the count of developers associated
    with each bug in the list display.
    """

    list_display = ['bug_id', 'resolved', 'created_at', 'developers']
    inlines = [BugOwnerInline]

    def developers(self, bug):
        """
        Return the number of developers associated with a bug.

        This method calculates and returns the count of developers
        associated with the given bug instance.

        Args:
            bug: The Bug instance for which the count of developers is to be calculated.

        Returns:
            int: The number of developers associated with the bug.
        """

        return bug.developers.count()
