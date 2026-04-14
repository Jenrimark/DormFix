from django.utils import timezone
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Feedback
from .permissions import IsAdmin
from .serializers import FeedbackSerializer, FeedbackAdminUpdateSerializer
from notifications.models import Notification


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('user', 'handled_by').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'admin_reply', 'user__username', 'user__real_name']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        # 非管理员仅可看自己的反馈
        if not user.is_admin():
            qs = qs.filter(user=user)

        status_q = self.request.query_params.get('status')
        if status_q:
            qs = qs.filter(status=status_q)

        category_q = self.request.query_params.get('category')
        if category_q:
            qs = qs.filter(category=category_q)

        return qs

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update', 'handle']:
            return FeedbackAdminUpdateSerializer
        return FeedbackSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'handle']:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        if not user.is_admin() and obj.user_id != user.id:
            return Response({'error': '无权访问'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def my(self, request):
        qs = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = FeedbackSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = FeedbackSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def handle(self, request, pk=None):
        """
        管理员处理反馈：更新状态/回复，并记录处理人、处理时间。
        """
        feedback = self.get_object()
        old_reply = feedback.admin_reply or ''
        old_status = feedback.status
        serializer = FeedbackAdminUpdateSerializer(feedback, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        if 'handled_by' not in data:
            data['handled_by'] = request.user
        if 'handled_at' not in data:
            data['handled_at'] = timezone.now()

        serializer.save(**data)

        # 管理员新增/更新回复时，给用户发站内通知（用于红点提示）
        new_reply = (feedback.admin_reply or '').strip()
        if 'admin_reply' in serializer.validated_data and new_reply and new_reply != old_reply.strip():
            Notification.objects.create(
                user=feedback.user,
                type=Notification.Type.FEEDBACK_REPLY,
                title='你的反馈有新回复',
                content=new_reply,
                feedback=feedback,
            )

        # 若未回复但状态发生变化，也可选通知（本次仅在状态变化时给一条简短通知）
        if 'status' in serializer.validated_data and feedback.status != old_status and not ('admin_reply' in serializer.validated_data and new_reply):
            Notification.objects.create(
                user=feedback.user,
                type=Notification.Type.FEEDBACK_REPLY,
                title='你的反馈状态已更新',
                content=f'当前状态：{feedback.get_status_display()}',
                feedback=feedback,
            )

        return Response(FeedbackSerializer(feedback).data)

