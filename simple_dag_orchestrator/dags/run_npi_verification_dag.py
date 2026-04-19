from celery import shared_task
from celery.utils.log import get_task_logger

from vida_verified.models import NpiCredential
from simple_dag_orchestrator.services.aws_lambda import (
    invoke_npi_registry_search_crawler,
    invoke_npi_registry_search_etl,
    invoke_load_npi_verifications,
)

logger = get_task_logger(__name__)


@shared_task
def run_npi_verification(npi_credential_id: str):
    credential = NpiCredential.objects.get(pk=npi_credential_id)

    params = {
        'number': credential.license_number,
        's3_bucket': 'vidaverified--raw-document-data',
    }
    logger.info(
        'run_npi_verification: invoking NPI registry search crawler. '
        'npi_credential_id=%s',
        npi_credential_id,
    )
    results = invoke_npi_registry_search_crawler(params)
    s3_key = results['result']['s3_key']
    logger.info(
        'run_npi_verification: crawler complete. s3_key=%s', s3_key,
    )

    invoke_npi_registry_search_etl(
        uuid=str(credential.id),
        source_key=s3_key,
    )
    logger.info(
        'run_npi_verification: ETL complete. npi_credential_id=%s',
        npi_credential_id,
    )

    invoke_load_npi_verifications(uuids=[str(credential.id)])
    logger.info(
        'run_npi_verification: load complete. npi_credential_id=%s',
        npi_credential_id,
    )
