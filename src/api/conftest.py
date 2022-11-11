import pytest
from rss.tests.factory import RSSItemModelFactory, RSSModelFactory, UserFactory


@pytest.fixture(autouse=True)
def user():
    return UserFactory()


@pytest.fixture(autouse=True)
def rss():
    return RSSModelFactory()


@pytest.fixture
def rss_item():
    return RSSItemModelFactory()
