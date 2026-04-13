from django.contrib import admin

from .forms import ReportRequestAddForm, ReportRequestChangeForm
from .models import ReportProxy, ReportRequestProxy


@admin.register(ReportRequestProxy)
class ReportRequestAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = ReportRequestAddForm
        else:
            kwargs['form'] = ReportRequestChangeForm
        return super().get_form(request, obj, **kwargs)


@admin.register(ReportProxy)
class ReportAdmin(admin.ModelAdmin):
    pass
