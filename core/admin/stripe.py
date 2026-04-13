from django.contrib import admin
from admin_extra_buttons.api import ExtraButtonsMixin, button
from ..models import StripePrice
from ..tasks import sync_stripe_prices_task


@admin.register(StripePrice)
class StripePriceAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ("id", "lookup_key")

    @button()
    def refresh(self, request):
        sync_stripe_prices_task.delay()
