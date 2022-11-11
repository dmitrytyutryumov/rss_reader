from django.conf import settings
from django.db import models


class RssModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("users")


class RSSModel(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField(verbose_name="RSS source link")
    ttl = models.IntegerField(default=60, verbose_name="Refresh time range")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserRSSModel")

    objects = RssModelManager()

    class Meta:
        db_table = "rss"

    def __str__(self):
        return self.title


class UserRSSModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rss = models.ForeignKey(RSSModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_rss"

    def __str__(self):
        return self.rss.title


class RssItemModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("user_rss").select_related("rss")


class RSSItemModel(models.Model):
    guid = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    link = models.URLField(verbose_name="RSS item link")
    published_date = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(auto_now=True)

    rss = models.ForeignKey(RSSModel, on_delete=models.CASCADE)
    user_rss = models.ManyToManyField(UserRSSModel, through="UserRSSItemModel")

    objects = RssItemModelManager()

    class Meta:
        ordering = ("-last_updated",)
        db_table = "rss_item"

    def __str__(self):
        return self.title


class UserRSSItemModel(models.Model):
    following_rss = models.ForeignKey(UserRSSModel, on_delete=models.CASCADE)
    rss_item = models.ForeignKey(RSSItemModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_rss_items"
        ordering = ["-rss_item__published_date"]

    def __str__(self):
        return self.rss_item.title
