from django.urls import path
from ..views.products import ProductListAPIView


app_name = 'products'


urlpatterns = [
    path(
        '',
        ProductListAPIView.as_view(),
        name=ProductListAPIView.name,
    ),
]
