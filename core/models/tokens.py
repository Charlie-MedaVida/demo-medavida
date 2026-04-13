from django.db import models
from django.conf import settings


class TokenEventLog(models.Model):

    class TypeChoices(models.TextChoices):
        ADD = "ADD", "ADD"
        SUBTRACT = "SUBTRACT", "SUBTRACT"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_logs'
    )
    event_type = models.CharField(
        max_length=24,
        choices=TypeChoices.choices,
        default=TypeChoices.SUBTRACT,
    )
    credit_count = models.IntegerField(default=1)
    summary = models.CharField(blank=True, null=True, max_length=300)
    details = models.TextField(blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
