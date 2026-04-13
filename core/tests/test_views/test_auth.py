import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


SIGN_UP_URL = reverse("auth:SIGN_UP")
SIGN_IN_URL = reverse("auth:SIGN_IN")
SIGN_OUT_URL = reverse("auth:SIGN_OUT")

VALID_SIGNUP_DATA = {
    "email": "newuser@example.com",
    "password": "securepass123",
    "firstName": "John",
    "lastName": "Doe",
}


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestSignUpView:
    def test_success_returns_201(self, client, stripe_mock):
        response = client.post(SIGN_UP_URL, VALID_SIGNUP_DATA, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_success_returns_access_token(self, client, stripe_mock):
        response = client.post(SIGN_UP_URL, VALID_SIGNUP_DATA, format="json")
        assert "access" in response.data

    def test_success_returns_refresh_token(self, client, stripe_mock):
        response = client.post(SIGN_UP_URL, VALID_SIGNUP_DATA, format="json")
        assert "refresh" in response.data

    def test_duplicate_email_returns_400(self, client, user):
        # user fixture already creates testuser with test@example.com
        data = {**VALID_SIGNUP_DATA, "email": "test@example.com"}
        response = client.post(SIGN_UP_URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplicate_email_returns_error_message(self, client, user):
        data = {**VALID_SIGNUP_DATA, "email": "test@example.com"}
        response = client.post(SIGN_UP_URL, data, format="json")
        assert "message" in response.data

    def test_missing_password_returns_400(self, client, stripe_mock):
        data = {k: v for k, v in VALID_SIGNUP_DATA.items() if k != "password"}
        response = client.post(SIGN_UP_URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_first_name_returns_400(self, client, stripe_mock):
        data = {k: v for k, v in VALID_SIGNUP_DATA.items() if k != "firstName"}
        response = client.post(SIGN_UP_URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_last_name_returns_400(self, client, stripe_mock):
        data = {k: v for k, v in VALID_SIGNUP_DATA.items() if k != "lastName"}
        response = client.post(SIGN_UP_URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email_format_returns_400(self, client, stripe_mock):
        data = {**VALID_SIGNUP_DATA, "email": "not-an-email"}
        response = client.post(SIGN_UP_URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestSignInView:
    def test_valid_credentials_returns_200(self, client, user):
        response = client.post(
            SIGN_IN_URL,
            {"email": "test@example.com", "password": "testpassword123"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_valid_credentials_returns_access_token(self, client, user):
        response = client.post(
            SIGN_IN_URL,
            {"email": "test@example.com", "password": "testpassword123"},
            format="json",
        )
        assert "access" in response.data

    def test_valid_credentials_returns_refresh_token(self, client, user):
        response = client.post(
            SIGN_IN_URL,
            {"email": "test@example.com", "password": "testpassword123"},
            format="json",
        )
        assert "refresh" in response.data

    def test_wrong_password_returns_error(self, client, user):
        response = client.post(
            SIGN_IN_URL,
            {"email": "test@example.com", "password": "wrongpassword"},
            format="json",
        )
        assert response.status_code >= status.HTTP_400_BAD_REQUEST

    def test_nonexistent_user_returns_error(self, client, stripe_mock):
        response = client.post(
            SIGN_IN_URL,
            {"email": "nobody@example.com", "password": "somepassword"},
            format="json",
        )
        assert response.status_code >= status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestSignOutView:
    def test_valid_token_returns_201(self, client, user):
        refresh = RefreshToken.for_user(user)
        client.force_authenticate(user=user)
        with patch.object(RefreshToken, "blacklist"):
            response = client.post(
                SIGN_OUT_URL, {"refresh": str(refresh)}, format="json"
            )
        assert response.status_code == status.HTTP_201_CREATED

    def test_unauthenticated_returns_401(self, client, user):
        refresh = RefreshToken.for_user(user)
        response = client.post(
            SIGN_OUT_URL, {"refresh": str(refresh)}, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_valid_token_returns_success_message(self, client, user):
        refresh = RefreshToken.for_user(user)
        client.force_authenticate(user=user)
        with patch.object(RefreshToken, "blacklist"):
            response = client.post(
                SIGN_OUT_URL, {"refresh": str(refresh)}, format="json"
            )
        # Response body is a set containing the success message string
        assert len(response.data) > 0
