from rest_framework.routers import DefaultRouter

from .views import KnowledgeItemViewSet, KnowledgeDocumentViewSet

router = DefaultRouter()
router.register(r'knowledge', KnowledgeItemViewSet, basename='knowledge')
router.register(r'knowledge-documents', KnowledgeDocumentViewSet, basename='knowledge-document')

urlpatterns = router.urls

