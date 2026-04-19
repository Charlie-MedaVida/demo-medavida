from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def run_periodic_npi_verification():
    from vida_verified.models import NpiCredential
    from simple_dag_orchestrator.dags import run_npi_verification

    credential_ids = NpiCredential.objects.values_list('id', flat=True)
    count = 0
    for credential_id in credential_ids:
        run_npi_verification.delay(str(credential_id))
        count += 1

    logger.info(
        'run_periodic_npi_verification: queued %d NPI verification tasks',
        count,
    )
