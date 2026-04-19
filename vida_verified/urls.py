from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeaCredentialViewSet, NpiCredentialViewSet

app_name = 'vida_verified'

router = DefaultRouter()
router.register('npi-credentials', NpiCredentialViewSet, basename='npi-credential')
router.register('dea-credentials', DeaCredentialViewSet, basename='dea-credential')

urlpatterns = [
    path('', include(router.urls)),
]
