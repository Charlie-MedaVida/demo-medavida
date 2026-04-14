from django.db import models
from django_materialized_view.base_model import MaterializedViewModel


class BaseRequest(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'Running'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETE = 'COMPLETE', 'Complete'
        FAILED = 'FAILED', 'Failed'

    class IdTypeChoices(models.TextChoices):
        SSN = 'SSN', 'SSN'
        EIN = 'EIN', 'EIN'

    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    postal_code = models.CharField(max_length=20, blank=True, default='')
    ssn = models.CharField(max_length=11, blank=True, default='')
    ein = models.CharField(max_length=10, blank=True, default='')
    id_type = models.CharField(
        max_length=3,
        choices=IdTypeChoices.choices,
        blank=True,
        default='',
    )
    status = models.CharField(
        max_length=24,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MonitorRequest(BaseRequest):
    pass


class ReportRequest(BaseRequest):
    pass


class BaseResults(models.Model):

    request_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    result = models.CharField(max_length=24)
    sam_exclusions = models.TextField(blank=True, null=True)
    npi_registration = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class ReportResults(BaseResults):

    content = models.TextField(blank=True, null=True)


class MonitorResults(BaseResults):

    content = models.TextField(blank=True, null=True)


class MonitorResultsView(MaterializedViewModel):
    create_pkey_index = True

    monitor_results_id = models.IntegerField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    result = models.CharField(max_length=24, blank=True)
    results_created_at = models.DateTimeField()
    results_updated_at = models.DateTimeField()
    request_id = models.IntegerField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    ssn = models.CharField(max_length=11)
    ein = models.CharField(max_length=10)
    id_type = models.CharField(max_length=3)
    status = models.CharField(max_length=24)
    request_created_at = models.DateTimeField()
    request_updated_at = models.DateTimeField()

    class Meta:
        managed = False

    @staticmethod
    def get_query_from_queryset():
        return MonitorResults.objects.select_related('request').values(
            monitor_results_id=models.F('id'),
            content=models.F('content'),
            result=models.F('result'),
            results_created_at=models.F('created_at'),
            results_updated_at=models.F('updated_at'),
            request_id=models.F('request__id'),
            first_name=models.F('request__first_name'),
            last_name=models.F('request__last_name'),
            city=models.F('request__city'),
            state=models.F('request__state'),
            postal_code=models.F('request__postal_code'),
            ssn=models.F('request__ssn'),
            ein=models.F('request__ein'),
            id_type=models.F('request__id_type'),
            status=models.F('request__status'),
            request_created_at=models.F('request__created_at'),
            request_updated_at=models.F('request__updated_at'),
        )


class ReportResultsView(MaterializedViewModel):
    create_pkey_index = True

    report_results_id = models.IntegerField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    result = models.CharField(max_length=24, blank=True)
    results_created_at = models.DateTimeField()
    request_id = models.IntegerField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    ssn = models.CharField(max_length=11)
    ein = models.CharField(max_length=10)
    id_type = models.CharField(max_length=3)
    status = models.CharField(max_length=24)
    request_created_at = models.DateTimeField()
    request_updated_at = models.DateTimeField()

    class Meta:
        managed = False

    @staticmethod
    def get_query_from_queryset():
        return ReportResults.objects.select_related('request').values(
            report_results_id=models.F('id'),
            content=models.F('content'),
            result=models.F('result'),
            results_created_at=models.F('created_at'),
            request_id=models.F('request__id'),
            first_name=models.F('request__first_name'),
            last_name=models.F('request__last_name'),
            city=models.F('request__city'),
            state=models.F('request__state'),
            postal_code=models.F('request__postal_code'),
            ssn=models.F('request__ssn'),
            ein=models.F('request__ein'),
            id_type=models.F('request__id_type'),
            status=models.F('request__status'),
            request_created_at=models.F('request__created_at'),
            request_updated_at=models.F('request__updated_at'),
        )
