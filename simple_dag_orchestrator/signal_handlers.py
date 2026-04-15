from django.db.models.signals import post_save
from django.dispatch import receiver

from vida_verified.models import ReportRequest
from simple_dag_orchestrator.dags.run_reports_dag import run_reports_dag


@receiver(post_save, sender=ReportRequest)
def on_report_request_saved(sender, instance, created, **kwargs):
    if created:
        run_reports_dag.delay(instance.pk)