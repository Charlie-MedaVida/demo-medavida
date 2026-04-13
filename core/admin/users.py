from django.contrib import admin
from ..models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "credit_count",
    )
    fieldsets = (
        (
            "Private", {
                "fields": (
                    "id",
                    "user",
                    "credit_count",
                ),
            }
        ),
    )
    readonly_fields = (
        "id",
        "user",
        "credit_count",
    )
