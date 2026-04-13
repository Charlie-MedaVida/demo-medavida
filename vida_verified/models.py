from django.db import models
from django.conf import settings


class ReportRequest(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETE = 'COMPLETE', 'Complete'
        FAILED = 'FAILED', 'Failed'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='report_requests',
    )
    status = models.CharField(
        max_length=24,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ReportRequest {self.pk} ({self.status}) — {self.user}'


class Report(models.Model):

    request = models.OneToOneField(
        ReportRequest,
        on_delete=models.CASCADE,
        related_name='report',
    )
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report for ReportRequest {self.request_id}'
