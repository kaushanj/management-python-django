import pytest
from django.contrib.admin.sites import AdminSite
from bugmanager.admin import BugAdmin
from bugmanager.models import Bug, Developer


@pytest.fixture
def bug_admin():
    """
    Fixture to create an instance of BugAdmin for testing.
    """
    admin_site = AdminSite()
    return BugAdmin(Bug, admin_site)


@pytest.mark.django_db
class TestBugModel:
    """
    Test cases for the BugAdmin model.
    """

    def test_not_allow_to_add_to_any_user(self, bug_admin):
        """
        Test that it does not allow adding bugs to any user.
        """
        admin_user = Developer.objects.filter(user__username='Admin').first()
        assert not bug_admin.has_add_permission(admin_user)
