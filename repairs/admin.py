from django.contrib import admin
from .models import RepairType, WorkOrder, OrderLog, Comment


@admin.register(RepairType)
class RepairTypeAdmin(admin.ModelAdmin):
    """故障类型管理"""
    
    list_display = ['name', 'priority', 'created_at']
    list_filter = ['priority']
    search_fields = ['name']
    ordering = ['id']


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    """工单管理"""
    
    list_display = ['order_sn', 'user', 'repair_type', 'status', 'priority', 'repairman', 'create_time']
    list_filter = ['status', 'priority', 'repair_type', 'create_time']
    search_fields = ['order_sn', 'user__username', 'content']
    readonly_fields = ['order_sn', 'create_time']
    ordering = ['-create_time']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('order_sn', 'user', 'repair_type', 'status', 'priority')
        }),
        ('详细内容', {
            'fields': ('content', 'img_proof', 'remark')
        }),
        ('派单信息', {
            'fields': ('repairman', 'finish_time')
        }),
        ('时间信息', {
            'fields': ('create_time',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """保存时自动记录日志"""
        super().save_model(request, obj, form, change)
        
        # 如果是新建，记录提交日志
        if not change:
            OrderLog.objects.create(
                work_order=obj,
                operator=request.user,
                action='submit',
                remark='工单提交'
            )


@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    """工单日志管理"""
    
    list_display = ['work_order', 'operator', 'action', 'create_time']
    list_filter = ['action', 'create_time']
    search_fields = ['work_order__order_sn', 'operator__username']
    readonly_fields = ['create_time']
    ordering = ['-create_time']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """评价管理"""
    
    list_display = ['work_order', 'score', 'create_time']
    list_filter = ['score', 'create_time']
    search_fields = ['work_order__order_sn', 'feedback']
    readonly_fields = ['create_time']
    ordering = ['-create_time']
