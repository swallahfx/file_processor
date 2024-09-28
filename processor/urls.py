from rest_framework.routers import DefaultRouter

from .views import ReconciliationViewSet

router = DefaultRouter()
router.register(r'processor', ReconciliationViewSet, basename='processor')

urlpatterns = router.urls
