import json

from celery import shared_task

from .models import (
    DcdCredentialStatus,
    NpiCredentialStatus,
    Report,
    ReportRequest
)
from .services import invoke_api_crawler, invoke_crawler


@shared_task
def async_run_report(report_request_pk):
    report_request = ReportRequest.objects.get(pk=report_request_pk)

    report_request.status = ReportRequest.StatusChoices.PROCESSING
    report_request.save()

    report = Report.objects.create(request=report_request)

    npi_status = NpiCredentialStatus.objects.create(report=report)
    crawler = 'npi_registry.search_api_v2_1'
    params = {
        'first_name': report_request.first_name,
        'last_name': report_request.last_name,
        'city': report_request.city,
        'state': report_request.state,
        'postal_code': report_request.postal_code,
        'ssn': report_request.ssn,
        'ein': report_request.ein,
        'id_type': report_request.id_type,
    }
    api_response = invoke_api_crawler(crawler, params)
    npi_status.json_content = json.dumps(api_response)
    npi_status.save()

    report_request.status = ReportRequest.StatusChoices.COMPLETE
    report_request.save()
