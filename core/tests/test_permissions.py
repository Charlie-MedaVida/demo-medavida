import pytest
from unittest.mock import MagicMock, patch
from rest_framework import status

from core.models import UserAPIKey
from core.permissions import check_user_has_credits, HasUserAPIKey, GuardianObjectPermissions


# ---------------------------------------------------------------------------
# check_user_has_credits
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestCheckUserHasCredits:

    def test_returns_none_when_credits_available(self, user_with_credits):
        assert check_user_has_credits(user_with_credits) is None

    def test_returns_response_when_zero_credits(self, user_without_credits):
        assert check_user_has_credits(user_without_credits) is not None

    def test_returns_402_when_zero_credits(self, user_without_credits):
        result = check_user_has_credits(user_without_credits)
        assert result.status_code == status.HTTP_402_PAYMENT_REQUIRED

    def test_returns_402_when_negative_credits(self, user):
        # spent > monthly_max → credit_count is negative
        user.profile.monthly_max_credit_count = 0
        user.profile.spent_credit_count = 3
        user.profile.save()
        result = check_user_has_credits(user)
        assert result.status_code == status.HTTP_402_PAYMENT_REQUIRED

    def test_returns_none_when_exactly_one_credit(self, user):
        user.profile.monthly_max_credit_count = 1
        user.profile.spent_credit_count = 0
        user.profile.save()
        assert check_user_has_credits(user) is None

    def test_error_message(self, user_without_credits):
        result = check_user_has_credits(user_without_credits)
        assert result.data["message"] == "Insufficient credits."


# ---------------------------------------------------------------------------
# HasUserAPIKey
# ---------------------------------------------------------------------------

class TestHasUserAPIKey:

    def test_model_is_user_api_key(self):
        assert HasUserAPIKey.model is UserAPIKey


# ---------------------------------------------------------------------------
# GuardianObjectPermissions
# ---------------------------------------------------------------------------

class TestGuardianObjectPermissions:

    def _make_request(self, method="GET", is_authenticated=True):
        request = MagicMock()
        request.method = method
        request.user = MagicMock()
        request.user.is_authenticated = is_authenticated
        return request

    def test_has_permission_true_for_authenticated_user(self):
        permission = GuardianObjectPermissions()
        assert permission.has_permission(self._make_request(), None) is True

    def test_has_permission_false_for_anonymous_user(self):
        permission = GuardianObjectPermissions()
        assert permission.has_permission(self._make_request(is_authenticated=False), None) is False

    def test_has_permission_false_when_user_is_none(self):
        permission = GuardianObjectPermissions()
        request = MagicMock()
        request.user = None
        assert permission.has_permission(request, None) is False

    def test_has_object_permission_true_when_perm_held(self):
        permission = GuardianObjectPermissions()
        request = self._make_request(method="GET")
        obj = MagicMock()
        obj.__class__._meta.model_name = "snapshot"
        with patch("core.permissions.get_perms", return_value=["view_snapshot"]):
            assert permission.has_object_permission(request, None, obj) is True

    def test_has_object_permission_false_when_perm_missing(self):
        permission = GuardianObjectPermissions()
        request = self._make_request(method="GET")
        obj = MagicMock()
        obj.__class__._meta.model_name = "snapshot"
        with patch("core.permissions.get_perms", return_value=[]):
            assert permission.has_object_permission(request, None, obj) is False

    def test_has_object_permission_false_for_unknown_method(self):
        permission = GuardianObjectPermissions()
        request = self._make_request(method="CONNECT")
        obj = MagicMock()
        obj.__class__._meta.model_name = "snapshot"
        with patch("core.permissions.get_perms", return_value=["view_snapshot"]):
            assert permission.has_object_permission(request, None, obj) is False

    def test_perms_map_covers_standard_methods(self):
        permission = GuardianObjectPermissions()
        assert set(permission.perms_map.keys()) == {"GET", "HEAD", "OPTIONS", "PUT", "PATCH", "DELETE"}

    @pytest.mark.parametrize("method,expected_perm", [
        ("GET", "view_{model_name}"),
        ("HEAD", "view_{model_name}"),
        ("OPTIONS", "view_{model_name}"),
        ("PUT", "change_{model_name}"),
        ("PATCH", "change_{model_name}"),
        ("DELETE", "delete_{model_name}"),
    ])
    def test_perms_map_values(self, method, expected_perm):
        permission = GuardianObjectPermissions()
        assert permission.perms_map[method] == expected_perm
