import json
import logging
from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime, timezone


logging.basicConfig(level=logging.INFO)


celery_logger = get_task_logger(__name__)
logger = logging.getLogger(__name__)


@shared_task(name="sync_stripe_prices_task")
def sync_stripe_prices_task():
    print("sync_stripe_prices")
    from core.business_logic.stripe import sync_stripe_prices
    sync_stripe_prices()


@shared_task(name="reset_spent_credit_count_task")
def reset_spent_credit_count_task():
    from core.models import Profile
    Profile.objects.all().update(spent_credit_count=0)
