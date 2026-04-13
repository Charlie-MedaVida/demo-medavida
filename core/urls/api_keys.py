from django.urls import path
from ..views.api_keys import ApiKeyRetrieveUpdateAPIView


app_name = 'api_keys'


urlpatterns = [
    path(
        '',
        ApiKeyRetrieveUpdateAPIView.as_view(),
        name=ApiKeyRetrieveUpdateAPIView.name
    ),
]
