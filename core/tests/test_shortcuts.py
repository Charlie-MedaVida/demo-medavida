import pytest
from unittest.mock import patch

from core.models.tokens import TokenEventLog
from core.shortcuts import add_tokens, subtract_token


# ---------------------------------------------------------------------------
# add_tokens
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestAddTokens:

    def test_increments_credit_count(self, user):
        with patch("core.shortcuts.assign_perm"):
            add_tokens(user, credit_count=5)
        user.profile.refresh_from_db()
        assert user.profile.credit_count == 5

    def test_creates_event_log_entry(self, user):
        with patch("core.shortcuts.assign_perm"):
            add_tokens(user, credit_count=3)
        assert TokenEventLog.objects.filter(user=user).count() == 1

    def test_event_log_has_add_type(self, user):
        with patch("core.shortcuts.assign_perm"):
            add_tokens(user, credit_count=2)
        log = TokenEventLog.objects.get(user=user)
        assert log.event_type == TokenEventLog.TypeChoices.ADD

    def test_event_log_credit_count_matches(self, user):
        with patch("core.shortcuts.assign_perm"):
            add_tokens(user, credit_count=7)
        log = TokenEventLog.objects.get(user=user)
        assert log.credit_count == 7

    def test_accumulates_across_multiple_calls(self, user):
        with patch("core.shortcuts.assign_perm"):
            add_tokens(user, credit_count=3)
            add_tokens(user, credit_count=4)
        user.profile.refresh_from_db()
        assert user.profile.credit_count == 7

    def test_default_credit_count_is_one(self, user):
        with patch("core.shortcuts.assign_perm"):
            add_tokens(user)
        user.profile.refresh_from_db()
        assert user.profile.credit_count == 1


# ---------------------------------------------------------------------------
# subtract_token
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestSubtractToken:

    def test_decrements_credit_count_by_one(self, user_with_credits):
        initial = user_with_credits.profile.credit_count
        with patch("core.shortcuts.assign_perm"):
            subtract_token(user_with_credits, summary="test", description="desc")
        user_with_credits.profile.refresh_from_db()
        assert user_with_credits.profile.credit_count == initial - 1

    def test_creates_event_log_entry(self, user_with_credits):
        with patch("core.shortcuts.assign_perm"):
            subtract_token(user_with_credits, summary="snap", description="took a snapshot")
        assert TokenEventLog.objects.filter(user=user_with_credits).count() == 1

    def test_event_log_has_subtract_type(self, user_with_credits):
        with patch("core.shortcuts.assign_perm"):
            subtract_token(user_with_credits, summary="snap", description="details")
        log = TokenEventLog.objects.get(user=user_with_credits)
        assert log.event_type == TokenEventLog.TypeChoices.SUBTRACT

    def test_event_log_stores_summary(self, user_with_credits):
        with patch("core.shortcuts.assign_perm"):
            subtract_token(user_with_credits, summary="snapshot taken", description="details")
        log = TokenEventLog.objects.get(user=user_with_credits)
        assert log.summary == "snapshot taken"

    def test_event_log_stores_description(self, user_with_credits):
        with patch("core.shortcuts.assign_perm"):
            subtract_token(user_with_credits, summary="summary", description="detailed info")
        log = TokenEventLog.objects.get(user=user_with_credits)
        assert log.details == "detailed info"
