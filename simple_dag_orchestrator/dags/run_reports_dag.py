from celery import shared_task
from celery.utils.log import get_task_logger

from vida_verified.models import ReportRequest
from simple_dag_orchestrator.services.aws_lambda import (
    invoke_npi_registry_search_crawler,
    invoke_npi_registry_search_etl,
    invoke_sam_exclusions_search_crawler,
    invoke_sam_exclusions_search_etl,
    invoke_load_report_results,
)

logger = get_task_logger(__name__)


@shared_task
def run_reports_dag(report_request_id: int):
    logger.info('run_reports_dag started. report_request_id=%s', report_request_id)

    report_requests = ReportRequest.objects.filter(
        id=report_request_id,
        status=ReportRequest.StatusChoices.PENDING,
    )
    report_requests.update(status=ReportRequest.StatusChoices.RUNNING)
    logger.info('ReportRequest %s status updated to RUNNING', report_request_id)

    # NPI Registrations
    params = [
        {
            'first_name': r.first_name,
            'last_name': r.last_name,
            'city': r.city,
            'state': r.state,
            'postal_code': r.postal_code,
            's3_bucket': 'vidaverified--raw-document-data',
        }
        for r in report_requests
    ]
    logger.info('Invoking NPI registry search crawler. record_count=%s', len(params))
    results = invoke_npi_registry_search_crawler(params)
    s3_key = results['result']['s3_key']
    logger.info('NPI registry search crawler complete. s3_key=%s', s3_key)

    invoke_npi_registry_search_etl(source_key=s3_key)
    logger.info('NPI registry search ETL complete.')

    # SAM Registrations
    sam_params = [
        {
            'exclusionName': f'{r.first_name} {r.last_name}',
            'classification': 'Individual',
            's3_bucket': 'vidaverified--raw-document-data',
        }
        for r in report_requests
    ]
    logger.info('Invoking SAM exclusions search crawler. record_count=%s', len(sam_params))
    results = invoke_sam_exclusions_search_crawler(sam_params)
    s3_key = results['result']['s3_key']
    logger.info('SAM exclusions search crawler complete. s3_key=%s', s3_key)

    invoke_sam_exclusions_search_etl(source_key=s3_key)
    logger.info('SAM exclusions search ETL complete.')

    # Call the Load Function to Close the Loop
    report_request = report_requests.first()
    logger.info('Invoking load_report_results. uuid=%s', report_request.uuid)
    invoke_load_report_results(uuids=[str(report_request.uuid)])
    logger.info('run_reports_dag complete. report_request_id=%s', report_request_id)
