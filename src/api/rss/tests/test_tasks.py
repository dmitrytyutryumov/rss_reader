from unittest import mock

import pytest
from django.test import override_settings
from rss.models import RSSModel
from rss.tasks import update_rss_feeds

# Create your tests here.


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
# @mock.patch('feedparser.parse', mock.MagicMock())
def test_update_rss_feeds_task__1_rss(rss):
    rss = RSSModel.objects.get(link="https://feeds.feedburner.com/tweakers/mixed")
    update_rss_feeds(rss_feed_id=rss.pk)
    update_rss_feeds(rss_feed_id=rss.pk)
    update_rss_feeds(rss_feed_id=rss.pk)
