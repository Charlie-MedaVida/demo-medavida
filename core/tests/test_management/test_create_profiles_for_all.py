import io
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from core.models import Profile


User = get_user_model()


def _create_user_without_profile(username, email):
    """Create a user and remove the Profile created by the post_save signal."""
    with patch("stripe.Customer.create", return_value=MagicMock(id="cus_test")):
        user = User.objects.create_user(username=username, email=email, password="pass")
    Profile.objects.filter(user=user).delete()
    return user


@pytest.mark.django_db
class TestCreateProfilesForAllCommand:
    def test_creates_profile_for_user_without_one(self):
        user = _create_user_without_profile("noprofile", "noprofile@example.com")
        assert not Profile.objects.filter(user=user).exists()

        call_command("create_profiles_for_all", stdout=io.StringIO())

        assert Profile.objects.filter(user=user).exists()

    def test_creates_profiles_for_multiple_users(self):
        user1 = _create_user_without_profile("noprofile1", "noprofile1@example.com")
        user2 = _create_user_without_profile("noprofile2", "noprofile2@example.com")

        call_command("create_profiles_for_all", stdout=io.StringIO())

        assert Profile.objects.filter(user=user1).exists()
        assert Profile.objects.filter(user=user2).exists()

    def test_skips_users_who_already_have_profiles(self, user):
        # user fixture creates a user with a Profile via signal
        existing_profile = Profile.objects.get(user=user)

        call_command("create_profiles_for_all", stdout=io.StringIO())

        assert Profile.objects.filter(user=user).count() == 1
        assert Profile.objects.get(user=user).pk == existing_profile.pk

    def test_created_profile_is_linked_to_correct_user(self):
        user = _create_user_without_profile("noprofile", "noprofile@example.com")

        call_command("create_profiles_for_all", stdout=io.StringIO())

        profile = Profile.objects.get(user=user)
        assert profile.user == user

    def test_outputs_created_message_when_profiles_created(self):
        _create_user_without_profile("noprofile", "noprofile@example.com")
        out = io.StringIO()

        call_command("create_profiles_for_all", stdout=out)

        assert "User Profiles Created" in out.getvalue()

    def test_outputs_already_has_profile_message_when_all_have_profiles(self, user):
        # user fixture user already has a profile
        out = io.StringIO()

        call_command("create_profiles_for_all", stdout=out)

        assert "All Users already have Profiles" in out.getvalue()

    def test_raises_command_error_on_exception(self):
        with patch(
            "core.management.commands.create_profiles_for_all.get_user_model"
        ) as mock_get_user_model:
            mock_model = MagicMock()
            mock_model.objects.filter.return_value.all.side_effect = Exception("DB error")
            mock_get_user_model.return_value = mock_model
            with pytest.raises(CommandError):
                call_command("create_profiles_for_all")
