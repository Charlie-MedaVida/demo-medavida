from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.contrib import admin
from django.contrib import messages
from rest_framework_api_key.models import APIKey

from practices.models import (
    DeaCredential,
    NpiCredential,
    Practice,
    Provider,
    ProviderByPractice,
)
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


@admin.register(NpiCredential)
class NpiCredentialAdmin(admin.ModelAdmin):
    fields = (
        'license_number', 'last_checked_at',
        'enumeration_date', 'expiration_date', 'file',
    )


@admin.register(DeaCredential)
class DeaCredentialAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    fields = (
        'license_number', 'last_checked_at',
        'enumeration_date', 'expiration_date', 'file',
    )

    @button(
        label='Run DEA License Extraction',
        change_form=True,
        html_attrs={'style': 'background:#417690;color:#fff;'},
    )
    def run_extraction(self, request, pk):
        from simple_dag_orchestrator.dags import run_dea_license_extraction
        run_dea_license_extraction.delay(str(pk))
        self.message_user(
            request,
            'DEA license extraction task queued.',
            messages.SUCCESS,
        )


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
    readonly_fields = (
        'npi_license_number', 'npi_last_checked_at',
        'npi_enumeration_date', 'npi_expiration_date', 'npi_file',
        'dea_license_number', 'dea_last_checked_at',
        'dea_enumeration_date', 'dea_expiration_date', 'dea_file',
    )

    list_display = (
        'first_name', 'last_name', 'title',
        'has_npi_credential', 'has_dea_credential',
    )

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

    change_fieldsets = (
        (None, {
            'fields': (
                ('first_name', 'last_name'),
                'email',
                'phone_number',
                'title',
                'specialty',
            ),
        }),
        ('NPI Credential', {
            'fields': (
                'npi_license_number', 'npi_last_checked_at',
                'npi_enumeration_date', 'npi_expiration_date', 'npi_file',
            ),
        }),
        ('DEA Credential', {
            'fields': (
                'dea_license_number', 'dea_last_checked_at',
                'dea_enumeration_date', 'dea_expiration_date', 'dea_file',
            ),
        }),
    )

    def _credential_field(self, obj, credential_attr, field):
        credential = getattr(obj, credential_attr, None)
        return getattr(credential, field, '—') if credential else '—'

    def npi_license_number(self, obj):
        return self._credential_field(obj, 'npi_credential', 'license_number')

    def npi_last_checked_at(self, obj):
        return self._credential_field(obj, 'npi_credential', 'last_checked_at')

    def npi_enumeration_date(self, obj):
        return self._credential_field(
            obj, 'npi_credential', 'enumeration_date',
        )

    def npi_expiration_date(self, obj):
        return self._credential_field(
            obj, 'npi_credential', 'expiration_date',
        )

    def npi_file(self, obj):
        return self._credential_field(obj, 'npi_credential', 'file')

    def dea_license_number(self, obj):
        return self._credential_field(obj, 'dea_credential', 'license_number')

    def dea_last_checked_at(self, obj):
        return self._credential_field(obj, 'dea_credential', 'last_checked_at')

    def dea_enumeration_date(self, obj):
        return self._credential_field(
            obj, 'dea_credential', 'enumeration_date',
        )

    def dea_expiration_date(self, obj):
        return self._credential_field(obj, 'dea_credential', 'expiration_date')

    def dea_file(self, obj):
        return self._credential_field(obj, 'dea_credential', 'file')

    @admin.display(boolean=True, description='NPI Credential')
    def has_npi_credential(self, obj):
        return obj.npi_credential is not None

    @admin.display(boolean=True, description='DEA Credential')
    def has_dea_credential(self, obj):
        return obj.dea_credential is not None

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form_class
        else:
            kwargs['form'] = self.change_form_class
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return self.change_fieldsets
