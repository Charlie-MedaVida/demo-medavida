from celery import shared_task


@shared_task
def run_report_dag():
    # Get the pending reports

    # bulk update the status of the reports objects to Running

    # NPI Registrations
    params = npi_registrations_params()
    results = call_npi_registrations_search(params)
    results = transform_npi_registrations_search(results)

    # SAM Registrations
    call_sam_exclusions_search()
    transform_sam_exclusions_search()
    pass


def npi_registrations_params():
    pass


def call_npi_registrations_search():
    pass


def transform_npi_registrations_search():
    pass


def call_dea_registrations_search():
    pass


def transform_dea_registrations_search():
    pass


def call_sam_exclusions_search():
    pass


def transform_sam_exclusions_search():
    pass


def reload_athena_table():
    pass


def load_reports():
    pass
