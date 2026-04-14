from rest_framework import serializers

from .models import KnowledgeItem, QALog, KnowledgeDocument


class KnowledgeItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    role_scope_display = serializers.CharField(source='get_role_scope_display', read_only=True)

    class Meta:
        model = KnowledgeItem
        fields = [
            'id',
            'title',
            'category',
            'category_display',
            'role_scope',
            'role_scope_display',
            'content',
            'is_active',
            'created_at',
            'updated_at',
        ]


class AskKnowledgeSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)


class QALogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QALog
        fields = ['id', 'role', 'question', 'answer', 'success', 'error_message', 'created_at']


class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    role_scope_display = serializers.CharField(source='get_role_scope_display', read_only=True)

    class Meta:
        model = KnowledgeDocument
        fields = [
            'id',
            'title',
            'role_scope',
            'role_scope_display',
            'file',
            'original_filename',
            'extracted_text',
            'parse_status',
            'parse_error',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['original_filename', 'extracted_text', 'parse_status', 'parse_error']

