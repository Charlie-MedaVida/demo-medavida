from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ReportRequest
from .tasks import async_run_report


@receiver(post_save, sender=ReportRequest)
def on_report_request_saved(sender, instance, created, **kwargs):
    if created:
        async_run_report.delay(instance.pk)
