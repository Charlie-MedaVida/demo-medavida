import pytest
from unittest.mock import patch, MagicMock
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers.auth import (
    SignupSerializer,
    OrigTokenObtainPairSerializer,
    OrigTokenBlockRefreshSerializer,
)


# ---------------------------------------------------------------------------
# SignupSerializer
# ---------------------------------------------------------------------------

class TestSignupSerializer:

    def test_exposed_fields(self):
        assert set(SignupSerializer().fields.keys()) == {
            "email", "password", "firstName", "lastName"
        }

    def test_email_is_write_only(self):
        assert SignupSerializer().fields["email"].write_only

    def test_password_is_write_only(self):
        assert SignupSerializer().fields["password"].write_only

    def test_first_name_is_write_only(self):
        assert SignupSerializer().fields["firstName"].write_only

    def test_last_name_is_write_only(self):
        assert SignupSerializer().fields["lastName"].write_only

    def test_valid_data_passes_validation(self):
        s = SignupSerializer(data={
            "email": "user@example.com",
            "password": "securepass123",
            "firstName": "Jane",
            "lastName": "Doe",
        })
        assert s.is_valid(), s.errors

    def test_invalid_email_fails_validation(self):
        s = SignupSerializer(data={
            "email": "not-an-email",
            "password": "securepass",
            "firstName": "Jane",
            "lastName": "Doe",
        })
        assert not s.is_valid()
        assert "email" in s.errors

    def test_missing_email_fails_validation(self):
        s = SignupSerializer(data={
            "password": "securepass",
            "firstName": "Jane",
            "lastName": "Doe",
        })
        assert not s.is_valid()
        assert "email" in s.errors

    def test_missing_password_fails_validation(self):
        s = SignupSerializer(data={
            "email": "user@example.com",
            "firstName": "Jane",
            "lastName": "Doe",
        })
        assert not s.is_valid()
        assert "password" in s.errors

    def test_missing_first_name_fails_validation(self):
        s = SignupSerializer(data={
            "email": "user@example.com",
            "password": "securepass",
            "lastName": "Doe",
        })
        assert not s.is_valid()
        assert "firstName" in s.errors

    def test_missing_last_name_fails_validation(self):
        s = SignupSerializer(data={
            "email": "user@example.com",
            "password": "securepass",
            "firstName": "Jane",
        })
        assert not s.is_valid()
        assert "lastName" in s.errors

    def test_empty_payload_reports_all_required_fields(self):
        s = SignupSerializer(data={})
        assert not s.is_valid()
        assert set(s.errors.keys()) == {"email", "password", "firstName", "lastName"}


# ---------------------------------------------------------------------------
# OrigTokenObtainPairSerializer
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestOrigTokenObtainPairSerializer:

    def test_get_token_includes_user_id_claim(self, user):
        token = OrigTokenObtainPairSerializer.get_token(user)
        assert "user_id" in token

    def test_get_token_user_id_matches_user(self, user):
        token = OrigTokenObtainPairSerializer.get_token(user)
        assert token["user_id"] == user.id

    def test_get_token_returns_a_token_object(self, user):
        token = OrigTokenObtainPairSerializer.get_token(user)
        # Token objects have a string representation (the encoded JWT)
        assert str(token) != ""


# ---------------------------------------------------------------------------
# OrigTokenBlockRefreshSerializer
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestOrigTokenBlockRefreshSerializer:

    def test_validate_blacklists_the_token(self, user):
        refresh = RefreshToken.for_user(user)
        s = OrigTokenBlockRefreshSerializer()
        with patch.object(RefreshToken, "blacklist") as mock_blacklist:
            s.validate({"refresh": str(refresh)})
        mock_blacklist.assert_called_once()

    def test_validate_returns_success_message(self, user):
        refresh = RefreshToken.for_user(user)
        s = OrigTokenBlockRefreshSerializer()
        with patch.object(RefreshToken, "blacklist"):
            result = s.validate({"refresh": str(refresh)})
        assert result == "The User has logged out succesfully"

    def test_validate_raises_for_invalid_token(self):
        s = OrigTokenBlockRefreshSerializer()
        with pytest.raises(Exception):
            s.validate({"refresh": "invalid.token.string"})
