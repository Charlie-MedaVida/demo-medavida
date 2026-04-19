from django.contrib import admin

from .models import ProviderVerificationView


@admin.register(ProviderVerificationView)
class ProviderVerificationViewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name',
        'npi_verification_status', 'dea_verification_status',
        'npi_verified', 'dea_verified',
    )
    readonly_fields = (
        'id', 'first_name', 'last_name', 'email', 'phone_number',
        'title', 'specialty',
        'npi_verification_status', 'npi_credential_id',
        'npi_license_number', 'npi_verified', 'npi_checked_at',
        'npi_enumeration_date', 'npi_expiration_date', 'npi_error_content',
        'dea_verification_status', 'dea_credential_id',
        'dea_license_number', 'dea_verified', 'dea_checked_at',
        'dea_enumeration_date', 'dea_expiration_date', 'dea_error_content',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
