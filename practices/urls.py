from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    DeaCertificateUploadView,
    DeaCredentialCreateView,
    NpiCredentialCreateView,
    NppesSearchView,
    PracticeProviderCreateView,
    PracticeViewSet,
    ProviderTitleListView,
    ProviderViewSet,
)

app_name = 'practices'

router = DefaultRouter()
router.register('practices', PracticeViewSet, basename='practice')
router.register('providers', ProviderViewSet, basename='provider')

urlpatterns = router.urls + [
    path(
        'nppes/search',
        NppesSearchView.as_view(),
        name='nppes-search',
    ),
    path(
        'provider-titles',
        ProviderTitleListView.as_view(),
        name='provider-title-list',
    ),
    path(
        'practice/<uuid:practice_id>/providers/',
        PracticeProviderCreateView.as_view(),
        name='practice-provider-create',
    ),
    path(
        'providers/<uuid:provider_id>/npi-credentials/',
        NpiCredentialCreateView.as_view(),
        name='provider-npi-credential-create',
    ),
    path(
        'providers/<uuid:provider_id>/dea-credentials/',
        DeaCredentialCreateView.as_view(),
        name='provider-dea-credential-create',
    ),
    path(
        'providers/<uuid:provider_id>/dea-credentials/certificate/',
        DeaCertificateUploadView.as_view(),
        name='provider-dea-certificate-upload',
    ),
]
