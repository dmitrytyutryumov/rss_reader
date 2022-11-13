from datetime import timedelta
from unittest import mock

import pytest
from django.contrib.auth.models import User
from django.test import override_settings
from django.utils.timezone import get_current_timezone
from rss.models import RSSModel
from rss.tasks import force_update_rss_feed, update_rss_feeds
from utils import struct_time_to_datetime


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_update_rss_feeds(rss: RSSModel, feedparser_result: dict):
    with mock.patch("feedparser.parse") as mock_parse:
        rss.updated_at = rss.updated_at - timedelta(minutes=10)
        rss.save()
        mock_parse.return_value = feedparser_result
        update_rss_feeds()
        rss.refresh_from_db()

        assert rss.title == feedparser_result["feed"]["title"]
        assert rss.language == feedparser_result["feed"]["language"]
        assert rss.category == feedparser_result["feed"]["category"]
        assert rss.ttl == feedparser_result["feed"]["ttl"]
        assert rss.updated_at == struct_time_to_datetime(
            feedparser_result["feed"]["updated_parsed"], tz=get_current_timezone()
        )
        assert rss.rssitemmodel_set.count() == 5


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_update_rss_feeds__no_updates(rss: RSSModel, feedparser_result: dict):
    with mock.patch("feedparser.parse") as mock_parse:
        rss.updated_at = struct_time_to_datetime(
            feedparser_result["feed"]["updated_parsed"], tz=get_current_timezone()
        )
        rss.save()
        mock_parse.return_value = feedparser_result
        update_rss_feeds()
        rss.refresh_from_db()
        assert rss.title != feedparser_result["feed"]["title"]
        assert rss.rssitemmodel_set.count() == 0


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_update_rss_feeds__incorrect_ttl(rss: RSSModel, feedparser_result: dict):
    with mock.patch("feedparser.parse") as mock_parse:
        rss.updated_at = rss.updated_at - timedelta(minutes=10)
        rss.save()
        feedparser_result["feed"]["ttl"] = "!@#asd"
        mock_parse.return_value = feedparser_result
        update_rss_feeds()
        rss.refresh_from_db()
        assert rss.title == feedparser_result["feed"]["title"]
        assert rss.ttl == 60


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_update_rss_feeds__items(rss: RSSModel, feedparser_result: dict):
    with mock.patch("feedparser.parse") as mock_parse:
        rss.updated_at = rss.updated_at - timedelta(minutes=10)
        rss.save()
        feedparser_entry = feedparser_result["entries"][0]
        feedparser_result["entries"] = [feedparser_entry]
        mock_parse.return_value = feedparser_result
        update_rss_feeds()
        rss.refresh_from_db()

        assert rss.title == feedparser_result["feed"]["title"]
        assert rss.rssitemmodel_set.count() == 1

        rss_item = rss.rssitemmodel_set.get()
        assert rss_item.title == feedparser_entry["title"]
        assert rss_item.link == feedparser_entry["link"]
        assert rss_item.author == feedparser_entry["author"]
        assert rss_item.guid == feedparser_entry["id"]
        assert rss_item.published_date == struct_time_to_datetime(
            feedparser_entry["published_parsed"], tz=get_current_timezone()
        )


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_force_update_rss_feed(user: User, rss: RSSModel, feedparser_result: dict):
    with mock.patch("feedparser.parse") as mock_parse:
        rss.updated_at = rss.updated_at - timedelta(minutes=10)
        rss.save()
        mock_parse.return_value = feedparser_result
        force_update_rss_feed(rss_feed_id=rss.pk, user_email=user.email)
        rss.refresh_from_db()

        assert rss.title == feedparser_result["feed"]["title"]
        assert rss.rssitemmodel_set.count() == 5


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_force_update_rss_feed__failed(user: User, rss: RSSModel):
    with mock.patch("rss.tasks.send_mail") as mock_send_mail:
        force_update_rss_feed(rss_feed_id=rss.pk, user_email=user.email)
        mock_send_mail.assert_called_once()
        rss.refresh_from_db()
        assert rss.unavailable is not None
