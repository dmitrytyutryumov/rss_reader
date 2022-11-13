import logging

from django.conf import settings
from django.core.mail import send_mail
from rss.models import RSSModel
from rss.rss_parser import RSSParser

from api import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, ignore_result=True)
def update_rss_feeds(self, *args, **kwargs) -> None:
    """
    Task updates / verify every added rss feed
    """
    for rss in RSSModel.objects.all():
        try:
            if not RSSParser(rss, force=kwargs.get("force", False)).parse():
                logger.exception(f"RSS feed {rss.link} is unavailable")
        except Exception as e:
            logger.exception(f"Failed {rss.link}", e)


@celery_app.task(bind=True, ignore_result=True)
def force_update_rss_feed(self, *args, rss_feed_id: int, user_email: str, **kwargs) -> None:
    """
    Force update 1 rss feed triggered by user
    """
    try:
        rss = RSSModel.objects.get(pk=rss_feed_id)
        if not RSSParser(rss, force=True).parse():
            send_mail(
                f"RSS feed {rss.link} is unavailable ",
                f"RSS feed {rss.link} is unavailable ",
                settings.EMAIL_HOST_USER,
                [user_email],
                fail_silently=False,
            )
    except RSSModel.DoesNotExist:
        logger.exception("Rss feed does not exist")
