from vida_verified.models import Report, ReportRequest


class ReportRequestProxy(ReportRequest):
    class Meta:
        proxy = True
        verbose_name = 'Report Request'
        verbose_name_plural = 'Report Requests'


class ReportProxy(Report):
    class Meta:
        proxy = True
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
