import pytest
from core.models import UserAPIKey


@pytest.mark.django_db
class TestUserAPIKeyModel:

    def test_api_key_is_created_with_user(self, user):
        assert UserAPIKey.objects.filter(user=user).exists()

    def test_api_key_raw_key_is_set(self, user):
        api_key = UserAPIKey.objects.get(user=user)
        assert api_key.key is not None
        assert api_key.key != ""

    def test_api_key_user_relationship(self, user):
        api_key = UserAPIKey.objects.get(user=user)
        assert api_key.user == user

    def test_only_one_api_key_per_user(self, user):
        assert UserAPIKey.objects.filter(user=user).count() == 1

    def test_api_key_deleted_when_user_deleted(self, user):
        user_id = user.id
        user.delete()
        assert not UserAPIKey.objects.filter(user_id=user_id).exists()

    def test_api_key_accessible_via_related_name(self, user):
        assert hasattr(user, "api_keys")
        assert user.api_keys is not None
