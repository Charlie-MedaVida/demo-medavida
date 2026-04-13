from django.contrib import admin
from django.db.models.signals import post_save
from rest_framework_api_key.models import APIKey
from vida_verified.models import ReportRequest

from .forms import ReportRequestAddForm, ReportRequestChangeForm
from .models import ReportProxy, ReportRequestProxy

admin.site.unregister(APIKey)


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
        # The signal handler is registered for sender=ReportRequest,
        # but saving via the admin uses ReportRequestProxy — Django fires
        # post_save with the proxy as sender, so the handler never matches.
        # The fix is to explicitly send the signal with ReportRequest as the
        # sender from save_model.
        post_save.send(sender=ReportRequest, instance=obj, created=not change)


@admin.register(ReportProxy)
class ReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
