from django.core.management.base import BaseCommand
from rss.models import RSSModel
from rss.tasks import update_rss_feeds

RSS_DEFAULT_SOURCES = {
    "Algemeen": "http://www.nu.nl/rss/Algemeen",
    "Tweakers": "https://feeds.feedburner.com/tweakers/mixed",
    "Cnn": "http://rss.cnn.com/rss/edition.rss",
}


class Command(BaseCommand):
    help = "Add default rss feeds"

    def handle(self, *args, **options) -> None:
        RSSModel.objects.bulk_create(
            [RSSModel(title=title, link=link) for title, link in RSS_DEFAULT_SOURCES.items()]
        )
        update_rss_feeds.delay(force=True)
        self.stdout.write(self.style.SUCCESS("Default rss successfully added"))
