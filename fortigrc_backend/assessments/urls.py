from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet, EvidenceViewSet

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet)
router.register(r'evidence', EvidenceViewSet)

urlpatterns = router.urls
