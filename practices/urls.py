from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
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
        'provider-titles',
        ProviderTitleListView.as_view(),
        name='provider-title-list',
    ),
    path(
        'practice/<uuid:practice_id>/providers/',
        PracticeProviderCreateView.as_view(),
        name='practice-provider-create',
    ),
]
