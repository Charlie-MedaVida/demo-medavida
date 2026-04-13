from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import UserAPIKey, Profile


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        api_key, key = UserAPIKey.objects.create_key(
            user=instance,
            name=instance.username
        )
        # This is so dumb...
        api_key.key = key
        api_key.save()

        Profile.objects.create(user=instance)

        import stripe
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        customer = stripe.Customer.create(
            name=instance.username,
            email="jennyrosen@example.com",
        )