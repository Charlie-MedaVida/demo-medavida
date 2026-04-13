import io
import os
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError


User = get_user_model()

ADMIN_ENV = {
    "DJANGO_SUPERUSER_USERNAME": "testadmin",
    "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
    "DJANGO_SUPERUSER_PASSWORD": "adminpass123",
}


def _call_command(stdout=None):
    out = stdout or io.StringIO()
    with patch.dict(os.environ, ADMIN_ENV), \
         patch("stripe.Customer.create", return_value=MagicMock(id="cus_test")):
        call_command("create_admin_user", stdout=out)
    return out


@pytest.mark.django_db
class TestCreateAdminUserCommand:
    def test_creates_superuser(self):
        _call_command()
        assert User.objects.filter(username="testadmin", is_superuser=True).exists()

    def test_creates_superuser_with_correct_email(self):
        _call_command()
        user = User.objects.get(username="testadmin")
        assert user.email == "admin@example.com"

    def test_outputs_creating_message(self):
        out = io.StringIO()
        _call_command(stdout=out)
        assert "Creating Admin User" in out.getvalue()

    def test_outputs_created_message(self):
        out = io.StringIO()
        _call_command(stdout=out)
        assert "Admin User Created" in out.getvalue()

    def test_skips_creation_when_admin_already_exists(self):
        _call_command()  # first call creates admin
        _call_command()  # second call should skip
        assert User.objects.filter(username="testadmin").count() == 1

    def test_outputs_exists_message_when_skipping(self):
        _call_command()  # create admin
        out = io.StringIO()
        _call_command(stdout=out)  # run again
        assert "Admin User exists" in out.getvalue()

    def test_outputs_skipping_message_when_already_exists(self):
        _call_command()  # create admin
        out = io.StringIO()
        _call_command(stdout=out)  # run again
        assert "Skipping" in out.getvalue()

    def test_raises_command_error_on_exception(self):
        with patch.dict(os.environ, ADMIN_ENV), \
             patch("stripe.Customer.create", return_value=MagicMock(id="cus_test")), \
             patch(
                 "core.management.commands.create_admin_user.get_user_model"
             ) as mock_get_user_model:
            mock_model = MagicMock()
            mock_model.objects.filter.return_value.exists.side_effect = Exception("DB error")
            mock_get_user_model.return_value = mock_model
            with pytest.raises(CommandError):
                call_command("create_admin_user")
