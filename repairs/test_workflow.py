"""
报修流程测试
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import WorkOrder, RepairType, OrderLog

User = get_user_model()


class WorkflowTestCase(TestCase):
    """报修流程测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.client = APIClient()
        
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
    
    def test_complete_workflow(self):
        """测试完整工单流程"""
        
        # 1. 学生提交工单
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/repairs/work-orders/', {
            'repair_type': self.repair_type.id,
            'priority': 'high',
            'content': '水龙头漏水'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 获取创建的工单
        order = WorkOrder.objects.filter(user=self.student).first()
        self.assertIsNotNone(order)
        order_id = order.id
        
        # 验证工单状态为待审核
        order = WorkOrder.objects.get(id=order_id)
        self.assertEqual(order.status, 0)
        
        # 2. 管理员审核通过
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/review/', {
            'action': 'pass',
            'remark': '审核通过'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证工单状态为待派单
        order.refresh_from_db()
        self.assertEqual(order.status, 1)
        self.assertEqual(order.reviewer, self.admin)
        self.assertIsNotNone(order.review_time)
        
        # 3. 维修人员接单
        self.client.force_authenticate(user=self.repairman)
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/accept/', format='json')
        print(f"Accept response: {response.status_code}, {response.data if hasattr(response, 'data') else response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证工单已分配维修人员
        order.refresh_from_db()
        self.assertEqual(order.repairman, self.repairman)
        self.assertIsNotNone(order.accept_time)
        
        # 4. 维修人员开始维修
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/start_repair/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证工单状态为维修中
        order.refresh_from_db()
        self.assertEqual(order.status, 2)
        self.assertIsNotNone(order.start_time)
        
        # 5. 维修人员完成维修
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/complete_repair/', {
            'repair_description': '已更换水龙头',
            'materials': '水龙头 x1'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证工单状态为已完成
        order.refresh_from_db()
        self.assertEqual(order.status, 3)
        self.assertIsNotNone(order.finish_time)
        self.assertEqual(order.repair_description, '已更换水龙头')
        
        # 验证日志记录
        logs = OrderLog.objects.filter(work_order=order).order_by('create_time')
        self.assertEqual(logs.count(), 5)  # 提交、审核通过、接单、开始维修、完成
        
        actions = [log.action for log in logs]
        self.assertEqual(actions, ['submit', 'review_pass', 'accept', 'start', 'complete'])
    
    def test_review_reject(self):
        """测试审核拒绝流程"""
        
        # 学生提交工单
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/repairs/work-orders/', {
            'repair_type': self.repair_type.id,
            'priority': 'low',
            'content': '测试工单'
        })
        
        # 获取创建的工单
        order = WorkOrder.objects.filter(user=self.student).first()
        order_id = order.id
        
        # 管理员审核拒绝
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/review/', {
            'action': 'reject',
            'remark': '信息不完整'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证工单状态为已取消
        order = WorkOrder.objects.get(id=order_id)
        self.assertEqual(order.status, 4)
        self.assertEqual(order.review_remark, '信息不完整')
    
    def test_available_orders(self):
        """测试接单池"""
        
        # 创建多个工单并审核通过
        self.client.force_authenticate(user=self.student)
        for i in range(3):
            response = self.client.post('/api/repairs/work-orders/', {
                'repair_type': self.repair_type.id,
                'priority': 'medium',
                'content': f'测试工单{i}'
            })
            
            # 获取创建的工单
            order = WorkOrder.objects.filter(content=f'测试工单{i}').first()
            order_id = order.id
            
            # 管理员审核通过
            self.client.force_authenticate(user=self.admin)
            self.client.post(f'/api/repairs/work-orders/{order_id}/review/', {
                'action': 'pass'
            })
            self.client.force_authenticate(user=self.student)
        
        # 维修人员查看接单池
        self.client.force_authenticate(user=self.repairman)
        response = self.client.get('/api/repairs/work-orders/available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_permissions(self):
        """测试权限控制"""
        
        # 学生提交工单
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/repairs/work-orders/', {
            'repair_type': self.repair_type.id,
            'priority': 'high',
            'content': '测试工单'
        })
        
        # 获取创建的工单
        order = WorkOrder.objects.filter(user=self.student).first()
        order_id = order.id
        
        # 学生尝试审核（应该失败）
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/review/', {
            'action': 'pass'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # 学生尝试接单（应该失败）
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/accept/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # 维修人员尝试审核（应该失败）
        self.client.force_authenticate(user=self.repairman)
        response = self.client.post(f'/api/repairs/work-orders/{order_id}/review/', {
            'action': 'pass'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
