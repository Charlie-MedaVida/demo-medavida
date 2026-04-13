from django.contrib import admin

from .forms import ReportRequestAdminForm
from .models import ReportProxy, ReportRequestProxy


@admin.register(ReportRequestProxy)
class ReportRequestAdmin(admin.ModelAdmin):
    form = ReportRequestAdminForm


@admin.register(ReportProxy)
class ReportAdmin(admin.ModelAdmin):
    pass
