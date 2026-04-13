import pytest
from unittest.mock import MagicMock

from core.serializers.users import ProfileSerializer, UserSerializer, UserDeleteSerializer
from core.serializers.api_keys import UserAPIKeySerializer


# ---------------------------------------------------------------------------
# ProfileSerializer
# ---------------------------------------------------------------------------

class TestProfileSerializer:

    def test_exposed_fields(self):
        assert set(ProfileSerializer().fields.keys()) == {"credit_count"}

    def test_no_extra_fields_exposed(self):
        assert len(ProfileSerializer().fields) == 1

    @pytest.mark.django_db
    def test_serializes_credit_count(self, user):
        user.profile.monthly_max_credit_count = 7
        user.profile.spent_credit_count = 0
        user.profile.save()
        data = ProfileSerializer(user.profile).data
        assert data["credit_count"] == 7

    @pytest.mark.django_db
    def test_default_credit_count_is_zero(self, user):
        data = ProfileSerializer(user.profile).data
        assert data["credit_count"] == 0


# ---------------------------------------------------------------------------
# UserSerializer
# ---------------------------------------------------------------------------

class TestUserSerializer:

    def test_exposed_fields(self):
        expected = {"id", "username", "email", "first_name", "last_name", "profile", "api_keys"}
        assert set(UserSerializer().fields.keys()) == expected

    def test_id_is_read_only(self):
        assert UserSerializer().fields["id"].read_only

    def test_username_is_read_only(self):
        assert UserSerializer().fields["username"].read_only

    def test_email_is_writable(self):
        assert not UserSerializer().fields["email"].read_only

    def test_first_name_is_writable(self):
        assert not UserSerializer().fields["first_name"].read_only

    def test_last_name_is_writable(self):
        assert not UserSerializer().fields["last_name"].read_only

    def test_profile_is_nested_profile_serializer(self):
        assert isinstance(UserSerializer().fields["profile"], ProfileSerializer)

    def test_profile_is_read_only(self):
        assert UserSerializer().fields["profile"].read_only

    def test_api_keys_is_nested_api_key_serializer(self):
        assert isinstance(UserSerializer().fields["api_keys"], UserAPIKeySerializer)

    def test_api_keys_is_read_only(self):
        assert UserSerializer().fields["api_keys"].read_only

    @pytest.mark.django_db
    def test_serializes_username(self, user):
        data = UserSerializer(user).data
        assert data["username"] == user.username

    @pytest.mark.django_db
    def test_serializes_email(self, user):
        data = UserSerializer(user).data
        assert data["email"] == user.email

    @pytest.mark.django_db
    def test_serializes_nested_profile(self, user):
        user.profile.monthly_max_credit_count = 5
        user.profile.spent_credit_count = 0
        user.profile.save()
        data = UserSerializer(user).data
        assert data["profile"]["credit_count"] == 5

    @pytest.mark.django_db
    def test_serializes_nested_api_keys(self, user):
        data = UserSerializer(user).data
        assert "id" in data["api_keys"]
        assert "key" in data["api_keys"]

    @pytest.mark.django_db
    def test_partial_update_email(self, user):
        s = UserSerializer(user, data={"email": "updated@example.com"}, partial=True)
        assert s.is_valid(), s.errors
        s.save()
        user.refresh_from_db()
        assert user.email == "updated@example.com"

    @pytest.mark.django_db
    def test_partial_update_first_name(self, user):
        s = UserSerializer(user, data={"first_name": "Alice"}, partial=True)
        assert s.is_valid(), s.errors
        s.save()
        user.refresh_from_db()
        assert user.first_name == "Alice"

    @pytest.mark.django_db
    def test_partial_update_last_name(self, user):
        s = UserSerializer(user, data={"last_name": "Smith"}, partial=True)
        assert s.is_valid(), s.errors
        s.save()
        user.refresh_from_db()
        assert user.last_name == "Smith"

    @pytest.mark.django_db
    def test_read_only_fields_are_ignored_on_update(self, user):
        original_username = user.username
        s = UserSerializer(user, data={"username": "hacker"}, partial=True)
        assert s.is_valid(), s.errors
        s.save()
        user.refresh_from_db()
        assert user.username == original_username

    @pytest.mark.django_db
    def test_invalid_email_fails_validation(self, user):
        s = UserSerializer(user, data={"email": "not-an-email"}, partial=True)
        assert not s.is_valid()
        assert "email" in s.errors


# ---------------------------------------------------------------------------
# UserDeleteSerializer
# ---------------------------------------------------------------------------

class TestUserDeleteSerializer:

    def test_exposed_fields(self):
        assert set(UserDeleteSerializer().fields.keys()) == {"password"}

    def test_password_is_write_only(self):
        assert UserDeleteSerializer().fields["password"].write_only

    def test_password_is_required(self):
        s = UserDeleteSerializer(data={})
        assert not s.is_valid()
        assert "password" in s.errors

    @pytest.mark.django_db
    def test_valid_password_passes_validation(self, user):
        request = MagicMock()
        request.user = user
        s = UserDeleteSerializer(
            data={"password": "testpassword123"},
            context={"request": request},
        )
        assert s.is_valid(), s.errors

    @pytest.mark.django_db
    def test_incorrect_password_fails_validation(self, user):
        request = MagicMock()
        request.user = user
        s = UserDeleteSerializer(
            data={"password": "wrongpassword"},
            context={"request": request},
        )
        assert not s.is_valid()
        assert "password" in s.errors

    @pytest.mark.django_db
    def test_incorrect_password_error_message(self, user):
        request = MagicMock()
        request.user = user
        s = UserDeleteSerializer(
            data={"password": "wrongpassword"},
            context={"request": request},
        )
        s.is_valid()
        assert "Incorrect password." in str(s.errors["password"])
