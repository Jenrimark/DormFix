from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.http import HttpResponse, Http404
from datetime import timedelta
from .models import RepairType, WorkOrder, OrderLog, Comment, StoredFile
from .serializers import (
    RepairTypeSerializer, WorkOrderSerializer, WorkOrderCreateSerializer,
    WorkOrderUpdateSerializer, OrderLogSerializer, CommentSerializer,
    WorkOrderStatisticsSerializer
)
from .permissions import IsStudent, IsRepairman, IsAdmin


class RepairTypeViewSet(viewsets.ModelViewSet):
    """故障类型视图集"""
    
    queryset = RepairType.objects.all()
    serializer_class = RepairTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # 关闭分页，返回所有故障类型
    
    def get_permissions(self):
        """只有管理员可以增删改，其他人只能查看"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return super().get_permissions()


class WorkOrderViewSet(viewsets.ModelViewSet):
    """工单视图集"""
    
    queryset = WorkOrder.objects.select_related(
        'user', 'repairman'
    ).prefetch_related('logs', 'comment').all()
    
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_sn', 'content', 'user__username']
    ordering_fields = ['create_time', 'status', 'priority']
    ordering = ['-create_time']
    
    def get_serializer_class(self):
        """根据不同的 action 返回不同的序列化器"""
        if self.action == 'create':
            return WorkOrderCreateSerializer
        elif self.action in ['update', 'partial_update', 'assign', 'update_status']:
            return WorkOrderUpdateSerializer
        return WorkOrderSerializer
    
    def get_queryset(self):
        """根据用户角色过滤工单"""
        user = self.request.user
        queryset = super().get_queryset()
        
        # 学生只能看到自己的工单
        if user.is_student():
            return queryset.filter(user=user)
        
        # 维修人员只能看到派给自己的工单
        elif user.is_repairman():
            return queryset.filter(repairman=user)
        
        # 管理员可以看到所有工单
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """获取单个工单详情 - 增强权限检查"""
        instance = self.get_object()
        user = request.user
        
        # 学生只能访问自己的工单
        if user.is_student() and instance.user != user:
            return Response(
                {'error': '无权访问此工单', 'code': 'ORDER_ACCESS_DENIED'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 维修人员只能访问分配给自己的工单
        if user.is_repairman() and instance.repairman != user:
            return Response(
                {'error': '无权访问此工单', 'code': 'ORDER_ACCESS_DENIED'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """更新工单 - 增强权限检查"""
        instance = self.get_object()
        user = request.user
        
        # 学生只能更新自己的工单
        if user.is_student() and instance.user != user:
            return Response(
                {'error': '无权修改此工单', 'code': 'ORDER_ACCESS_DENIED'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 维修人员只能更新分配给自己的工单
        if user.is_repairman() and instance.repairman != user:
            return Response(
                {'error': '无权修改此工单', 'code': 'ORDER_ACCESS_DENIED'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """部分更新工单 - 增强权限检查"""
        instance = self.get_object()
        user = request.user
        
        # 学生只能更新自己的工单
        if user.is_student() and instance.user != user:
            return Response(
                {'error': '无权修改此工单', 'code': 'ORDER_ACCESS_DENIED'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 维修人员只能更新分配给自己的工单
        if user.is_repairman() and instance.repairman != user:
            return Response(
                {'error': '无权修改此工单', 'code': 'ORDER_ACCESS_DENIED'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """删除工单 - 增强权限检查"""
        instance = self.get_object()
        user = request.user
        
        # 只有管理员可以删除工单
        if not user.is_admin():
            return Response(
                {'error': '权限不足', 'code': 'PERMISSION_DENIED'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """创建工单时自动设置当前用户"""
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """获取我的工单"""
        user = request.user
        if user.is_student():
            orders = self.get_queryset().filter(user=user)
        elif user.is_repairman():
            orders = self.get_queryset().filter(repairman=user)
        else:
            orders = self.get_queryset()
        
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """获取待处理工单（管理员）"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        orders = self.get_queryset().filter(status=0)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """获取接单池工单（维修人员）"""
        if not request.user.is_repairman():
            return Response(
                {'error': '权限不足，只有维修人员可以访问接单池'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 查询已审核通过但未分配维修人员的工单
        # status=1（已派单）且 repairman=None（未分配维修人员）
        orders = WorkOrder.objects.select_related(
            'user', 'repairman'
        ).filter(status=1, repairman__isnull=True)
        
        # 按紧急程度和提交时间排序（紧急的优先，同等紧急度按时间倒序）
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        orders = sorted(
            orders,
            key=lambda x: (priority_order.get(x.priority, 1), -x.create_time.timestamp())
        )
        
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """审核工单（管理员）"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        work_order = self.get_object()
        action_type = request.data.get('action')  # 'pass' or 'reject'
        remark = request.data.get('remark', '')
        
        # 验证工单状态
        if work_order.status != 0:
            return Response(
                {'error': '只能审核待审核状态的工单'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not action_type or action_type not in ['pass', 'reject']:
            return Response(
                {'error': '请提供有效的审核操作（pass 或 reject）'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 记录审核信息
        work_order.reviewer = request.user
        work_order.review_time = timezone.now()
        work_order.review_remark = remark
        
        if action_type == 'pass':
            # 审核通过，状态变为待派单
            work_order.status = 1
            work_order.save()
            
            # 记录审核通过日志
            OrderLog.objects.create(
                work_order=work_order,
                operator=request.user,
                action='review_pass',
                remark=remark or '审核通过'
            )
            
            message = '审核通过'
        else:
            # 审核拒绝，状态变为已取消
            if not remark:
                return Response(
                    {'error': '审核拒绝必须填写原因'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            work_order.status = 4
            work_order.save()
            
            # 记录审核拒绝日志
            OrderLog.objects.create(
                work_order=work_order,
                operator=request.user,
                action='review_reject',
                remark=remark
            )
            
            message = '审核拒绝'
        
        serializer = self.get_serializer(work_order)
        return Response({
            'message': message,
            'order': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """接单（维修人员）"""
        if not request.user.is_repairman():
            return Response(
                {'error': '权限不足，只有维修人员可以接单'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 直接查询工单，不使用 get_object()，因为 get_queryset() 会过滤掉未分配的工单
        try:
            work_order = WorkOrder.objects.get(pk=pk)
        except WorkOrder.DoesNotExist:
            return Response(
                {'error': '工单不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 验证工单状态（只能接待派单工单）
        if work_order.status != 1:
            return Response(
                {'error': '只能接取待派单状态的工单'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证工单未被接单
        if work_order.repairman is not None:
            return Response(
                {'error': '该工单已被其他维修人员接取'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 分配维修人员并记录接单时间
        work_order.repairman = request.user
        work_order.accept_time = timezone.now()
        work_order.save()
        
        # 记录接单日志
        OrderLog.objects.create(
            work_order=work_order,
            operator=request.user,
            action='accept',
            remark=f'{request.user.real_name or request.user.username} 接单'
        )
        
        serializer = self.get_serializer(work_order)
        return Response({
            'message': '接单成功',
            'order': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """派单（管理员）"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        work_order = self.get_object()
        repairman_id = request.data.get('repairman_id')
        
        if not repairman_id:
            return Response(
                {'error': '请选择维修人员'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from accounts.models import User
            repairman = User.objects.get(id=repairman_id, role=2)
        except User.DoesNotExist:
            return Response(
                {'error': '维修人员不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        work_order.repairman = repairman
        work_order.status = 1  # 已派单
        work_order.accept_time = timezone.now()  # 记录派单时间（管理员派单）
        work_order.save()
        
        # 记录派单日志
        OrderLog.objects.create(
            work_order=work_order,
            operator=request.user,
            action='assign',
            remark=f'派单给 {repairman.real_name or repairman.username}'
        )
        
        serializer = self.get_serializer(work_order)
        return Response({
            'message': '派单成功',
            'order': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def start_repair(self, request, pk=None):
        """开始维修（维修人员）"""
        work_order = self.get_object()
        user = request.user
        
        # 验证权限：只有维修人员可以开始维修
        if not user.is_repairman():
            return Response(
                {'error': '权限不足，只有维修人员可以开始维修'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 验证是否是被分配的维修人员
        if work_order.repairman != user:
            return Response(
                {'error': '只能开始分配给自己的工单'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 验证工单状态（只能开始已派单工单）
        if work_order.status != 1:
            return Response(
                {'error': '只能开始已派单状态的工单'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新状态为维修中，记录开始时间
        work_order.status = 2
        work_order.start_time = timezone.now()
        work_order.save()
        
        # 记录开始维修日志
        OrderLog.objects.create(
            work_order=work_order,
            operator=user,
            action='start',
            remark='开始维修'
        )
        
        serializer = self.get_serializer(work_order)
        return Response({
            'message': '已开始维修',
            'order': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def complete_repair(self, request, pk=None):
        """完成维修（维修人员）"""
        work_order = self.get_object()
        user = request.user
        
        # 验证权限：只有维修人员可以完成维修
        if not user.is_repairman():
            return Response(
                {'error': '权限不足，只有维修人员可以完成维修'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 验证是否是被分配的维修人员
        if work_order.repairman != user:
            return Response(
                {'error': '只能完成分配给自己的工单'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 验证工单状态（只能完成维修中工单）
        if work_order.status != 2:
            return Response(
                {'error': '只能完成维修中状态的工单'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取维修凭证数据
        repair_proof_img = request.FILES.get('repair_proof_img')
        repair_description = request.data.get('repair_description', '')
        materials = request.data.get('materials', '')
        
        # 验证至少提供照片或说明
        if not repair_proof_img and not repair_description:
            return Response(
                {'error': '请至少上传维修照片或填写维修说明'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新工单信息
        work_order.status = 3
        work_order.finish_time = timezone.now()
        if repair_proof_img:
            work_order.repair_proof_img = repair_proof_img
        if repair_description:
            work_order.repair_description = repair_description
        if materials:
            # 将耗材信息追加到备注中
            if work_order.remark:
                work_order.remark += f'\n耗材：{materials}'
            else:
                work_order.remark = f'耗材：{materials}'
        work_order.save()
        
        # 记录完成维修日志
        log_remark = repair_description or '维修完成'
        if materials:
            log_remark += f'，耗材：{materials}'
        
        OrderLog.objects.create(
            work_order=work_order,
            operator=user,
            action='complete',
            remark=log_remark
        )
        
        serializer = self.get_serializer(work_order)
        return Response({
            'message': '维修完成',
            'order': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """更新工单状态"""
        work_order = self.get_object()
        new_status = request.data.get('status')
        remark = request.data.get('remark', '')
        
        if new_status is None:
            return Response(
                {'error': '请提供新状态'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 权限检查
        user = request.user
        if user.is_student() and new_status not in [4]:  # 学生只能取消
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if user.is_repairman() and work_order.repairman != user:
            return Response(
                {'error': '只能操作分配给自己的工单'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        old_status = work_order.status
        work_order.status = new_status
        
        # 如果是完工，记录完工时间
        if new_status == 3:
            work_order.finish_time = timezone.now()
        
        if remark:
            work_order.remark = remark
        
        work_order.save()
        
        # 记录日志
        action_map = {
            0: 'submit',
            1: 'assign',
            2: 'start',
            3: 'complete',
            4: 'cancel',
        }
        action = action_map.get(new_status, 'review')
        
        OrderLog.objects.create(
            work_order=work_order,
            operator=user,
            action=action,
            remark=remark
        )
        
        serializer = self.get_serializer(work_order)
        return Response({
            'message': '状态更新成功',
            'order': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """工单统计（管理员）"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = WorkOrder.objects.all()
        
        # 统计各状态工单数
        stats = {
            'total': queryset.count(),
            'pending': queryset.filter(status=0).count(),
            'assigned': queryset.filter(status=1).count(),
            'in_progress': queryset.filter(status=2).count(),
            'completed': queryset.filter(status=3).count(),
            'cancelled': queryset.filter(status=4).count(),
        }
        
        # 计算平均响应时间（从提交到接单的时间，单位：小时）
        # 只统计已接单的工单（accept_time 不为空）
        accepted_orders = queryset.filter(accept_time__isnull=False)
        if accepted_orders.exists():
            total_hours = 0
            count = 0
            for order in accepted_orders:
                # 计算从创建到接单的时间差
                delta = order.accept_time - order.create_time
                hours = delta.total_seconds() / 3600
                # 只统计正数（防止数据异常）
                if hours >= 0:
                    total_hours += hours
                    count += 1
            stats['avg_response_time'] = round(total_hours / count, 1) if count > 0 else 0
        else:
            stats['avg_response_time'] = 0
        
        serializer = WorkOrderStatisticsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def type_distribution(self, request):
        """故障类型分布（管理员）"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        distribution = WorkOrder.objects.values(
            'category'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response(list(distribution))
    
    @action(detail=False, methods=['get'])
    def trend_data(self, request):
        """工单趋势数据（管理员）- 最近7天"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from datetime import datetime, timedelta
        
        # 获取最近7天的日期
        today = timezone.now().date()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        
        trend_data = []
        for date in dates:
            next_date = date + timedelta(days=1)
            
            # 当天提交的工单数
            submitted = WorkOrder.objects.filter(
                create_time__date=date
            ).count()
            
            # 当天完成的工单数
            completed = WorkOrder.objects.filter(
                finish_time__date=date,
                status=3
            ).count()
            
            trend_data.append({
                'date': date.strftime('%m/%d'),
                'submitted': submitted,
                'completed': completed
            })
        
        return Response(trend_data)
    
    @action(detail=False, methods=['get'])
    def repairman_performance(self, request):
        """维修员绩效数据（管理员）- 基于真实数据计算"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from accounts.models import User
        from django.db.models import Avg
        import logging
        logger = logging.getLogger(__name__)
        
        # 获取所有维修员
        repairmen = User.objects.filter(role=2)
        logger.info(f'找到 {repairmen.count()} 个维修员')
        
        performance_data = []
        for repairman in repairmen:
            orders = WorkOrder.objects.filter(repairman=repairman)
            completed_orders = orders.filter(status=3)
            total_orders = orders.count()
            
            logger.info(f'{repairman.username}: 总工单={total_orders}, 已完成={completed_orders.count()}')
            
            # 即使没有工单也显示，给默认分数
            if total_orders == 0:
                performance_data.append({
                    'name': repairman.username,
                    'response_speed': 50.0,
                    'quality': 50.0,
                    'quantity': 50.0,
                    'rating': 50.0,
                    'punctuality': 50.0
                })
                continue
            
            # 1. 响应速度：平均接单时间（小时）转换为分数（越快越高，50-100分）
            accepted_orders = orders.filter(accept_time__isnull=False)
            if accepted_orders.exists():
                total_response_hours = 0
                for order in accepted_orders:
                    delta = order.accept_time - order.create_time
                    hours = delta.total_seconds() / 3600
                    if hours >= 0:  # 只统计正数
                        total_response_hours += hours
                avg_response_hours = total_response_hours / accepted_orders.count()
                # 24小时内=100分，48小时=50分
                response_speed = max(50, min(100, 100 - (avg_response_hours / 48 * 50)))
            else:
                response_speed = 50
            
            # 2. 维修质量：基于用户评分（1-5星转换为 50-100 分）
            comments = Comment.objects.filter(work_order__repairman=repairman)
            if comments.exists():
                avg_score = comments.aggregate(Avg('score'))['score__avg']
                quality = 50 + ((avg_score / 5) * 50) if avg_score else 50
            else:
                quality = 50
            
            # 3. 工单数量：完成的工单数量（归一化到 50-100）
            # 10个工单为满分
            quantity = 50 + min(50, (completed_orders.count() / 10) * 50)
            
            # 4. 用户评分：直接使用评分转换（50-100分）
            rating = quality
            
            # 5. 准时率：在预期时间内完成的比例（50-100分）
            # 从接单到完工 48 小时内为准时
            finished_orders = completed_orders.filter(
                accept_time__isnull=False,
                finish_time__isnull=False
            )
            if finished_orders.exists():
                on_time_count = 0
                for order in finished_orders:
                    delta = order.finish_time - order.accept_time
                    if delta.total_seconds() / 3600 <= 48:
                        on_time_count += 1
                punctuality = 50 + ((on_time_count / finished_orders.count()) * 50)
            else:
                punctuality = 50
            
            performance_data.append({
                'name': repairman.username,
                'response_speed': round(response_speed, 1),
                'quality': round(quality, 1),
                'quantity': round(quantity, 1),
                'rating': round(rating, 1),
                'punctuality': round(punctuality, 1)
            })
            
            logger.info(f'{repairman.username} 绩效: 响应={response_speed:.1f}, 质量={quality:.1f}, 数量={quantity:.1f}, 评分={rating:.1f}, 准时={punctuality:.1f}')
        
        return Response(performance_data)
    
    @action(detail=False, methods=['get'])
    def heatmap_data(self, request):
        """报修时段热力图数据（管理员）"""
        if not request.user.is_admin():
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from django.db.models.functions import ExtractWeekDay, ExtractHour
        
        # 获取最近30天的数据
        thirty_days_ago = timezone.now() - timedelta(days=30)
        orders = WorkOrder.objects.filter(create_time__gte=thirty_days_ago)
        
        # 按星期和小时统计
        heatmap_data = []
        for day in range(7):  # 0=周一, 6=周日
            for hour in range(0, 24, 2):  # 每2小时一个时段
                count = orders.filter(
                    create_time__week_day=(day + 2) % 7 + 1,  # Django week_day: 1=周日
                    create_time__hour__gte=hour,
                    create_time__hour__lt=hour + 2
                ).count()
                
                heatmap_data.append([hour // 2, day, count])
        
        return Response(heatmap_data)


class CommentViewSet(viewsets.ModelViewSet):
    """评价视图集"""
    
    queryset = Comment.objects.select_related('work_order').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """学生只能看到自己工单的评价"""
        user = self.request.user
        if user.is_student():
            return self.queryset.filter(work_order__user=user)
        return self.queryset
    
    def perform_create(self, serializer):
        """创建评价时记录日志"""
        comment = serializer.save()
        
        # 记录评价日志
        OrderLog.objects.create(
            work_order=comment.work_order,
            operator=self.request.user,
            action='comment',
            remark=f'评分：{comment.score}星'
        )


def serve_db_file(request, pk):
    """从数据库读取并返回文件（用于 db/<id> 的媒体 URL）。"""
    try:
        obj = StoredFile.objects.get(pk=pk)
    except StoredFile.DoesNotExist:
        raise Http404
    return HttpResponse(obj.content, content_type=obj.content_type or 'application/octet-stream')
