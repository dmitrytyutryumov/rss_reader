from django.urls import path

from .views import (
    ForceRssUpdate,
    UserReadRSSItemView,
    UserRSSFollowingView,
    UserRSSItemView,
    UserRSSView,
)

urlpatterns = [
    path("", UserRSSView.as_view(), name="rss_list"),
    path("update", ForceRssUpdate.as_view(), name="rss_force_update"),
    path("follow", UserRSSFollowingView.as_view(), name="rss_follow"),
    path("items/", UserRSSItemView.as_view(), name="rss_items"),
    path("items/<int:pk>", UserReadRSSItemView.as_view(), name="rss_item_read"),
]
