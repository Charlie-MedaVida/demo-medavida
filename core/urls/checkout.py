from django.urls import path
from ..views import checkout


app_name = 'checkout'


urlpatterns = [
    path(
        'create-checkout-session',
        checkout.CreateCheckoutView.as_view(),
        name=checkout.CreateCheckoutView.name
    ),
    path(
        'session-status/webhook',
        checkout.CheckoutWebhookApiView.as_view(),
        name=checkout.CheckoutWebhookApiView.name
    ),
    path(
        'session-status',
        checkout.CheckoutStatusRetrieveApiView.as_view(),
        name=checkout.CheckoutStatusRetrieveApiView.name
    ),
]
