from celery import shared_task

from vida_verified.models import ReportRequest
from simple_dag_orchestrator.services.aws_lambda import (
    invoke_npi_registry_search_crawler,
    invoke_npi_registry_search_etl,
    invoke_sam_exclusions_search_crawler,
    invoke_sam_exclusions_search_etl
)


@shared_task
def run_reports_dag(report_request_id: int):
    report_requests = ReportRequest.objects.filter(
        id=report_request_id,
        status=ReportRequest.StatusChoices.PENDING,
    )
    report_requests.update(status=ReportRequest.StatusChoices.RUNNING)

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
    results = invoke_npi_registry_search_crawler(params)
    s3_key = results['result']['s3_key']
    invoke_npi_registry_search_etl(source_key=s3_key)

    # SAM Registrations
    sam_params = [
        {
            'exclusionName': f'{r.first_name} {r.last_name}',
            'classification': 'Individual',
            's3_bucket': 'vidaverified--raw-document-data',
        }
        for r in report_requests
    ]
    results = invoke_sam_exclusions_search_crawler(sam_params)
    s3_key = results['result']['s3_key']
    invoke_sam_exclusions_search_etl(source_key=s3_key)
