import stripe
from django.conf import settings
from ..models import StripePrice


def sync_stripe_prices():
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    vendor_id = settings.STRIPE_VENDOR_ID
    query = f"active:'true' AND metadata['vendor_id']:'{vendor_id}'"
    data = stripe.Price.search(query=query)
    prices = data['data']
    for price in prices:
        StripePrice.objects.update_or_create(
            lookup_key=price.lookup_key,
            defaults={"json_content": price},
        )