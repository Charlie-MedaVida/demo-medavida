from celery import shared_task
from celery.utils.log import get_task_logger

from practices.business_logic import nppes_search
from practices.models import Provider
from simple_dag_orchestrator.services.aws_lambda import invoke_crawler

logger = get_task_logger(__name__)


@shared_task
def verify_provider(provider_id: str):
    provider = Provider.objects.select_related(
        'npi_credential', 'dea_credential',
    ).get(pk=provider_id)

    # --- NPI verification via NPPES ---
    try:
        npi_number = (
            provider.npi_credential.license_number
            if provider.npi_credential else None
        )
        if npi_number:
            nppes_search({'number': npi_number})
            logger.info(
                'verify_provider: NPI search complete. provider_id=%s '
                'npi_number=%s',
                provider_id, npi_number,
            )
        provider.npi_verification_status = (
            Provider.VerificationStatus.VERIFIED
        )
    except Exception:
        logger.exception(
            'verify_provider: NPI verification failed. provider_id=%s',
            provider_id,
        )
        provider.npi_verification_status = Provider.VerificationStatus.FAILED

    # --- DEA verification via medavida-crawler ---
    try:
        dea = provider.dea_credential
        if dea:
            expiration_year = (
                dea.expiration_date.year if dea.expiration_date else None
            )
            expiration_month = (
                dea.expiration_date.month if dea.expiration_date else None
            )
            invoke_crawler(
                platform='dea',
                bot='dea_credentials_form',
                dea_number=dea.license_number,
                last_name=provider.last_name,
                ssn=provider.ssn,
                zip_code=provider.zip_code,
                expiration_year=expiration_year,
                expiration_month=expiration_month,
            )
            logger.info(
                'verify_provider: DEA crawler complete. provider_id=%s '
                'dea_number=%s',
                provider_id, dea.license_number,
            )
        provider.dea_verification_status = (
            Provider.VerificationStatus.VERIFIED
        )
    except Exception:
        logger.exception(
            'verify_provider: DEA verification failed. provider_id=%s',
            provider_id,
        )
        provider.dea_verification_status = Provider.VerificationStatus.FAILED

    provider.save()
