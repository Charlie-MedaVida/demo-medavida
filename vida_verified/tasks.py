from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def refresh_verification_views():
    from vida_verified.models import DeaVerificationView, NpiVerificationView # noqa
    from practices.models import ProviderVerificationView, PracticeVerificationView # noqa

    NpiVerificationView.refresh()
    logger.info('refresh_verification_views: NpiVerificationView refreshed')

    DeaVerificationView.refresh()
    logger.info('refresh_verification_views: DeaVerificationView refreshed')

    ProviderVerificationView.refresh()
    logger.info(
        'refresh_verification_views: ProviderVerificationView refreshed'
    )

    PracticeVerificationView.refresh()
    logger.info(
        'refresh_verification_views: PracticeVerificationView refreshed'
    )
