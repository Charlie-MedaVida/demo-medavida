import uuid

from django.db import models
from django_materialized_view.base_model import MaterializedViewModel


class VerificationResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checked_at = models.DateTimeField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    error_content = models.TextField(blank=True, default='')
    json_content = models.TextField(blank=True, default='')

    class Meta:
        abstract = True


class Credential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_number = models.CharField(max_length=100, blank=True, default='')
    last_checked_at = models.DateTimeField(null=True, blank=True)
    enumeration_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='credentials/', null=True, blank=True)

    class Meta:
        abstract = True


class NpiVerificationResult(VerificationResult):
    pass


class DeaVerificationResult(VerificationResult):
    pass


class NpiCredential(Credential):
    def __str__(self):
        return f'NPI {self.license_number}'


class DeaCredential(Credential):
    def __str__(self):
        return f'DEA {self.license_number}'


class DeaVerificationView(MaterializedViewModel):
    create_pkey_index = True

    id = models.UUIDField(primary_key=True, editable=False)
    license_number = models.CharField(max_length=100)
    last_checked_at = models.DateTimeField(null=True)
    enumeration_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    checked_at = models.DateTimeField(null=True)
    verified = models.BooleanField(null=True)
    error_content = models.TextField()
    json_content = models.TextField()

    class Meta:
        managed = False


class NpiVerificationView(MaterializedViewModel):
    create_pkey_index = True

    id = models.UUIDField(primary_key=True, editable=False)
    license_number = models.CharField(max_length=100)
    last_checked_at = models.DateTimeField(null=True)
    enumeration_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    checked_at = models.DateTimeField(null=True)
    verified = models.BooleanField(null=True)
    error_content = models.TextField()
    json_content = models.TextField()

    class Meta:
        managed = False
