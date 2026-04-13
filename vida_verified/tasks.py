from celery import shared_task

from .models import ReportRequest
from .services import invoke_api_crawler, invoke_crawler


@shared_task
def async_run_report(report_request_pk):
    report_request = ReportRequest.objects.get(pk=report_request_pk)

    report_request.status = ReportRequest.StatusChoices.PROCESSING
    report_request.save()

    invoke_api_crawler()
    invoke_crawler()

    report_request.status = ReportRequest.StatusChoices.COMPLETE
    report_request.save()