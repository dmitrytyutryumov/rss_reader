import factory
from django.conf import settings
from rss.models import RSSItemModel, RSSModel, UserRSSItemModel, UserRSSModel


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL


class RSSModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RSSModel


class UserRSSModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRSSModel

    user = factory.SubFactory(UserFactory)
    rss = factory.SubFactory(RSSModelFactory)


class RSSItemModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RSSItemModel

    rss = factory.SubFactory(RSSModelFactory)


class UserRSSItemModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRSSItemModel

    following_rss = factory.SubFactory(UserRSSModelFactory)
    rss_item = factory.SubFactory(RSSItemModel)
