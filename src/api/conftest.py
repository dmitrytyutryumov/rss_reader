import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from rss.tests.factory import UserFactory


@pytest.fixture()
def user(transactional_db):
    return UserFactory()


@pytest.fixture(autouse=True)
def client(user):
    client = APIClient(enforce_csrf_checks=True)
    client.credentials()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(user)}")
    return client
