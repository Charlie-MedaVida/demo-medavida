from django.db import models


class StripePrice(models.Model):
    lookup_key = models.CharField(max_length=255, unique=True)
    json_content = models.TextField(blank=True, null=True,)
