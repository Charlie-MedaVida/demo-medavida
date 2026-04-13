from django.contrib import admin

from .forms import ReportRequestAddForm, ReportRequestChangeForm
from .models import ReportProxy, ReportRequestProxy


@admin.register(ReportRequestProxy)
class ReportRequestAdmin(admin.ModelAdmin):

    add_fieldsets = (
        (None, {
            'fields': (
                ('first_name', 'last_name'),
                'city',
                'state',
                'postal_code',
                'ssn',
                'ein',
                'id_type',
            ),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = ReportRequestAddForm
        else:
            kwargs['form'] = ReportRequestChangeForm
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReportProxy)
class ReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
