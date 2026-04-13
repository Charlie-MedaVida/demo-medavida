import pytest
from unittest.mock import patch, MagicMock, call
from django.conf import settings

from core.business_logic.stripe import sync_stripe_prices
from core.models import StripePrice


def _make_mock_price(lookup_key):
    price = MagicMock()
    price.lookup_key = lookup_key
    return price


@pytest.mark.django_db
class TestSyncStripePrices:
    def test_calls_stripe_price_search(self):
        with patch("stripe.Price.search", return_value=[]) as mock_search:
            sync_stripe_prices()
        mock_search.assert_called_once()

    def test_search_query_contains_active_filter(self):
        with patch("stripe.Price.search", return_value=[]) as mock_search:
            sync_stripe_prices()
        query = mock_search.call_args[1]["query"]
        assert "active:'true'" in query

    def test_search_query_contains_vendor_id(self):
        vendor_id = settings.STRIPE_VENDOR_ID
        with patch("stripe.Price.search", return_value=[]) as mock_search:
            sync_stripe_prices()
        query = mock_search.call_args[1]["query"]
        assert str(vendor_id) in query

    def test_single_price_creates_stripe_price_record(self):
        mock_prices = [_make_mock_price("plan_basic")]
        with patch("stripe.Price.search", return_value=mock_prices):
            sync_stripe_prices()
        assert StripePrice.objects.filter(lookup_key="plan_basic").exists()

    def test_multiple_prices_creates_all_records(self):
        mock_prices = [
            _make_mock_price("plan_basic"),
            _make_mock_price("plan_pro"),
            _make_mock_price("plan_enterprise"),
        ]
        with patch("stripe.Price.search", return_value=mock_prices):
            sync_stripe_prices()
        assert StripePrice.objects.filter(lookup_key="plan_basic").exists()
        assert StripePrice.objects.filter(lookup_key="plan_pro").exists()
        assert StripePrice.objects.filter(lookup_key="plan_enterprise").exists()

    def test_multiple_prices_correct_count(self):
        mock_prices = [
            _make_mock_price("plan_basic"),
            _make_mock_price("plan_pro"),
        ]
        with patch("stripe.Price.search", return_value=mock_prices):
            sync_stripe_prices()
        assert StripePrice.objects.count() == 2

    def test_no_prices_returned_creates_no_records(self):
        with patch("stripe.Price.search", return_value=[]):
            sync_stripe_prices()
        assert StripePrice.objects.count() == 0

    def test_existing_price_is_updated_not_duplicated(self):
        StripePrice.objects.create(lookup_key="plan_existing")
        mock_prices = [_make_mock_price("plan_existing")]
        with patch("stripe.Price.search", return_value=mock_prices):
            sync_stripe_prices()
        # update_or_create should not create a duplicate
        assert StripePrice.objects.filter(lookup_key="plan_existing").count() == 1

    def test_sets_stripe_api_key(self):
        import stripe
        with patch("stripe.Price.search", return_value=[]):
            sync_stripe_prices()
        assert stripe.api_key == settings.STRIPE_TEST_SECRET_KEY
