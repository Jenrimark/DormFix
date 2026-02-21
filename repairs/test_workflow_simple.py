"""
简单的报修流程测试
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import WorkOrder, RepairType, OrderLog

User = get_user_model()


class SimpleWorkflowTestCase(TestCase):
    """简单的报修流程测试"""
    
    def setUp(self):
        """设置测试数据"""
        # 创建测试用户
        self.student = User.objects.create_user(
            username='student',
            password='pass123',
            role=1,
            real_name='测试学生'
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            password='pass123',
            role=3,
            real_name='测试管理员'
        )
        
        self.repairman = User.objects.create_user(
            username='repairman',
            password='pass123',
            role=2,
            real_name='测试维修工'
        )
        
        # 创建故障类型
        self.repair_type = RepairType.objects.create(
            name='水电类',
            priority='high'
        )
    
    def test_model_fields(self):
        """测试模型新字段"""
        # 创建工单
        order = WorkOrder.objects.create(
            user=self.student,
            repair_type=self.repair_type,
            priority='high',
            content='水龙头漏水',
            status=0
        )
        
        # 测试审核字段
        order.reviewer = self.admin
        order.review_time = timezone.now()
        order.review_remark = '审核通过'
        order.status = 1
        order.save()
        
        order.refresh_from_db()
        self.assertEqual(order.reviewer, self.admin)
        self.assertIsNotNone(order.review_time)
        self.assertEqual(order.review_remark, '审核通过')
        
        # 测试接单字段
        order.repairman = self.repairman
        order.accept_time = timezone.now()
        order.save()
        
        order.refresh_from_db()
        self.assertEqual(order.repairman, self.repairman)
        self.assertIsNotNone(order.accept_time)
        
        # 测试维修字段
        order.start_time = timezone.now()
        order.status = 2
        order.save()
        
        order.refresh_from_db()
        self.assertIsNotNone(order.start_time)
        self.assertEqual(order.status, 2)
        
        # 测试完成字段
        order.finish_time = timezone.now()
        order.repair_description = '已更换水龙头'
        order.status = 3
        order.save()
        
        order.refresh_from_db()
        self.assertIsNotNone(order.finish_time)
        self.assertEqual(order.repair_description, '已更换水龙头')
        self.assertEqual(order.status, 3)
    
    def test_order_log_actions(self):
        """测试日志动作类型"""
        order = WorkOrder.objects.create(
            user=self.student,
            repair_type=self.repair_type,
            priority='high',
            content='测试工单',
            status=0
        )
        
        # 测试新的日志动作类型
        actions = ['submit', 'review_pass', 'review_reject', 'accept', 'start', 'complete']
        
        for action in actions:
            log = OrderLog.objects.create(
                work_order=order,
                operator=self.admin,
                action=action,
                remark=f'测试{action}'
            )
            self.assertEqual(log.action, action)
            self.assertIsNotNone(log.get_action_display())
    
    def test_workflow_logic(self):
        """测试工单流程逻辑"""
        # 1. 创建工单（待审核）
        order = WorkOrder.objects.create(
            user=self.student,
            repair_type=self.repair_type,
            priority='high',
            content='水龙头漏水',
            status=0
        )
        self.assertEqual(order.status, 0)
        
        # 2. 审核通过（待派单）
        order.reviewer = self.admin
        order.review_time = timezone.now()
        order.status = 1
        order.save()
        
        OrderLog.objects.create(
            work_order=order,
            operator=self.admin,
            action='review_pass',
            remark='审核通过'
        )
        
        # 3. 接单（已派单）
        order.repairman = self.repairman
        order.accept_time = timezone.now()
        order.save()
        
        OrderLog.objects.create(
            work_order=order,
            operator=self.repairman,
            action='accept',
            remark='接单'
        )
        
        # 4. 开始维修（维修中）
        order.start_time = timezone.now()
        order.status = 2
        order.save()
        
        OrderLog.objects.create(
            work_order=order,
            operator=self.repairman,
            action='start',
            remark='开始维修'
        )
        
        # 5. 完成维修（已完成）
        order.finish_time = timezone.now()
        order.repair_description = '已更换水龙头'
        order.status = 3
        order.save()
        
        OrderLog.objects.create(
            work_order=order,
            operator=self.repairman,
            action='complete',
            remark='维修完成'
        )
        
        # 验证最终状态
        order.refresh_from_db()
        self.assertEqual(order.status, 3)
        self.assertEqual(order.reviewer, self.admin)
        self.assertEqual(order.repairman, self.repairman)
        self.assertIsNotNone(order.review_time)
        self.assertIsNotNone(order.accept_time)
        self.assertIsNotNone(order.start_time)
        self.assertIsNotNone(order.finish_time)
        self.assertEqual(order.repair_description, '已更换水龙头')
        
        # 验证日志记录
        logs = OrderLog.objects.filter(work_order=order).order_by('create_time')
        self.assertEqual(logs.count(), 4)
        
        actions = [log.action for log in logs]
        self.assertEqual(actions, ['review_pass', 'accept', 'start', 'complete'])
