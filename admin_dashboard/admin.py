from django.contrib import admin
from rest_framework_api_key.models import APIKey

from practices.models import Practice, Provider, ProviderByPractice
from vida_verified.models import (
    MonitorRequest,
    MonitorResults,
    ReportRequest,
    ReportResults,
)

from .forms import (
    MonitorRequestAddForm,
    MonitorRequestChangeForm,
    MonitorResultsChangeForm,
    PracticeAddForm,
    PracticeChangeForm,
    ProviderAddForm,
    ProviderChangeForm,
    ReportChangeForm,
    ReportRequestAddForm,
    ReportRequestChangeForm,
)

admin.site.unregister(APIKey)


class BaseRequestAdmin(admin.ModelAdmin):
    add_form_class = None
    change_form_class = None

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
            kwargs['form'] = self.add_form_class
        else:
            kwargs['form'] = self.change_form_class
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class BaseResultsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


@admin.register(ReportRequest)
class ReportRequestAdmin(BaseRequestAdmin):
    add_form_class = ReportRequestAddForm
    change_form_class = ReportRequestChangeForm


@admin.register(MonitorRequest)
class MonitorRequestAdmin(BaseRequestAdmin):
    add_form_class = MonitorRequestAddForm
    change_form_class = MonitorRequestChangeForm


@admin.register(ReportResults)
class ReportResultsAdmin(BaseResultsAdmin):
    form = ReportChangeForm
    readonly_fields = ('sam_exclusions_results', 'npi_registration_results')


@admin.register(MonitorResults)
class MonitorResultsAdmin(BaseResultsAdmin):
    form = MonitorResultsChangeForm
    readonly_fields = ('sam_exclusions_results', 'npi_registration_results')


class ProviderByPracticeInline(admin.TabularInline):
    model = ProviderByPractice
    extra = 1


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    add_form_class = PracticeAddForm
    change_form_class = PracticeChangeForm
    inlines = [ProviderByPracticeInline]

    add_fieldsets = (
        (None, {
            'fields': (
                'name', 'email', 'phone_number', 'tax_id', 'npi_number',
            ),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form_class
        else:
            kwargs['form'] = self.change_form_class
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    add_form_class = ProviderAddForm
    change_form_class = ProviderChangeForm
    inlines = [ProviderByPracticeInline]

    add_fieldsets = (
        (None, {
            'fields': (
                ('first_name', 'last_name'),
                'email',
                'phone_number',
                'title',
                'specialty',
            ),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form_class
        else:
            kwargs['form'] = self.change_form_class
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
