from django.contrib import admin
from rest_framework_api_key.models import APIKey
from vida_verified.models import Report, ReportRequest

from .forms import ReportRequestAddForm, ReportRequestChangeForm

admin.site.unregister(APIKey)


@admin.register(ReportRequest)
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
            ReportRequest.objects.create(
                user=request.user,
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
                city=form.cleaned_data.get('city', ''),
                state=form.cleaned_data.get('state', ''),
                postal_code=form.cleaned_data.get('postal_code', ''),
                ssn=form.cleaned_data.get('ssn', ''),
                ein=form.cleaned_data.get('ein', ''),
                id_type=form.cleaned_data.get('id_type', ''),
            )
        else:
            super().save_model(request, obj, form, change)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False