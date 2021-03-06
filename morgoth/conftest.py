import pytest

from django.test.client import Client
from rest_framework.test import APIClient

from morgoth.base.tests import UserFactory


@pytest.fixture
def api_client():
    """Fixture to provide a DRF API client."""
    user = UserFactory(is_superuser=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def client():
    """Fixture to provide Django test client."""
    user = UserFactory(is_superuser=True)
    client = Client()
    client.force_login(user=user, backend='django.contrib.auth.backends.ModelBackend')
    return client
