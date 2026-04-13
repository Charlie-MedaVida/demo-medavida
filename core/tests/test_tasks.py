import pytest
from unittest.mock import patch
from django.test import override_settings

from core.tasks import sync_stripe_prices_task, reset_spent_credit_count_task


# The function is imported lazily inside the task body, so we mock it at its
# definition site so the patch is active when the task resolves the name.
SYNC_PATCH = "core.business_logic.stripe.sync_stripe_prices"


class TestSyncStripePricesTask:
    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def test_task_is_registered_with_correct_name(self):
        assert sync_stripe_prices_task.name == "sync_stripe_prices_task"

    def test_task_has_delay_method(self):
        assert callable(sync_stripe_prices_task.delay)

    def test_task_has_apply_async_method(self):
        assert callable(sync_stripe_prices_task.apply_async)

    # ------------------------------------------------------------------
    # Logic — call the task function directly (no broker required)
    # ------------------------------------------------------------------

    def test_calls_sync_stripe_prices(self):
        with patch(SYNC_PATCH) as mock_sync:
            sync_stripe_prices_task()
        mock_sync.assert_called_once()

    def test_calls_sync_stripe_prices_with_no_arguments(self):
        with patch(SYNC_PATCH) as mock_sync:
            sync_stripe_prices_task()
        mock_sync.assert_called_once_with()

    # ------------------------------------------------------------------
    # Execution via .apply() — runs the task in-process synchronously
    # ------------------------------------------------------------------

    def test_apply_returns_successful_result(self):
        with patch(SYNC_PATCH):
            result = sync_stripe_prices_task.apply()
        assert result.successful()

    def test_apply_result_value_is_none(self):
        with patch(SYNC_PATCH):
            result = sync_stripe_prices_task.apply()
        assert result.get() is None

    def test_apply_calls_sync_stripe_prices(self):
        with patch(SYNC_PATCH) as mock_sync:
            sync_stripe_prices_task.apply()
        mock_sync.assert_called_once()

    # ------------------------------------------------------------------
    # Eager execution via .delay() — CELERY_TASK_ALWAYS_EAGER=True
    # makes .delay() run the task synchronously in the current process.
    # ------------------------------------------------------------------

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_delay_executes_task_synchronously_in_eager_mode(self):
        with patch(SYNC_PATCH) as mock_sync:
            sync_stripe_prices_task.delay()
        mock_sync.assert_called_once()

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_delay_returns_eager_result_in_eager_mode(self):
        with patch(SYNC_PATCH):
            result = sync_stripe_prices_task.delay()
        assert result.successful()


# ===========================================================================
# reset_spent_credit_count_task
# ===========================================================================

class TestResetSpentCreditCountTask:
    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def test_task_is_registered_with_correct_name(self):
        assert reset_spent_credit_count_task.name == "reset_spent_credit_count_task"

    def test_task_has_delay_method(self):
        assert callable(reset_spent_credit_count_task.delay)

    def test_task_has_apply_async_method(self):
        assert callable(reset_spent_credit_count_task.apply_async)

    # ------------------------------------------------------------------
    # Logic — DB-backed (the task issues a bulk UPDATE, no external deps)
    # ------------------------------------------------------------------

    @pytest.mark.django_db
    def test_resets_spent_credit_count_to_zero(self, user):
        user.profile.spent_credit_count = 5
        user.profile.save()

        reset_spent_credit_count_task()

        user.profile.refresh_from_db()
        assert user.profile.spent_credit_count == 0

    @pytest.mark.django_db
    def test_resets_all_profiles(self, stripe_mock):
        from django.contrib.auth.models import User
        from core.models import Profile

        user_a = User.objects.create_user("reset_a", "a@example.com", "pass")
        user_b = User.objects.create_user("reset_b", "b@example.com", "pass")
        user_a.profile.spent_credit_count = 3
        user_a.profile.save()
        user_b.profile.spent_credit_count = 7
        user_b.profile.save()

        reset_spent_credit_count_task()

        assert Profile.objects.get(user=user_a).spent_credit_count == 0
        assert Profile.objects.get(user=user_b).spent_credit_count == 0

    @pytest.mark.django_db
    def test_does_not_affect_monthly_max_credit_count(self, user):
        user.profile.monthly_max_credit_count = 20
        user.profile.spent_credit_count = 10
        user.profile.save()

        reset_spent_credit_count_task()

        user.profile.refresh_from_db()
        assert user.profile.monthly_max_credit_count == 20

    @pytest.mark.django_db
    def test_credit_count_equals_monthly_max_after_reset(self, user):
        user.profile.monthly_max_credit_count = 15
        user.profile.spent_credit_count = 8
        user.profile.save()

        reset_spent_credit_count_task()

        user.profile.refresh_from_db()
        assert user.profile.credit_count == 15

    # ------------------------------------------------------------------
    # Execution via .apply()
    # ------------------------------------------------------------------

    @pytest.mark.django_db
    def test_apply_returns_successful_result(self, user):
        result = reset_spent_credit_count_task.apply()
        assert result.successful()

    @pytest.mark.django_db
    def test_apply_result_value_is_none(self, user):
        result = reset_spent_credit_count_task.apply()
        assert result.get() is None

    # ------------------------------------------------------------------
    # Eager execution via .delay()
    # ------------------------------------------------------------------

    @pytest.mark.django_db
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_delay_resets_credits_in_eager_mode(self, user):
        user.profile.spent_credit_count = 9
        user.profile.save()

        reset_spent_credit_count_task.delay()

        user.profile.refresh_from_db()
        assert user.profile.spent_credit_count == 0