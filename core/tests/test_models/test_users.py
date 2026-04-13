import pytest
from core.models import Profile


@pytest.mark.django_db
class TestProfileModel:

    def test_profile_is_created_with_user(self, user):
        assert Profile.objects.filter(user=user).exists()

    def test_default_credit_count_is_zero(self, user):
        assert user.profile.credit_count == 0

    def test_default_spent_credit_count_is_zero(self, user):
        assert user.profile.spent_credit_count == 0

    def test_default_monthly_max_credit_count_is_zero(self, user):
        assert user.profile.monthly_max_credit_count == 0

    def test_str_returns_profile_of_username(self, user):
        assert str(user.profile) == f"Profile of {user.username}"

    def test_profile_deleted_when_user_deleted(self, user):
        profile_id = user.profile.id
        user.delete()
        assert not Profile.objects.filter(id=profile_id).exists()

    def test_credit_count_is_computed_from_monthly_max_and_spent(self, user):
        user.profile.monthly_max_credit_count = 10
        user.profile.spent_credit_count = 3
        user.profile.save()
        user.profile.refresh_from_db()
        assert user.profile.credit_count == 7

    def test_credit_count_is_zero_when_fully_spent(self, user):
        user.profile.monthly_max_credit_count = 5
        user.profile.spent_credit_count = 5
        user.profile.save()
        user.profile.refresh_from_db()
        assert user.profile.credit_count == 0

    def test_credit_count_is_negative_when_overspent(self, user):
        user.profile.monthly_max_credit_count = 0
        user.profile.spent_credit_count = 3
        user.profile.save()
        user.profile.refresh_from_db()
        assert user.profile.credit_count == -3

    def test_monthly_max_credit_count_can_be_updated(self, user):
        user.profile.monthly_max_credit_count = 50
        user.profile.save()
        user.profile.refresh_from_db()
        assert user.profile.monthly_max_credit_count == 50

    def test_spent_credit_count_can_be_updated(self, user):
        user.profile.spent_credit_count = 4
        user.profile.save()
        user.profile.refresh_from_db()
        assert user.profile.spent_credit_count == 4

    def test_profile_accessible_via_related_name(self, user):
        assert hasattr(user, "profile")
        assert user.profile is not None

    def test_only_one_profile_per_user(self, user):
        assert Profile.objects.filter(user=user).count() == 1
