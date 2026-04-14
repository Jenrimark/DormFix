from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'status', 'handled_by', 'created_at', 'updated_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('content', 'admin_reply', 'user__username', 'user__real_name')
    readonly_fields = ('created_at', 'updated_at')

