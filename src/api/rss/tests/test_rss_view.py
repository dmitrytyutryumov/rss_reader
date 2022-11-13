from unittest import mock

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_rss_view__all(client, rss, following_rss):
    response = client.get(reverse("rss_list"))
    assert response.status_code == 200
    rss_feeds = response.data
    assert len(rss_feeds) == 2


@pytest.mark.django_db
def test_rss_view__followed_only(client, rss, following_rss):
    url = reverse("rss_list")
    response = client.get(f"{url}?following=true")
    assert response.status_code == 200
    rss_feeds = response.data
    assert len(rss_feeds) == 1
    assert rss_feeds[0]["id"] == following_rss.rss.pk
    assert rss_feeds[0]["following"] is True


@pytest.mark.django_db
def test_rss_follow(client, user, rss):
    response = client.post(reverse("rss_follow"), {"id": rss.pk})
    assert response.status_code == 201
    rss.refresh_from_db()
    assert rss.users.get() == user


@pytest.mark.django_db
def test_rss_unfollow(client, following_rss):
    rss = following_rss.rss
    response = client.delete(reverse("rss_follow"), {"id": rss.pk})
    assert response.status_code == 204
    rss.refresh_from_db()
    assert rss.users.count() == 0


@pytest.mark.django_db
def test_rss_force_update(client, user, rss):
    with mock.patch("rss.views.rss_views.force_update_rss_feed.delay") as mock_update_task:
        response = client.post(reverse("rss_force_update"), {"id": rss.pk})
        assert response.status_code == 200
        mock_update_task.assert_called_once()
        mock_update_task.assert_called_with(rss_feed_id=rss.pk, user_email=user.email)
