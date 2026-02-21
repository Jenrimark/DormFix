from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_real_name = serializers.CharField(source='author.real_name', read_only=True)
    
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'author', 'author_name', 'author_real_name', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # 自动设置作者为当前用户
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
