from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """自定义用户管理"""
    
    list_display = ['username', 'email', 'role', 'phone', 'dorm_code', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'phone', 'dorm_code']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': ('role', 'phone', 'dorm_code', 'avatar')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {
            'fields': ('role', 'phone', 'dorm_code')
        }),
    )
