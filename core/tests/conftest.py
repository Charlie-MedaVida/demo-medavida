import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User


@pytest.fixture
def stripe_mock():
    """Prevents live Stripe API calls triggered by the user post_save signal."""
    with patch("stripe.Customer.create", return_value=MagicMock(id="cus_test123")):
        yield


@pytest.fixture
def user(stripe_mock):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )


@pytest.fixture
def user_with_credits(user):
    user.profile.monthly_max_credit_count = 10
    user.profile.save()
    return user


@pytest.fixture
def user_without_credits(user):
    user.profile.monthly_max_credit_count = 0
    user.profile.spent_credit_count = 0
    user.profile.save()
    return user
