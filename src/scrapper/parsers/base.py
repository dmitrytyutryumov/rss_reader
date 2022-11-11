import dataclasses
import uuid
from datetime import datetime
from time import mktime
from typing import Optional, Sequence

import feedparser


@dataclasses.dataclass
class RSSItem:
    title: str
    link: str
    guid: str
    published_date: Optional[datetime]
    media_content: Optional[list[dict]]


@dataclasses.dataclass
class RSSSource:
    name: str
    link: str
    last_updated: datetime
    published_date: datetime


class RSSParser:
    source = None

    def run(self):
        feed = feedparser.parse(self.source)
        items = self._parse_items(feed["entries"])
        return items

    def _parse_items(self, items: list[dict]) -> Sequence[RSSItem]:
        rss_items = []
        for item in items:
            published = item.get("published_parsed")
            if published:
                published = datetime.fromtimestamp(mktime(published))
            rss_items.append(
                RSSItem(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    guid=item.get("id", uuid.uuid4().hex),
                    published_date=published,
                    media_content=item.get("media_content"),
                )
            )
        return rss_items
