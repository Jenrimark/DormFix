from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    handled_by_info = UserSerializer(source='handled_by', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id',
            'user',
            'user_info',
            'category',
            'category_display',
            'content',
            'contact',
            'status',
            'status_display',
            'admin_reply',
            'handled_by',
            'handled_by_info',
            'handled_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'status',
            'admin_reply',
            'handled_by',
            'handled_at',
            'created_at',
            'updated_at',
        ]


class FeedbackAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['status', 'admin_reply', 'handled_by', 'handled_at']

