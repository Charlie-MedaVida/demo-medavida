from django.db import models
from django.conf import settings


class BaseCredentialStatus(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETE = 'COMPLETE', 'Complete'
        FAILED = 'FAILED', 'Failed'

    report = models.ForeignKey(
        'Report',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=24,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    json_content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NpiCredentialStatus(BaseCredentialStatus):
    npi_number = models.CharField(max_length=10, blank=True, default='')


class DcdCredentialStatus(BaseCredentialStatus):
    dea_number = models.CharField(max_length=9, blank=True, default='')


class ReportRequest(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETE = 'COMPLETE', 'Complete'
        FAILED = 'FAILED', 'Failed'

    class IdTypeChoices(models.TextChoices):
        SSN = 'SSN', 'SSN'
        EIN = 'EIN', 'EIN'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='report_requests',
    )
    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    postal_code = models.CharField(max_length=20, blank=True, default='')
    ssn = models.CharField(max_length=11, blank=True, default='')
    ein = models.CharField(max_length=10, blank=True, default='')
    id_type = models.CharField(
        max_length=3,
        choices=IdTypeChoices.choices,
        blank=True,
        default='',
    )
    status = models.CharField(
        max_length=24,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):

    request = models.OneToOneField(
        ReportRequest,
        on_delete=models.CASCADE,
        related_name='report',
    )
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
