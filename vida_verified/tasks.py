from celery import shared_task


@shared_task
def async_run_report(report_request_pk):
    pass
