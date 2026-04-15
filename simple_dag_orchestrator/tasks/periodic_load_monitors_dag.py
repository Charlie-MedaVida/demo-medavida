from celery import shared_task

from simple_dag_orchestrator.services.aws_lambda import invoke_load_monitor_results


@shared_task(name="load_monitors_dag")
def load_monitors_dag():
    invoke_load_monitor_results()
