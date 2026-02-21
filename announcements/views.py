from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Announcement
from .serializers import AnnouncementSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """只有管理员可以创建/编辑/删除，所有人可以查看"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 3


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def latest(self, request):
        """获取最新的3条公告（公开接口）"""
        announcements = self.queryset[:3]
        serializer = self.get_serializer(announcements, many=True)
        return Response(serializer.data)
