from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    spent_credit_count = models.IntegerField(default=0)
    monthly_max_credit_count = models.IntegerField(default=0)

    def __str__(self):
        return f'Profile of {self.user.username}'

    @property
    def credit_count(self):
        return self.monthly_max_credit_count - self.spent_credit_count
