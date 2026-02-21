from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import OperationLog
from repairs.models import WorkOrder, RepairType

User = get_user_model()


class OperationLogModelTestCase(TestCase):
    """用户日志模型单元测试"""
    
    def setUp(self):
        """设置测试数据"""
        # 创建测试用户
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            role=3,
            real_name='管理员'
        )
        
        self.student = User.objects.create_user(
            username='student',
            password='student123',
            role=1,
            real_name='学生'
        )
        
        self.repairman = User.objects.create_user(
            username='repairman',
            password='repairman123',
            role=2,
            real_name='维修人员'
        )
        
        # 创建测试工单（用于测试工单相关日志）
        self.repair_type = RepairType.objects.create(
            name='水电类',
            priority='high'
        )
        
        self.work_order = WorkOrder.objects.create(
            user=self.student,
            repair_type=self.repair_type,
            content='水龙头漏水',
            priority='high'
        )
    
    def test_create_user_operation_log(self):
        """测试创建用户用户日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student,
            description='创建学生账号',
            ip_address='127.0.0.1'
        )
        
        self.assertEqual(log.operator, self.admin)
        self.assertEqual(log.action, 'create_user')
        self.assertEqual(log.target_user, self.student)
        self.assertEqual(log.description, '创建学生账号')
        self.assertEqual(log.ip_address, '127.0.0.1')
        self.assertIsNotNone(log.created_at)
    
    def test_update_user_operation_log(self):
        """测试更新用户用户日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='update_user',
            target_user=self.repairman,
            description='修改维修人员角色'
        )
        
        self.assertEqual(log.action, 'update_user')
        self.assertEqual(log.target_user, self.repairman)
    
    def test_delete_user_operation_log(self):
        """测试删除用户用户日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='delete_user',
            target_user=self.student,
            description='删除学生账号'
        )
        
        self.assertEqual(log.action, 'delete_user')
        self.assertEqual(log.get_action_display(), '删除用户')
    
    def test_reset_password_operation_log(self):
        """测试重置密码用户日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='reset_password',
            target_user=self.student,
            description='重置学生密码'
        )
        
        self.assertEqual(log.action, 'reset_password')
        self.assertEqual(log.get_action_display(), '重置密码')
    
    def test_toggle_status_operation_log(self):
        """测试切换状态用户日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='toggle_status',
            target_user=self.student,
            description='禁用学生账号'
        )
        
        self.assertEqual(log.action, 'toggle_status')
        self.assertEqual(log.get_action_display(), '切换状态')
    
    def test_assign_order_operation_log(self):
        """测试派单用户日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='assign_order',
            target_order=self.work_order,
            description=f'将工单派给维修人员 {self.repairman.real_name}'
        )
        
        self.assertEqual(log.action, 'assign_order')
        self.assertEqual(log.target_order, self.work_order)
        self.assertIsNone(log.target_user)
    
    def test_batch_operation_logs(self):
        """测试批量用户日志"""
        # 批量启用
        log1 = OperationLog.objects.create(
            operator=self.admin,
            action='batch_enable',
            description='批量启用3个用户'
        )
        
        # 批量禁用
        log2 = OperationLog.objects.create(
            operator=self.admin,
            action='batch_disable',
            description='批量禁用2个用户'
        )
        
        # 批量删除
        log3 = OperationLog.objects.create(
            operator=self.admin,
            action='batch_delete',
            description='批量删除5个用户'
        )
        
        self.assertEqual(log1.get_action_display(), '批量启用')
        self.assertEqual(log2.get_action_display(), '批量禁用')
        self.assertEqual(log3.get_action_display(), '批量删除')
    
    def test_query_logs_by_operator(self):
        """测试按操作人查询日志"""
        # 创建多条日志
        OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student
        )
        
        OperationLog.objects.create(
            operator=self.admin,
            action='update_user',
            target_user=self.repairman
        )
        
        # 查询管理员的用户日志
        admin_logs = OperationLog.objects.filter(operator=self.admin)
        self.assertEqual(admin_logs.count(), 2)
    
    def test_query_logs_by_action(self):
        """测试按操作类型查询日志"""
        # 创建不同类型的日志
        OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student
        )
        
        OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.repairman
        )
        
        OperationLog.objects.create(
            operator=self.admin,
            action='delete_user',
            target_user=self.student
        )
        
        # 查询创建用户的日志
        create_logs = OperationLog.objects.filter(action='create_user')
        self.assertEqual(create_logs.count(), 2)
        
        # 查询删除用户的日志
        delete_logs = OperationLog.objects.filter(action='delete_user')
        self.assertEqual(delete_logs.count(), 1)
    
    def test_log_ordering(self):
        """测试日志按时间倒序排列"""
        log1 = OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student
        )
        
        log2 = OperationLog.objects.create(
            operator=self.admin,
            action='update_user',
            target_user=self.student
        )
        
        log3 = OperationLog.objects.create(
            operator=self.admin,
            action='delete_user',
            target_user=self.student
        )
        
        # 获取所有日志
        logs = list(OperationLog.objects.all())
        
        # 验证按创建时间倒序排列
        self.assertEqual(logs[0].id, log3.id)
        self.assertEqual(logs[1].id, log2.id)
        self.assertEqual(logs[2].id, log1.id)
    
    def test_log_without_target_user(self):
        """测试不需要目标用户的日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='assign_order',
            target_order=self.work_order,
            description='派单操作'
        )
        
        self.assertIsNone(log.target_user)
        self.assertIsNotNone(log.target_order)
    
    def test_log_without_target_order(self):
        """测试不需要目标工单的日志"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student,
            description='创建用户'
        )
        
        self.assertIsNotNone(log.target_user)
        self.assertIsNone(log.target_order)
    
    def test_log_str_representation(self):
        """测试日志的字符串表示"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student
        )
        
        str_repr = str(log)
        self.assertIn(str(self.admin), str_repr)
        self.assertIn('创建用户', str_repr)
    
    def test_operator_deletion_sets_null(self):
        """测试删除操作人后日志保留但操作人为空"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student
        )
        
        # 删除操作人
        admin_id = self.admin.id
        self.admin.delete()
        
        # 重新获取日志
        log.refresh_from_db()
        
        # 验证日志仍然存在但操作人为空
        self.assertIsNone(log.operator)
        self.assertEqual(log.target_user, self.student)
    
    def test_target_user_deletion_sets_null(self):
        """测试删除目标用户后日志保留但目标用户为空"""
        log = OperationLog.objects.create(
            operator=self.admin,
            action='delete_user',
            target_user=self.student
        )
        
        # 删除目标用户
        self.student.delete()
        
        # 重新获取日志
        log.refresh_from_db()
        
        # 验证日志仍然存在但目标用户为空
        self.assertIsNone(log.target_user)
        self.assertEqual(log.operator, self.admin)
    
    def test_ip_address_field_validation(self):
        """测试IP地址字段验证"""
        # IPv4地址
        log1 = OperationLog.objects.create(
            operator=self.admin,
            action='create_user',
            target_user=self.student,
            ip_address='192.168.1.1'
        )
        self.assertEqual(log1.ip_address, '192.168.1.1')
        
        # IPv6地址
        log2 = OperationLog.objects.create(
            operator=self.admin,
            action='update_user',
            target_user=self.student,
            ip_address='2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        )
        self.assertEqual(log2.ip_address, '2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        
        # 空IP地址
        log3 = OperationLog.objects.create(
            operator=self.admin,
            action='delete_user',
            target_user=self.student
        )
        self.assertIsNone(log3.ip_address)


class UserIsActiveFieldTestCase(TestCase):
    """用户is_active字段单元测试"""
    
    def test_user_is_active_default_true(self):
        """测试用户创建时is_active默认为True"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role=1
        )
        
        self.assertTrue(user.is_active)
    
    def test_user_can_be_disabled(self):
        """测试用户可以被禁用"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role=1
        )
        
        user.is_active = False
        user.save()
        
        user.refresh_from_db()
        self.assertFalse(user.is_active)
    
    def test_user_can_be_enabled(self):
        """测试用户可以被启用"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role=1,
            is_active=False
        )
        
        user.is_active = True
        user.save()
        
        user.refresh_from_db()
        self.assertTrue(user.is_active)
    
    def test_can_login_method(self):
        """测试can_login方法"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role=1
        )
        
        # 启用状态且已认证
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.can_login())
        
        # 禁用状态
        user.is_active = False
        user.save()
        self.assertFalse(user.can_login())
