from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepairTypeViewSet, WorkOrderViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'repair-types', RepairTypeViewSet, basename='repair-type')
router.register(r'work-orders', WorkOrderViewSet, basename='work-order')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
