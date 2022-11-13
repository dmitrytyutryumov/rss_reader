import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_rss_item_view(client, following_rss__item, following_rss_2__item):
    response = client.get(reverse("rss_items"))
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_rss_item_view__filter_by_1_rss(client, following_rss__item, following_rss_2__item):
    url = reverse("rss_items")
    response = client.get(f"{url}?rss={following_rss__item.rss.pk}")
    assert response.status_code == 200
    assert len(response.data) == 1
    rss_item = response.data[0]
    assert rss_item["guid"] == following_rss__item.guid
    assert rss_item["rss"] == following_rss__item.rss.pk
    assert rss_item["is_read"] is False


@pytest.mark.django_db
def test_rss_item_view__read_only(client, following_rss__item, following_rss__read_item):
    url = reverse("rss_items")
    response = client.get(f"{url}?is_read=true")
    assert response.status_code == 200
    assert len(response.data) == 1
    rss_item = response.data[0]
    assert rss_item["guid"] == following_rss__read_item.rss_item.guid
    assert rss_item["rss"] == following_rss__read_item.rss_item.rss.pk
    assert rss_item["is_read"] is True


@pytest.mark.django_db
def test_mark_as_read_rss_item(client, following_rss__item):
    response = client.post(
        reverse("rss_item_read", kwargs={"pk": following_rss__item.pk}),
        {"rss_id": following_rss__item.rss.pk},
    )
    assert response.status_code == 201
    following_rss__item.refresh_from_db()
    assert following_rss__item.userrssitemmodel_set.count() == 1


@pytest.mark.django_db
def test_mark_as_unread_rss_item(client, following_rss__read_item):
    rss_item = following_rss__read_item.rss_item
    response = client.delete(
        reverse("rss_item_read", kwargs={"pk": rss_item.pk}), {"rss_id": rss_item.rss.pk}
    )
    assert response.status_code == 204
    rss_item.refresh_from_db()
    assert rss_item.userrssitemmodel_set.count() == 0
