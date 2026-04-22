from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CurrentPracticeView,
    PracticeReportView,
    DeaCertificateUploadView,
    DeaCredentialCreateView,
    NpiCredentialCreateView,
    NppesSearchView,
    PracticeProviderCreateView,
    PracticeViewSet,
    ProviderTitleListView,
    ProviderVerifyView,
    ProviderViewSet,
)

app_name = 'practices'

router = DefaultRouter()
router.register('practices', PracticeViewSet, basename='practice')
router.register('providers', ProviderViewSet, basename='provider')

urlpatterns = router.urls + [
    path(
        'practices/current',
        CurrentPracticeView.as_view(),
        name='practice-current',
    ),
    path(
        'practices/<uuid:practice_id>/report',
        PracticeReportView.as_view(),
        name='practice-report',
    ),
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
        'providers/<uuid:provider_id>/verify',
        ProviderVerifyView.as_view(),
        name='provider-verify',
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
