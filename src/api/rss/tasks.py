import logging
import uuid
from typing import Optional, Sequence

import feedparser
from django.utils.timezone import get_current_timezone
from rss.models import RSSItemModel, RSSModel
from utils import struct_time_to_datetime

from api import celery_app

logger = logging.getLogger(__name__)


class NoUpdatesException(Exception):
    ...


@celery_app.task(bind=True, ignore_result=True)
def update_rss_feeds(self, *args, rss_feed_id: Optional[int] = None, **kwargs) -> None:
    if rss_feed_id:
        try:
            rss = RSSModel.objects.get(pk=rss_feed_id)
            _parse_rss_feed(rss)
            return
        except RSSModel.DoesNotExist:
            logger.exception("Rss feed does not exist")
    else:
        for rss in RSSModel.objects.all():
            try:
                _parse_rss_feed(rss)
            except Exception as e:
                logger.exception(f"Failed {rss.link}", e)


def _parse_rss_feed(rss: RSSModel) -> None:
    feed = feedparser.parse(rss.link)
    logger.info(f"Start working on RSS {rss.link}")
    try:
        _update_rss_feed(rss, feed["feed"])
        _parse_rss_items(rss, feed["entries"])
    except NoUpdatesException:
        logger.info(f"No updates for RSS {rss.link}")
    finally:
        logger.info(f"Finished working on RSS {rss.link}")


def _update_rss_feed(rss_model: RSSModel, feed: dict) -> RSSModel:
    updated_at = feed.get("updated_parsed")
    if updated_at:
        updated_at = struct_time_to_datetime(updated_at, tz=get_current_timezone())
        if updated_at.timestamp() <= rss_model.updated_at.timestamp():
            raise NoUpdatesException
        rss_model.updated_at = updated_at

    rss_model.title = feed["title"]
    rss_model.language = feed.get("language") or rss_model.language
    rss_model.category = feed.get("category") or rss_model.category
    try:
        rss_model.ttl = int(feed.get("ttl")) or rss_model.ttl
    except (TypeError, ValueError):
        logger.warning(
            f"RSS {rss_model.pk} - {rss_model.title} has incorrect ttl {feed.get('ttl')}"
        )

    rss_model.save(
        update_fields=(
            "title",
            "language",
            "category",
            "ttl",
            "updated_at",
        )
    )
    return rss_model


def _parse_rss_items(rss: RSSModel, items: Sequence[dict]):
    rss_items = []
    for item in items:
        published = item.get("published_parsed")
        if published:
            published = struct_time_to_datetime(published, tz=get_current_timezone())
        rss_items.append(
            RSSItemModel(
                rss=rss,
                title=item["title"],
                link=item["link"],
                author=item.get("author", ""),
                guid=item.get("id", uuid.uuid4().hex),
                published_date=published,
            )
        )
    return RSSItemModel.objects.bulk_create(
        rss_items,
        update_conflicts=True,
        update_fields=(
            "title",
            "link",
            "author",
            "published_date",
        ),
        unique_fields=("guid",),
    )
