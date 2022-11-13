import pytest
from rss.tests.factory import (
    FeedparserResult,
    RSSItemModelFactory,
    RSSModelFactory,
    UserRSSItemModelFactory,
    UserRSSModelFactory,
)


@pytest.fixture()
def rss():
    return RSSModelFactory()


@pytest.fixture()
def following_rss(user):
    return UserRSSModelFactory(rss=RSSModelFactory(), user=user)


@pytest.fixture
def following_rss__item(following_rss):
    return RSSItemModelFactory(rss=following_rss.rss)


@pytest.fixture()
def following_rss__read_item(following_rss):
    return UserRSSItemModelFactory(
        rss_item=RSSItemModelFactory(rss=following_rss.rss), following_rss=following_rss
    )


@pytest.fixture
def following_rss_2__item(user):
    return RSSItemModelFactory(rss=UserRSSModelFactory(rss=RSSModelFactory(), user=user).rss)


@pytest.fixture
def feedparser_result():
    return FeedparserResult()
