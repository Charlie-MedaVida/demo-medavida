from ..models import Profile, StripePrice


def set_subscription(user_id, lookup_key):
    profile = Profile.objects.get(user__id=user_id)
    subscription = StripePrice.objects.get(lookup_key=lookup_key)

    if subscription.lookup_key == 'twitter_pictures_gold':
        profile.monthly_max_credit_count = 1000
    elif subscription.lookup_key == 'twitter_pictures_silver':
        profile.monthly_max_credit_count = 100
    elif subscription.lookup_key == 'twitter_pictures_basic':
        profile.monthly_max_credit_count = 10
