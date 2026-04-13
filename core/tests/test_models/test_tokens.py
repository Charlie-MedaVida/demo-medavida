import pytest
from core.models.tokens import TokenEventLog


class TestTokenEventLogTypeChoices:

    def test_add_choice_value(self):
        assert TokenEventLog.TypeChoices.ADD == "ADD"

    def test_subtract_choice_value(self):
        assert TokenEventLog.TypeChoices.SUBTRACT == "SUBTRACT"

    def test_exactly_two_choices(self):
        assert len(TokenEventLog.TypeChoices.choices) == 2


@pytest.mark.django_db
class TestTokenEventLogModel:

    def test_create_with_required_fields(self, user):
        log = TokenEventLog.objects.create(user=user)
        assert log.pk is not None

    def test_default_event_type_is_subtract(self, user):
        log = TokenEventLog.objects.create(user=user)
        assert log.event_type == TokenEventLog.TypeChoices.SUBTRACT

    def test_default_credit_count_is_one(self, user):
        log = TokenEventLog.objects.create(user=user)
        assert log.credit_count == 1

    def test_created_at_is_set_automatically(self, user):
        log = TokenEventLog.objects.create(user=user)
        assert log.created_at is not None

    def test_summary_defaults_to_null(self, user):
        log = TokenEventLog.objects.create(user=user)
        assert log.summary is None

    def test_details_defaults_to_null(self, user):
        log = TokenEventLog.objects.create(user=user)
        assert log.details is None

    def test_create_add_event_type(self, user):
        log = TokenEventLog.objects.create(
            user=user,
            event_type=TokenEventLog.TypeChoices.ADD,
            credit_count=5,
        )
        assert log.event_type == "ADD"
        assert log.credit_count == 5

    def test_summary_and_details_are_persisted(self, user):
        log = TokenEventLog.objects.create(
            user=user,
            summary="snapshot taken",
            details="tweet_id=abc123",
        )
        log.refresh_from_db()
        assert log.summary == "snapshot taken"
        assert log.details == "tweet_id=abc123"

    def test_user_foreign_key(self, user):
        log = TokenEventLog.objects.create(user=user)
        assert log.user == user

    def test_logs_accessible_via_user_related_name(self, user):
        TokenEventLog.objects.create(user=user)
        assert user.event_logs.count() == 1

    def test_user_can_have_multiple_logs(self, user):
        TokenEventLog.objects.create(user=user, event_type=TokenEventLog.TypeChoices.ADD)
        TokenEventLog.objects.create(user=user, event_type=TokenEventLog.TypeChoices.SUBTRACT)
        assert TokenEventLog.objects.filter(user=user).count() == 2

    def test_logs_deleted_when_user_deleted(self, user):
        TokenEventLog.objects.create(user=user)
        user_id = user.id
        user.delete()
        assert not TokenEventLog.objects.filter(user_id=user_id).exists()
