import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


API_KEYS_URL = reverse("api_keys:ApiKeyRetrieveUpdateAPIView")


@pytest.fixture
def client():
    return APIClient()


def _auth_header(user):
    """Return Bearer token header for a user."""
    refresh = RefreshToken.for_user(user)
    return f"Bearer {str(refresh.access_token)}"


@pytest.mark.django_db
class TestApiKeyRetrieveView:
    def test_authenticated_user_returns_200(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.get(API_KEYS_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_returns_api_key_prefix(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.get(API_KEYS_URL)
        assert "prefix" in response.data

    def test_returns_api_key_name(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.get(API_KEYS_URL)
        assert "name" in response.data

    def test_api_key_belongs_to_authenticated_user(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.get(API_KEYS_URL)
        # The API key is automatically created by signal with name = username
        assert response.data["name"] == user.username

    def test_unauthenticated_returns_401(self, client):
        response = client.get(API_KEYS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
