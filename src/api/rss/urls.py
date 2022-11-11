from django.urls import path

from .views import (
    ForceRssUpdate,
    UserReadRSSItemView,
    UserRSSFollowingView,
    UserRSSItemView,
    UserRSSView,
)

urlpatterns = [
    path("", UserRSSView.as_view()),
    path("update", ForceRssUpdate.as_view()),
    path("follow", UserRSSFollowingView.as_view()),
    path("items/", UserRSSItemView.as_view()),
    path("items/<int:pk>", UserReadRSSItemView.as_view()),
]
