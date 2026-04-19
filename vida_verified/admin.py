from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.contrib import admin, messages

from .models import (
    DeaCredential,
    DeaVerificationView,
    NpiCredential,
    NpiVerificationView,
)


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


@admin.register(NpiVerificationView)
class NpiVerificationViewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'license_number', 'verified',
        'checked_at', 'enumeration_date', 'expiration_date',
    )
    readonly_fields = (
        'id', 'license_number', 'last_checked_at',
        'enumeration_date', 'expiration_date',
        'checked_at', 'verified', 'error_content', 'json_content',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DeaVerificationView)
class DeaVerificationViewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'license_number', 'verified',
        'checked_at', 'enumeration_date', 'expiration_date',
    )
    readonly_fields = (
        'id', 'license_number', 'last_checked_at',
        'enumeration_date', 'expiration_date',
        'checked_at', 'verified', 'error_content', 'json_content',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
