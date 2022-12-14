import logging
import uuid
from typing import Optional, Sequence

import feedparser
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from rss.models import RSSItemModel, RSSModel
from utils import struct_time_to_datetime

logger = logging.getLogger(__name__)


class NoUpdatesException(Exception):
    ...


class RSSParser:
    """
    RSSParser parse rss link, save updates
    """

    def __init__(
        self, rss: RSSModel, max_retry: Optional[int] = 3, force: Optional[bool] = False
    ) -> None:
        self._rss = rss
        self._max_retry = max_retry
        self._force = force  # ignore rss.updated_at

    def parse(self) -> bool:
        logger.info(f"Start working on RSS {self._rss.link}")

        feed = self._get_rss_feed()
        if feed is None:
            return False

        try:
            self._parse_rss_feed(feed["feed"])
            self._parse_rss_items(feed["entries"])

            logger.info(f"Finished working on RSS {self._rss.link}")
        except NoUpdatesException:
            logger.info(f"No updates for RSS {self._rss.link}")

        return True

    def _get_rss_feed(self, retries: Optional[int] = 1) -> Optional[dict]:
        if retries > self._max_retry:
            self._rss.unavailable = timezone.now()
            self._rss.save()
            return None
        try:
            feed = feedparser.parse(self._rss.link)
            if feed.get("bozo"):
                logger.exception(feed["bozo_exception"])
                raise feed["bozo_exception"]
            return feed
        except Exception:
            return self._get_rss_feed(retries=retries + 1)

    def _parse_rss_feed(self, feed: dict) -> RSSModel:
        updated_at = feed.get("updated_parsed")
        if updated_at:
            updated_at = struct_time_to_datetime(updated_at, tz=get_current_timezone())
            if not self._force and updated_at.timestamp() <= self._rss.updated_at.timestamp():
                raise NoUpdatesException
            self._rss.updated_at = updated_at

        self._rss.title = feed["title"]
        self._rss.language = feed.get("language") or self._rss.language
        self._rss.category = feed.get("category") or self._rss.category
        try:
            self._rss.ttl = int(feed.get("ttl")) or self._rss.ttl
        except (TypeError, ValueError):
            logger.warning(
                f"RSS {self._rss.pk} - {self._rss.title} has incorrect ttl {feed.get('ttl')}"
            )

        self._rss.unavailable = None

        self._rss.save(
            update_fields=(
                "title",
                "language",
                "category",
                "ttl",
                "updated_at",
                "unavailable",
            )
        )
        return self._rss

    def _parse_rss_items(self, items: Sequence[dict]) -> None:
        rss_items = []
        for item in items:
            published = item.get("published_parsed")
            if published:
                published = struct_time_to_datetime(published, tz=get_current_timezone())
            rss_items.append(
                RSSItemModel(
                    rss=self._rss,
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
