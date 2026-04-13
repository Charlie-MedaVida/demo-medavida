import json
import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


CREATE_CHECKOUT_URL = reverse("checkout:CreateCheckoutView")
SESSION_STATUS_URL = reverse("checkout:CheckoutStatusRetrieveApiView")
WEBHOOK_URL = reverse("checkout:CheckoutWebhookApiView")


@pytest.fixture
def client():
    return APIClient()


def _mock_stripe_price(price_id="price_test123"):
    mock_price = MagicMock()
    mock_price.id = price_id
    mock_prices = MagicMock()
    mock_prices.data = [mock_price]
    return mock_prices


def _mock_stripe_session(session_id="cs_test123", url="https://checkout.stripe.com/session"):
    mock_session = MagicMock()
    mock_session.id = session_id
    mock_session.url = url
    return mock_session


@pytest.mark.django_db
class TestCreateCheckoutView:
    def test_success_returns_200(self, client, user):
        client.force_authenticate(user=user)
        with patch("stripe.Price.list", return_value=_mock_stripe_price()), \
             patch("stripe.checkout.Session.create", return_value=_mock_stripe_session()):
            response = client.post(
                CREATE_CHECKOUT_URL, {"lookup_key": "basic_plan"}, format="json"
            )
        assert response.status_code == status.HTTP_200_OK

    def test_returns_session_id(self, client, user):
        client.force_authenticate(user=user)
        with patch("stripe.Price.list", return_value=_mock_stripe_price()), \
             patch("stripe.checkout.Session.create", return_value=_mock_stripe_session(session_id="cs_abc")):
            response = client.post(
                CREATE_CHECKOUT_URL, {"lookup_key": "basic_plan"}, format="json"
            )
        assert response.data["sessionId"] == "cs_abc"

    def test_returns_checkout_url(self, client, user):
        client.force_authenticate(user=user)
        checkout_url = "https://checkout.stripe.com/pay/cs_abc"
        with patch("stripe.Price.list", return_value=_mock_stripe_price()), \
             patch("stripe.checkout.Session.create", return_value=_mock_stripe_session(url=checkout_url)):
            response = client.post(
                CREATE_CHECKOUT_URL, {"lookup_key": "basic_plan"}, format="json"
            )
        assert response.data["url"] == checkout_url

    def test_stripe_price_list_called_with_lookup_key(self, client, user):
        client.force_authenticate(user=user)
        with patch("stripe.Price.list", return_value=_mock_stripe_price()) as mock_price_list, \
             patch("stripe.checkout.Session.create", return_value=_mock_stripe_session()):
            client.post(CREATE_CHECKOUT_URL, {"lookup_key": "premium_plan"}, format="json")
        mock_price_list.assert_called_once_with(
            lookup_keys=["premium_plan"],
            expand=["data.product"],
        )

    def test_stripe_session_create_includes_user_id_in_metadata(self, client, user):
        client.force_authenticate(user=user)
        with patch("stripe.Price.list", return_value=_mock_stripe_price()), \
             patch("stripe.checkout.Session.create", return_value=_mock_stripe_session()) as mock_session_create:
            client.post(CREATE_CHECKOUT_URL, {"lookup_key": "basic_plan"}, format="json")
        call_kwargs = mock_session_create.call_args[1]
        assert call_kwargs["metadata"]["internal_user_id"] == user.id

    def test_stripe_error_returns_400(self, client, user):
        client.force_authenticate(user=user)
        with patch("stripe.Price.list", side_effect=Exception("Stripe error")):
            response = client.post(
                CREATE_CHECKOUT_URL, {"lookup_key": "basic_plan"}, format="json"
            )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCheckoutStatusRetrieveView:
    def test_returns_session_status(self, client, user):
        client.force_authenticate(user=user)
        mock_session = MagicMock()
        mock_session.status = "complete"
        mock_session.customer_details.email = "customer@example.com"
        with patch("stripe.checkout.Session.retrieve", return_value=mock_session):
            response = client.get(SESSION_STATUS_URL, {"session_id": "cs_test123"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "complete"

    def test_returns_customer_email(self, client, user):
        client.force_authenticate(user=user)
        mock_session = MagicMock()
        mock_session.status = "complete"
        mock_session.customer_details.email = "customer@example.com"
        with patch("stripe.checkout.Session.retrieve", return_value=mock_session):
            response = client.get(SESSION_STATUS_URL, {"session_id": "cs_test123"})
        assert response.data["customer_email"] == "customer@example.com"

    def test_stripe_session_retrieve_called_with_session_id(self, client, user):
        client.force_authenticate(user=user)
        mock_session = MagicMock()
        mock_session.status = "complete"
        mock_session.customer_details.email = "customer@example.com"
        with patch("stripe.checkout.Session.retrieve", return_value=mock_session) as mock_retrieve:
            client.get(SESSION_STATUS_URL, {"session_id": "cs_test123"})
        mock_retrieve.assert_called_once_with("cs_test123")


@pytest.mark.django_db
class TestCheckoutWebhookView:
    """
    Tests for the webhook endpoint (AllowAny — no authentication required).
    STRIPE_ENDPOINT_SECRET defaults to None in test settings, so signature
    verification is skipped and only stripe.Event.construct_from is exercised.
    """

    def _make_event_payload(self, event_type, user_id=1, count=10):
        return json.dumps({
            "type": event_type,
            "data": {
                "object": {
                    "metadata": {
                        "internal_user_id": str(user_id),
                        "count": str(count),
                    }
                }
            },
        })

    def _mock_stripe_event(self, event_type, user_id=1, count=10):
        mock_event = MagicMock()
        mock_event.type = event_type
        mock_event.data.object.metadata = {
            "internal_user_id": str(user_id),
            "count": str(count),
        }
        return mock_event

    def test_checkout_completed_returns_200(self, client, user):
        payload = self._make_event_payload("checkout.session.completed", user_id=user.id)
        mock_event = self._mock_stripe_event("checkout.session.completed", user_id=user.id)
        with patch("stripe.Event.construct_from", return_value=mock_event), \
             patch("core.views.checkout.add_tokens"):
            response = client.post(
                WEBHOOK_URL,
                data=payload,
                content_type="application/json",
            )
        assert response.status_code == status.HTTP_200_OK

    def test_checkout_completed_returns_success_true(self, client, user):
        payload = self._make_event_payload("checkout.session.completed", user_id=user.id)
        mock_event = self._mock_stripe_event("checkout.session.completed", user_id=user.id)
        with patch("stripe.Event.construct_from", return_value=mock_event), \
             patch("core.views.checkout.add_tokens"):
            response = client.post(
                WEBHOOK_URL,
                data=payload,
                content_type="application/json",
            )
        assert response.data["success"] is True

    def test_checkout_completed_calls_add_tokens(self, client, user):
        payload = self._make_event_payload("checkout.session.completed", user_id=user.id, count=5)
        mock_event = self._mock_stripe_event("checkout.session.completed", user_id=user.id, count=5)
        with patch("stripe.Event.construct_from", return_value=mock_event), \
             patch("core.views.checkout.add_tokens") as mock_add_tokens:
            client.post(WEBHOOK_URL, data=payload, content_type="application/json")
        mock_add_tokens.assert_called_once_with(str(user.id), credit_count=str(5))

    def test_async_payment_succeeded_calls_add_tokens(self, client, user):
        payload = self._make_event_payload(
            "checkout.session.async_payment_succeeded", user_id=user.id, count=3
        )
        mock_event = self._mock_stripe_event(
            "checkout.session.async_payment_succeeded", user_id=user.id, count=3
        )
        with patch("stripe.Event.construct_from", return_value=mock_event), \
             patch("core.views.checkout.add_tokens") as mock_add_tokens:
            client.post(WEBHOOK_URL, data=payload, content_type="application/json")
        mock_add_tokens.assert_called_once()

    def test_unhandled_event_type_returns_200(self, client):
        payload = json.dumps({"type": "payment_intent.created", "data": {"object": {}}})
        mock_event = MagicMock()
        mock_event.type = "payment_intent.created"
        with patch("stripe.Event.construct_from", return_value=mock_event):
            response = client.post(
                WEBHOOK_URL, data=payload, content_type="application/json"
            )
        assert response.status_code == status.HTTP_200_OK

    def test_invalid_json_payload_returns_400(self, client):
        with patch("stripe.Event.construct_from", side_effect=ValueError("Invalid JSON")):
            response = client.post(
                WEBHOOK_URL, data="not-valid-json", content_type="application/json"
            )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_no_authentication_required(self, client, stripe_mock):
        """Webhook endpoint is AllowAny — unauthenticated requests are accepted."""
        payload = json.dumps({"type": "some.event", "data": {"object": {}}})
        mock_event = MagicMock()
        mock_event.type = "some.event"
        with patch("stripe.Event.construct_from", return_value=mock_event):
            response = client.post(
                WEBHOOK_URL, data=payload, content_type="application/json"
            )
        # Should not return 401 or 403
        assert response.status_code not in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]
