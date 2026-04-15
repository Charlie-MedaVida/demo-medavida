from celery import shared_task

from vida_verified.models import MonitorResults
from simple_dag_orchestrator.services.aws_lambda import invoke_load_monitor_results


@shared_task(name="load_monitors_dag")
def load_monitors_dag():
    uuids = list(MonitorResults.objects.values_list('uuid', flat=True))
    invoke_load_monitor_results(uuids=[str(u) for u in uuids])
