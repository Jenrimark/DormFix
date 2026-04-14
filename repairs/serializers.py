from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import RepairType, WorkOrder, OrderLog, Comment
from accounts.serializers import UserSerializer


class RepairTypeSerializer(serializers.ModelSerializer):
    """故障类型序列化器"""
    
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = RepairType
        fields = ['id', 'category', 'category_display', 'name', 'priority', 
                  'priority_display', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderLogSerializer(serializers.ModelSerializer):
    """工单日志序列化器"""
    
    operator_info = UserSerializer(source='operator', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = OrderLog
        fields = ['id', 'work_order', 'operator', 'operator_info', 
                  'action', 'action_display', 'remark', 'create_time']
        read_only_fields = ['id', 'create_time']


class CommentSerializer(serializers.ModelSerializer):
    """评价序列化器"""
    
    class Meta:
        model = Comment
        fields = ['id', 'work_order', 'score', 'feedback', 'create_time']
        read_only_fields = ['id', 'create_time']

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        work_order = attrs.get('work_order')
        score = attrs.get('score')

        if work_order is None:
            raise serializers.ValidationError({'work_order': '请选择要评价的工单'})

        # 仅学生可评价，且只能评价自己的工单
        if not user or not user.is_authenticated:
            raise serializers.ValidationError('未登录')
        if not user.is_student():
            raise serializers.ValidationError('只有学生可以评价')
        if work_order.user_id != user.id:
            raise serializers.ValidationError({'work_order': '只能评价自己的工单'})

        # 仅已完成工单可评价
        if work_order.status != 3:
            raise serializers.ValidationError({'work_order': '只有已完成工单可以评价'})

        # 每工单最多评价一次（OneToOne 再加业务校验，返回更友好错误）
        if hasattr(work_order, 'comment'):
            raise serializers.ValidationError({'work_order': '该工单已评价，不能重复提交'})

        # 评分范围兜底（模型 choices 已约束，但这里给明确错误）
        if score is None or not (1 <= int(score) <= 5):
            raise serializers.ValidationError({'score': '评分必须在 1-5 之间'})

        return attrs


class WorkOrderSerializer(serializers.ModelSerializer):
    """工单序列化器"""
    
    user_info = UserSerializer(source='user', read_only=True)
    repairman_info = UserSerializer(source='repairman', read_only=True)
    reviewer_info = UserSerializer(source='reviewer', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    logs = OrderLogSerializer(many=True, read_only=True)
    # 反向 OneToOne：当尚未评价时，直接访问 obj.comment 会抛 RelatedObjectDoesNotExist。
    # 用方法字段保证列表/详情序列化稳定返回 null。
    comment = serializers.SerializerMethodField(read_only=True)
    
    # 添加 repair_type_info 字段以兼容前端
    repair_type_info = serializers.SerializerMethodField(read_only=True)
    
    def get_repair_type_info(self, obj):
        """根据 category 返回故障类型信息"""
        return {
            'name': obj.get_category_display()
        }

    def get_comment(self, obj):
        try:
            comment = obj.comment
        except ObjectDoesNotExist:
            return None
        return CommentSerializer(comment).data
    
    class Meta:
        model = WorkOrder
        fields = ['id', 'order_sn', 'user', 'user_info', 'category', 
                  'category_display', 'status', 'status_display', 'priority', 
                  'priority_display', 'content', 'img_proof', 'repairman', 
                  'repairman_info', 'reviewer', 'reviewer_info', 'create_time', 
                  'review_time', 'review_remark', 'accept_time', 'start_time',
                  'finish_time', 'repair_proof_img', 'repair_description', 'remark',
                  'logs', 'comment', 'repair_type_info']
        read_only_fields = ['id', 'order_sn', 'user', 'create_time']


class WorkOrderCreateSerializer(serializers.ModelSerializer):
    """工单创建序列化器"""
    
    class Meta:
        model = WorkOrder
        fields = ['category', 'priority', 'content', 'img_proof']
    
    def create(self, validated_data):
        """创建工单并记录日志"""
        # 从 context 中获取当前用户
        user = self.context['request'].user
        validated_data['user'] = user
        
        # 创建工单
        work_order = WorkOrder.objects.create(**validated_data)
        
        # 记录提交日志
        OrderLog.objects.create(
            work_order=work_order,
            operator=user,
            action='submit',
            remark='工单提交'
        )
        
        return work_order


class WorkOrderUpdateSerializer(serializers.ModelSerializer):
    """工单更新序列化器（管理员/维修员使用）"""
    
    class Meta:
        model = WorkOrder
        fields = ['status', 'repairman', 'remark', 'finish_time']
    
    def update(self, instance, validated_data):
        """更新工单并记录日志"""
        user = self.context['request'].user
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # 更新工单
        instance = super().update(instance, validated_data)
        
        # 根据状态变化记录日志
        if old_status != new_status:
            action_map = {
                0: 'submit',
                1: 'assign',
                2: 'start',
                3: 'complete',
                4: 'cancel',
            }
            action = action_map.get(new_status, 'review')
            
            OrderLog.objects.create(
                work_order=instance,
                operator=user,
                action=action,
                remark=validated_data.get('remark', '')
            )
        
        return instance


class WorkOrderStatisticsSerializer(serializers.Serializer):
    """工单统计序列化器"""
    
    total = serializers.IntegerField(help_text='总工单数')
    pending = serializers.IntegerField(help_text='待审核')
    assigned = serializers.IntegerField(help_text='已派单')
    in_progress = serializers.IntegerField(help_text='维修中')
    completed = serializers.IntegerField(help_text='已完成')
    cancelled = serializers.IntegerField(help_text='已取消')
    avg_response_time = serializers.FloatField(help_text='平均响应时间（小时）')
