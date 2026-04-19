import uuid

from django.db import models


class Credential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_number = models.CharField(max_length=100, blank=True, default='')
    last_checked_at = models.DateTimeField(null=True, blank=True)
    enumeration_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='credentials/', null=True, blank=True)

    class Meta:
        abstract = True


class NpiCredential(Credential):
    def __str__(self):
        return f'NPI {self.license_number}'


class DeaCredential(Credential):
    def __str__(self):
        return f'DEA {self.license_number}'


