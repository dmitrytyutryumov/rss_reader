from datetime import datetime
from time import struct_time

import factory
from django.conf import settings
from factory import fuzzy
from rss.models import RSSItemModel, RSSModel, UserRSSItemModel, UserRSSModel


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL


class RSSModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RSSModel

    link = fuzzy.FuzzyText(prefix="https://", suffix=".com", length=50)


class UserRSSModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRSSModel

    user = factory.SubFactory(UserFactory)
    rss = factory.SubFactory(RSSModelFactory)


class RSSItemModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RSSItemModel

    rss = factory.SubFactory(RSSModelFactory)
    link = fuzzy.FuzzyText(prefix="https://", suffix=".com", length=50)
    guid = fuzzy.FuzzyText(prefix="guid", length=50)


class UserRSSItemModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRSSItemModel

    following_rss = factory.SubFactory(UserRSSModelFactory)
    rss_item = factory.SubFactory(RSSItemModel)


class FuzzyStructTime(fuzzy.BaseFuzzyAttribute):
    def fuzz(self) -> struct_time:
        return datetime.utcnow().timetuple()


class FeedparserFeed(factory.DictFactory):
    title = fuzzy.FuzzyText(length=20)
    language = fuzzy.FuzzyText(length=5)
    category = fuzzy.FuzzyText(length=15)
    ttl = fuzzy.FuzzyInteger(low=10, high=60)
    updated_parsed = FuzzyStructTime()


class FeedparserEntry(factory.DictFactory):
    title = fuzzy.FuzzyText(length=20)
    link = fuzzy.FuzzyText(prefix="https://", suffix=".com", length=50)
    author = fuzzy.FuzzyText(length=5)
    id = fuzzy.FuzzyText(length=30)
    published_parsed = FuzzyStructTime()


class FeedparserResult(factory.DictFactory):
    feed = factory.SubFactory(FeedparserFeed)
    entries = factory.List([factory.SubFactory(FeedparserEntry) for _ in range(5)])
