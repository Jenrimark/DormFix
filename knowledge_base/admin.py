from django.contrib import admin

from .models import KnowledgeItem, QALog, KnowledgeDocument


@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'role_scope', 'is_active', 'updated_at')
    list_filter = ('category', 'role_scope', 'is_active')
    search_fields = ('title', 'content')
    ordering = ('-updated_at',)


@admin.register(QALog)
class QALogAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'success', 'created_at')
    list_filter = ('role', 'success')
    search_fields = ('question', 'answer', 'error_message')
    ordering = ('-created_at',)


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_filename', 'role_scope', 'parse_status', 'is_active', 'updated_at')
    list_filter = ('role_scope', 'parse_status', 'is_active')
    search_fields = ('title', 'original_filename')
    ordering = ('-updated_at',)

