from rest_framework.routers import DefaultRouter

from .views import PracticeViewSet, ProviderViewSet

app_name = 'practices'

router = DefaultRouter()
router.register('practices', PracticeViewSet, basename='practice')
router.register('providers', ProviderViewSet, basename='provider')

urlpatterns = router.urls
