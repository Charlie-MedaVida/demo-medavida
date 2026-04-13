from django.db import models
from django.conf import settings  # Recommended way to refer to the user model
from rest_framework_api_key.models import AbstractAPIKey


class UserAPIKey(AbstractAPIKey):

    key = models.CharField(blank=True, null=True, max_length=300)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    def __str__(self):
        return f'UserAPIKey of {self.user.username}'
