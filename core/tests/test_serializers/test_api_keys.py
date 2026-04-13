import pytest

from core.models import UserAPIKey
from core.serializers.api_keys import UserAPIKeySerializer


class TestUserAPIKeySerializer:

    def test_exposed_fields(self):
        assert set(UserAPIKeySerializer().fields.keys()) == {"id", "key"}

    def test_no_extra_fields_exposed(self):
        assert len(UserAPIKeySerializer().fields) == 2

    @pytest.mark.django_db
    def test_serializes_id(self, user):
        api_key = UserAPIKey.objects.get(user=user)
        data = UserAPIKeySerializer(api_key).data
        assert str(api_key.id) == data["id"]

    @pytest.mark.django_db
    def test_serializes_key(self, user):
        api_key = UserAPIKey.objects.get(user=user)
        data = UserAPIKeySerializer(api_key).data
        assert data["key"] == api_key.key

    @pytest.mark.django_db
    def test_key_is_non_empty(self, user):
        api_key = UserAPIKey.objects.get(user=user)
        data = UserAPIKeySerializer(api_key).data
        assert data["key"] not in (None, "")
