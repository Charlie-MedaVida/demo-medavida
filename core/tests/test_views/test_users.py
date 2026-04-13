import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


USER_ME_URL = reverse("users:USER_RETRIEVE_UPDATE_DESTROY")
DASHBOARD_URL = reverse("users:DashboardRetrieveAPIView")


@pytest.fixture
def client():
    return APIClient()


def _auth_header(user):
    """Return Bearer token header for a user."""
    refresh = RefreshToken.for_user(user)
    return f"Bearer {str(refresh.access_token)}"


@pytest.mark.django_db
class TestUserRetrieveView:
    def test_authenticated_user_returns_200(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(USER_ME_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_returns_user_id(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(USER_ME_URL)
        assert response.data["id"] == user.id

    def test_returns_email(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(USER_ME_URL)
        assert response.data["email"] == user.email

    def test_returns_profile_credit_count(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(USER_ME_URL)
        assert "profile" in response.data
        assert "credit_count" in response.data["profile"]

    def test_unauthenticated_returns_401(self, client):
        response = client.get(USER_ME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserUpdateView:
    def test_patch_first_name_returns_200(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.patch(USER_ME_URL, {"first_name": "Updated"}, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_patch_updates_first_name(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        client.patch(USER_ME_URL, {"first_name": "Updated"}, format="json")
        user.refresh_from_db()
        assert user.first_name == "Updated"

    def test_patch_last_name_returns_200(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.patch(USER_ME_URL, {"last_name": "Smith"}, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_patch_returns_updated_data(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.patch(USER_ME_URL, {"first_name": "NewFirst"}, format="json")
        assert response.data["first_name"] == "NewFirst"

    def test_patch_unauthenticated_returns_401(self, client):
        response = client.patch(USER_ME_URL, {"first_name": "Updated"}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserDeleteView:
    def test_delete_returns_400_due_to_serializer_bug(self, client, user):
        """
        Known bug: the view passes {'user_id': id} to UserDeleteSerializer,
        but UserDeleteSerializer requires a 'password' field. Because the
        required field is missing, is_valid() always raises a ValidationError,
        causing the endpoint to always return 400 instead of deleting the user.
        """
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.delete(USER_ME_URL)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_does_not_remove_user_due_to_bug(self, client, user):
        from django.contrib.auth.models import User

        user_id = user.id
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        client.delete(USER_ME_URL)
        # User still exists because the delete path always fails validation
        assert User.objects.filter(id=user_id).exists()


@pytest.mark.django_db
class TestDashboardRetrieveView:
    def test_authenticated_user_returns_200(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.get(DASHBOARD_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_returns_user_data(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.get(DASHBOARD_URL)
        assert response.data["id"] == user.id
        assert response.data["email"] == user.email

    def test_returns_profile(self, client, user):
        client.credentials(HTTP_AUTHORIZATION=_auth_header(user))
        response = client.get(DASHBOARD_URL)
        assert "profile" in response.data
