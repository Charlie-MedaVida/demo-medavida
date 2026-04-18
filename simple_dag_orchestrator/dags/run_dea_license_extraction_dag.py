from celery import shared_task

from practices.models import DeaCredential
from simple_dag_orchestrator.services.aws_lambda import (
    invoke_dea_license_extraction,
)


@shared_task
def run_dea_license_extraction(dea_certificate_id: str):
    dea_credential = DeaCredential.objects.get(pk=dea_certificate_id)
    invoke_dea_license_extraction(
        uuid=str(dea_credential.id),
        source_key=dea_credential.file.name,
    )
