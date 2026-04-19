from django.contrib import admin
from rest_framework_api_key.models import APIKey

from practices.models import (
    Practice,
    Provider,
    ProviderByPractice,
)

from .forms import (
    PracticeAddForm,
    PracticeChangeForm,
    ProviderAddForm,
    ProviderChangeForm,
)

admin.site.unregister(APIKey)


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
                'ssn',
                'zip_code',
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
                'ssn',
                'zip_code',
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
