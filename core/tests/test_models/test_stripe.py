import pytest
from django.db import IntegrityError
from core.models import StripePrice


@pytest.mark.django_db
class TestStripePriceModel:

    def test_create_with_lookup_key(self):
        price = StripePrice.objects.create(lookup_key="plan_basic_monthly")
        assert price.pk is not None

    def test_lookup_key_is_persisted(self):
        StripePrice.objects.create(lookup_key="plan_pro_monthly")
        price = StripePrice.objects.get(lookup_key="plan_pro_monthly")
        assert price.lookup_key == "plan_pro_monthly"

    def test_lookup_key_is_unique(self):
        StripePrice.objects.create(lookup_key="plan_unique")
        with pytest.raises(IntegrityError):
            StripePrice.objects.create(lookup_key="plan_unique")

    def test_multiple_prices_with_different_keys(self):
        StripePrice.objects.create(lookup_key="plan_a")
        StripePrice.objects.create(lookup_key="plan_b")
        assert StripePrice.objects.count() == 2
