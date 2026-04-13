import io
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from core.models.api_keys import UserAPIKey


User = get_user_model()


def _create_user_without_api_key(username, email):
    """Create a user and remove the API key created by the post_save signal."""
    with patch("stripe.Customer.create", return_value=MagicMock(id="cus_test")):
        user = User.objects.create_user(username=username, email=email, password="pass")
    UserAPIKey.objects.filter(user=user).delete()
    return user


@pytest.mark.django_db
class TestCreateApiKeysForAllCommand:
    def test_creates_api_key_for_user_without_one(self):
        user = _create_user_without_api_key("nokey", "nokey@example.com")
        assert not UserAPIKey.objects.filter(user=user).exists()

        call_command("create_api_keys_for_all", stdout=io.StringIO())

        assert UserAPIKey.objects.filter(user=user).exists()

    def test_creates_api_key_with_username_as_name(self):
        user = _create_user_without_api_key("nokey", "nokey@example.com")

        call_command("create_api_keys_for_all", stdout=io.StringIO())

        api_key = UserAPIKey.objects.get(user=user)
        assert api_key.name == user.username

    def test_creates_api_keys_for_multiple_users(self):
        user1 = _create_user_without_api_key("nokey1", "nokey1@example.com")
        user2 = _create_user_without_api_key("nokey2", "nokey2@example.com")

        call_command("create_api_keys_for_all", stdout=io.StringIO())

        assert UserAPIKey.objects.filter(user=user1).exists()
        assert UserAPIKey.objects.filter(user=user2).exists()

    def test_skips_users_who_already_have_api_keys(self, user):
        # user fixture creates a user with an API key via signal
        existing_key = UserAPIKey.objects.get(user=user)

        call_command("create_api_keys_for_all", stdout=io.StringIO())

        assert UserAPIKey.objects.filter(user=user).count() == 1
        assert UserAPIKey.objects.get(user=user).pk == existing_key.pk

    def test_outputs_created_message_when_keys_created(self):
        _create_user_without_api_key("nokey", "nokey@example.com")
        out = io.StringIO()

        call_command("create_api_keys_for_all", stdout=out)

        assert "Api Keys Created" in out.getvalue()

    def test_outputs_already_has_key_message_when_all_have_keys(self, user):
        # user fixture user already has an API key
        out = io.StringIO()

        call_command("create_api_keys_for_all", stdout=out)

        assert "All Users already have Api Key" in out.getvalue()

    def test_raises_command_error_on_exception(self):
        with patch(
            "core.management.commands.create_api_keys_for_all.get_user_model"
        ) as mock_get_user_model:
            mock_model = MagicMock()
            mock_model.objects.filter.return_value.all.side_effect = Exception("DB error")
            mock_get_user_model.return_value = mock_model
            with pytest.raises(CommandError):
                call_command("create_api_keys_for_all")
