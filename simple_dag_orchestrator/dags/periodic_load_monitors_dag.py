from celery import shared_task

from simple_dag_orchestrator.services.aws_lambda import invoke_load_credential_monitors


@shared_task
def load_monitors_dag():
    invoke_load_credential_monitors()
