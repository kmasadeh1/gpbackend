from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, RiskViewSet

router = DefaultRouter()
router.register(r'assets', AssetViewSet)
router.register(r'risks', RiskViewSet)

urlpatterns = router.urls
