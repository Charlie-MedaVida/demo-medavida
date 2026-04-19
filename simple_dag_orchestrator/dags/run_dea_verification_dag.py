from celery import shared_task
from celery.utils.log import get_task_logger

from vida_verified.models import DeaCredential
from simple_dag_orchestrator.services.aws_lambda import (
    invoke_sam_exclusions_search_crawler,
    invoke_sam_exclusions_search_etl,
    invoke_load_dea_verifications,
)

logger = get_task_logger(__name__)


@shared_task
def run_dea_verification(dea_credential_id: str):
    credential = DeaCredential.objects.prefetch_related(
        'primary_providers',
    ).get(pk=dea_credential_id)

    provider = credential.primary_providers.first()

    params = {
        'exclusionName': (
            f'{provider.first_name} {provider.last_name}' if provider else ''
        ),
        'classification': 'Individual',
        's3_bucket': 'vidaverified--raw-document-data',
    }
    logger.info(
        'run_dea_verification: invoking SAM exclusions search crawler. '
        'dea_credential_id=%s',
        dea_credential_id,
    )
    results = invoke_sam_exclusions_search_crawler(params)
    s3_key = results['result']['s3_key']
    logger.info(
        'run_dea_verification: crawler complete. s3_key=%s', s3_key,
    )

    invoke_sam_exclusions_search_etl(
        uuid=str(credential.id),
        source_key=s3_key,
    )
    logger.info(
        'run_dea_verification: ETL complete. dea_credential_id=%s',
        dea_credential_id,
    )

    invoke_load_dea_verifications(uuids=[str(credential.id)])
    logger.info(
        'run_dea_verification: load complete. dea_credential_id=%s',
        dea_credential_id,
    )
