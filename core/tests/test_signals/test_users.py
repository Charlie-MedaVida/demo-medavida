import pytest
from unittest.mock import patch, MagicMock, call
from django.contrib.auth.models import User

from core.models import UserAPIKey, Profile


def create_user(username="signaluser", email="signal@example.com", password="pass"):
    """Creates a User with Stripe mocked, triggering the post_save signal."""
    with patch("stripe.Customer.create", return_value=MagicMock(id="cus_test")):
        return User.objects.create_user(username=username, email=email, password=password)


# ---------------------------------------------------------------------------
# Profile creation
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestProfileCreatedOnUserCreate:

    def test_profile_is_created(self):
        user = create_user()
        assert Profile.objects.filter(user=user).exists()

    def test_exactly_one_profile_per_user(self):
        user = create_user()
        assert Profile.objects.filter(user=user).count() == 1

    def test_profile_has_default_credit_count(self):
        user = create_user()
        assert user.profile.credit_count == 0

    def test_profile_not_created_on_update(self):
        user = create_user()
        profile_count_before = Profile.objects.filter(user=user).count()

        user.email = "updated@example.com"
        user.save()

        assert Profile.objects.filter(user=user).count() == profile_count_before


# ---------------------------------------------------------------------------
# UserAPIKey creation
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestUserAPIKeyCreatedOnUserCreate:

    def test_api_key_is_created(self):
        user = create_user("keyuser")
        assert UserAPIKey.objects.filter(user=user).exists()

    def test_exactly_one_api_key_per_user(self):
        user = create_user("onekey")
        assert UserAPIKey.objects.filter(user=user).count() == 1

    def test_raw_key_is_stored_on_the_instance(self):
        user = create_user("storedkey")
        api_key = UserAPIKey.objects.get(user=user)
        assert api_key.key is not None
        assert api_key.key != ""

    def test_api_key_name_matches_username(self):
        user = create_user("namedkey")
        api_key = UserAPIKey.objects.get(user=user)
        assert api_key.name == "namedkey"

    def test_api_key_not_created_on_update(self):
        user = create_user("updatekey")
        key_count_before = UserAPIKey.objects.filter(user=user).count()

        user.email = "updated@example.com"
        user.save()

        assert UserAPIKey.objects.filter(user=user).count() == key_count_before


# ---------------------------------------------------------------------------
# Stripe customer creation
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestStripeCustomerCreatedOnUserCreate:

    def test_stripe_customer_create_is_called(self):
        with patch("stripe.Customer.create", return_value=MagicMock()) as mock_create:
            User.objects.create_user(
                username="stripeuser",
                email="stripe@example.com",
                password="pass",
            )
        mock_create.assert_called_once()

    def test_stripe_customer_create_called_with_username(self):
        with patch("stripe.Customer.create", return_value=MagicMock()) as mock_create:
            User.objects.create_user(
                username="stripecheck",
                email="stripe@example.com",
                password="pass",
            )
        _, kwargs = mock_create.call_args
        assert kwargs["name"] == "stripecheck"

    def test_stripe_not_called_on_update(self):
        user = create_user("norestripe")

        with patch("stripe.Customer.create", return_value=MagicMock()) as mock_create:
            user.email = "updated@example.com"
            user.save()

        mock_create.assert_not_called()
