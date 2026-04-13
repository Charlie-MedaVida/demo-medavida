from django.contrib import admin
from ..models import UserAPIKey


@admin.register(UserAPIKey)
class UserAPIKeyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "revoked",
        "expiry_date",
    )
    fieldsets = (
        (
            "Private", {
                "fields": (
                    "id",
                    "name",
                    "key",
                    "user",
                    "revoked",
                    "expiry_date",
                ),
            }
        ),
    )
    readonly_fields = (
        "id",
        "key",
        "user",
        "revoked",
        "expiry_date",
    )
