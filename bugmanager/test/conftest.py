import pytest
from model_bakery import baker
from bugmanager.models import Bug, Dimension

@pytest.fixture
def bug_instence():
    bimension = baker.make(Dimension)
    return baker.make(Bug, dimension=bimension)
