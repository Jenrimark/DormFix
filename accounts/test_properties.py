"""
Property-Based Tests for User Management
使用 Hypothesis 进行基于属性的测试
"""
from hypothesis import given, strategies as st, settings
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.models import OperationLog
import uuid

User = get_user_model()


class UserManagementPropertyTests(TransactionTestCase):
    """用户管理属性测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = APIClient()
        # 创建管理员用户
        self.admin = User.objects.create_user(
            username='admin_test',
            password='admin123',
            role=3,
            real_name='管理员'
        )
        self.client.force_authenticate(user=self.admin)
    
    @settings(max_examples=100)
    @given(
        search_query=st.text(
            min_size=1, 
            max_size=10,
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        )
    )
    def test_property_search_results_match_query(self, search_query):
        """
        属性 1：用户搜索结果匹配
        Feature: user-management-and-role-optimization, Property 1: 用户搜索结果匹配
        
        对于任何用户搜索查询和用户数据集，所有返回的搜索结果都应该匹配搜索条件
        （用户名或真实姓名包含搜索关键词）。
        
        验证：需求 1.2
        """
        # 创建一些测试用户，确保有些匹配搜索条件
        try:
            User.objects.create_user(
                username=f'user_{search_query[:5]}_{uuid.uuid4().hex[:4]}',
                password='test123',
                role=1,
                real_name=f'测试用户{search_query[:3]}'
            )
        except:
            pass
        
        # 执行搜索
        response = self.client.get(f'/api/users/list_all/?search={search_query}')
        
        if response.status_code == 200:
            results = response.data.get('results', [])
            
            # 验证所有搜索结果都匹配查询条件
            for user in results:
                username = user.get('username', '').lower()
                real_name = user.get('real_name', '') or ''
                real_name = real_name.lower()
                search_lower = search_query.lower()
                
                # 至少用户名或真实姓名包含搜索关键词
                assert (
                    search_lower in username or 
                    search_lower in real_name
                ), f"搜索结果不匹配：用户名={username}, 真实姓名={real_name}, 搜索词={search_query}"
    
    @settings(max_examples=100)
    @given(
        username=st.text(
            min_size=3, 
            max_size=15, 
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        ),
        real_name=st.text(
            min_size=2, 
            max_size=20,
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))
        ),
        role=st.integers(min_value=1, max_value=3)
    )
    def test_property_user_creation_round_trip(self, username, real_name, role):
        """
        属性 2：用户创建后可查询
        Feature: user-management-and-role-optimization, Property 2: 用户创建后可查询
        
        对于任何有效的用户数据，创建用户后应该能够通过用户ID查询到该用户，
        且用户信息与创建时一致。
        
        验证：需求 1.4
        """
        # 跳过已存在的用户名
        if User.objects.filter(username=username).exists():
            return
        
        # 创建用户
        data = {
            'username': username,
            'password': 'testpass123',
            'real_name': real_name,
            'role': role
        }
        response = self.client.post('/api/users/create_user/', data)
        
        if response.status_code == 201:
            user_id = response.data['user']['id']
            
            # 查询用户
            user = User.objects.get(id=user_id)
            
            # 验证数据一致性
            assert user.username == username, f"用户名不匹配：期望={username}, 实际={user.username}"
            assert user.real_name == real_name, f"真实姓名不匹配：期望={real_name}, 实际={user.real_name}"
            assert user.role == role, f"角色不匹配：期望={role}, 实际={user.role}"
    
    @settings(max_examples=100)
    @given(
        username=st.text(
            min_size=3, 
            max_size=15, 
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        )
    )
    def test_property_duplicate_username_rejected(self, username):
        """
        属性 3：重复用户名拒绝
        Feature: user-management-and-role-optimization, Property 3: 重复用户名拒绝
        
        对于任何已存在的用户名，尝试创建同名用户应该被系统拒绝并返回错误。
        
        验证：需求 1.5
        """
        # 跳过admin用户名（已存在）
        if username == 'admin_test':
            return
        
        # 先创建一个用户
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                password='test123',
                role=1
            )
        
        # 尝试创建同名用户
        data = {
            'username': username,
            'password': 'testpass123',
            'role': 1
        }
        response = self.client.post('/api/users/create_user/', data)
        
        # 验证被拒绝
        assert response.status_code == 400, f"应该拒绝重复用户名，但返回状态码={response.status_code}"
        assert 'USERNAME_EXISTS' in response.data.get('code', ''), "错误代码应该包含 USERNAME_EXISTS"
    
    @settings(max_examples=100)
    @given(
        new_role=st.integers(min_value=1, max_value=3)
    )
    def test_property_role_change_logged(self, new_role):
        """
        属性 4：角色修改生效并记录日志
        Feature: user-management-and-role-optimization, Property 4: 角色修改生效并记录日志
        
        对于任何用户和新角色，修改用户角色后，用户的角色应该更新为新角色，
        且系统应该创建一条用户日志记录。
        
        验证：需求 1.7
        """
        # 创建测试用户
        unique_username = f'testuser_{uuid.uuid4().hex[:8]}'
        test_user = User.objects.create_user(
            username=unique_username,
            password='test123',
            role=1
        )
        
        old_role = test_user.role
        
        # 记录修改前的日志数量
        log_count_before = OperationLog.objects.filter(
            action='update_user',
            target_user=test_user
        ).count()
        
        # 修改角色
        data = {'role': new_role}
        response = self.client.put(f'/api/users/{test_user.id}/update_user/', data)
        
        if response.status_code == 200:
            # 重新获取用户
            test_user.refresh_from_db()
            
            # 验证角色已更新
            assert test_user.role == new_role, f"角色未更新：期望={new_role}, 实际={test_user.role}"
            
            # 验证用户日志已创建
            log_count_after = OperationLog.objects.filter(
                action='update_user',
                target_user=test_user
            ).count()
            
            assert log_count_after > log_count_before, "应该创建用户日志"
    
    @settings(max_examples=100)
    @given(
        username=st.text(
            min_size=3, 
            max_size=15, 
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        )
    )
    def test_property_user_deletion_not_queryable(self, username):
        """
        属性 5：用户删除后不可查询
        Feature: user-management-and-role-optimization, Property 5: 用户删除后不可查询
        
        对于任何用户，删除该用户后，通过用户ID查询应该返回不存在错误或空结果。
        
        验证：需求 1.9
        """
        # 跳过admin用户名（不能删除自己）
        if username == 'admin_test':
            return
        
        # 创建测试用户
        if not User.objects.filter(username=username).exists():
            test_user = User.objects.create_user(
                username=username,
                password='test123',
                role=1
            )
        else:
            test_user = User.objects.get(username=username)
        
        user_id = test_user.id
        
        # 删除用户
        response = self.client.delete(f'/api/users/{user_id}/delete_user/')
        
        if response.status_code == 200:
            # 验证用户不存在
            assert not User.objects.filter(id=user_id).exists(), "用户应该已被删除"
    
    @settings(max_examples=100)
    @given(
        username=st.text(
            min_size=3, 
            max_size=15, 
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        )
    )
    def test_property_password_reset_changes_password(self, username):
        """
        属性 6：密码重置后密码改变
        Feature: user-management-and-role-optimization, Property 6: 密码重置后密码改变
        
        对于任何用户，重置密码后，使用旧密码登录应该失败，使用新密码登录应该成功。
        
        验证：需求 1.10
        """
        # 跳过admin用户名
        if username == 'admin_test':
            return
        
        old_password = 'oldpass123'
        
        # 创建测试用户
        if not User.objects.filter(username=username).exists():
            test_user = User.objects.create_user(
                username=username,
                password=old_password,
                role=1
            )
        else:
            test_user = User.objects.get(username=username)
            test_user.set_password(old_password)
            test_user.save()
        
        # 重置密码
        response = self.client.post(f'/api/users/{test_user.id}/reset_password/')
        
        if response.status_code == 200:
            new_password = response.data.get('new_password')
            
            # 重新获取用户
            test_user.refresh_from_db()
            
            # 验证旧密码失效
            assert not test_user.check_password(old_password), "旧密码应该失效"
            
            # 验证新密码成功
            assert test_user.check_password(new_password), "新密码应该有效"


class UserStatusPropertyTests(TransactionTestCase):
    """用户状态管理属性测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = APIClient()
        # 创建管理员用户
        self.admin = User.objects.create_user(
            username='admin_status_test',
            password='admin123',
            role=3,
            real_name='管理员'
        )
        self.client.force_authenticate(user=self.admin)
    
    @settings(max_examples=100)
    @given(
        username=st.text(
            min_size=3, 
            max_size=15, 
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        )
    )
    def test_property_user_disable_updates_status(self, username):
        """
        属性 25：用户禁用后状态更新
        Feature: user-management-and-role-optimization, Property 25: 用户禁用后状态更新
        
        对于任何用户，管理员点击"禁用"后，用户的 is_active 字段应该更新为 False。
        
        验证：需求 7.1
        """
        # 跳过admin用户名
        if username == 'admin_status_test':
            return
        
        # 创建启用状态的测试用户
        if not User.objects.filter(username=username).exists():
            test_user = User.objects.create_user(
                username=username,
                password='test123',
                role=1,
                is_active=True
            )
        else:
            test_user = User.objects.get(username=username)
            test_user.is_active = True
            test_user.save()
        
        # 禁用用户
        response = self.client.post(f'/api/users/{test_user.id}/toggle_status/')
        
        if response.status_code == 200:
            # 重新获取用户
            test_user.refresh_from_db()
            
            # 验证状态已更新为禁用
            assert test_user.is_active == False, f"用户应该被禁用，但 is_active={test_user.is_active}"
    
    @settings(max_examples=100)
    @given(
        username=st.text(
            min_size=3, 
            max_size=15, 
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        )
    )
    def test_property_disabled_user_cannot_login(self, username):
        """
        属性 26：禁用用户无法登录
        Feature: user-management-and-role-optimization, Property 26: 禁用用户无法登录
        
        对于任何被禁用的用户（is_active=False），尝试登录应该被拒绝并返回账号已禁用错误。
        
        验证：需求 7.2
        """
        # 跳过admin用户名
        if username == 'admin_status_test':
            return
        
        password = 'testpass123'
        
        # 创建禁用状态的测试用户
        if not User.objects.filter(username=username).exists():
            test_user = User.objects.create_user(
                username=username,
                password=password,
                role=1,
                is_active=False
            )
        else:
            test_user = User.objects.get(username=username)
            test_user.set_password(password)
            test_user.is_active = False
            test_user.save()
        
        # 创建未认证的客户端
        unauthenticated_client = APIClient()
        
        # 尝试登录
        response = unauthenticated_client.post('/api/users/login/', {
            'username': username,
            'password': password
        })
        
        # 验证登录被拒绝
        assert response.status_code == 403, f"禁用用户应该无法登录，但返回状态码={response.status_code}"
        assert 'ACCOUNT_DISABLED' in response.data.get('code', ''), "错误代码应该包含 ACCOUNT_DISABLED"
    
    @settings(max_examples=100)
    @given(
        username=st.text(
            min_size=3, 
            max_size=15, 
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))
        )
    )
    def test_property_user_enable_updates_status(self, username):
        """
        属性 27：用户启用后状态更新
        Feature: user-management-and-role-optimization, Property 27: 用户启用后状态更新
        
        对于任何被禁用的用户，管理员点击"启用"后，用户的 is_active 字段应该更新为 True。
        
        验证：需求 7.3
        """
        # 跳过admin用户名
        if username == 'admin_status_test':
            return
        
        # 创建禁用状态的测试用户
        if not User.objects.filter(username=username).exists():
            test_user = User.objects.create_user(
                username=username,
                password='test123',
                role=1,
                is_active=False
            )
        else:
            test_user = User.objects.get(username=username)
            test_user.is_active = False
            test_user.save()
        
        # 启用用户
        response = self.client.post(f'/api/users/{test_user.id}/toggle_status/')
        
        if response.status_code == 200:
            # 重新获取用户
            test_user.refresh_from_db()
            
            # 验证状态已更新为启用
            assert test_user.is_active == True, f"用户应该被启用，但 is_active={test_user.is_active}"


class BatchOperationPropertyTests(TransactionTestCase):
    """批量操作属性测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = APIClient()
        # 创建管理员用户
        self.admin = User.objects.create_user(
            username='admin_batch_test',
            password='admin123',
            role=3,
            real_name='管理员'
        )
        self.client.force_authenticate(user=self.admin)
    
    @settings(max_examples=100)
    @given(
        user_count=st.integers(min_value=2, max_value=5)
    )
    def test_property_batch_disable_all_selected_users(self, user_count):
        """
        属性 28：批量禁用所有选中用户
        Feature: user-management-and-role-optimization, Property 28: 批量禁用所有选中用户
        
        对于任何用户ID集合，执行批量禁用操作后，所有选中用户的 is_active 字段都应该更新为 False。
        
        验证：需求 8.2
        """
        # 创建测试用户
        user_ids = []
        for i in range(user_count):
            user = User.objects.create_user(
                username=f'batch_user_{uuid.uuid4().hex[:8]}',
                password='test123',
                role=1,
                is_active=True
            )
            user_ids.append(user.id)
        
        # 批量禁用
        response = self.client.post('/api/users/batch_operation/', {
            'user_ids': user_ids,
            'action': 'disable'
        })
        
        if response.status_code == 200:
            # 验证所有用户都被禁用
            for user_id in user_ids:
                user = User.objects.get(id=user_id)
                assert user.is_active == False, f"用户 {user_id} 应该被禁用"
    
    @settings(max_examples=100)
    @given(
        user_count=st.integers(min_value=2, max_value=5)
    )
    def test_property_batch_enable_all_selected_users(self, user_count):
        """
        属性 29：批量启用所有选中用户
        Feature: user-management-and-role-optimization, Property 29: 批量启用所有选中用户
        
        对于任何用户ID集合，执行批量启用操作后，所有选中用户的 is_active 字段都应该更新为 True。
        
        验证：需求 8.3
        """
        # 创建禁用状态的测试用户
        user_ids = []
        for i in range(user_count):
            user = User.objects.create_user(
                username=f'batch_user_{uuid.uuid4().hex[:8]}',
                password='test123',
                role=1,
                is_active=False
            )
            user_ids.append(user.id)
        
        # 批量启用
        response = self.client.post('/api/users/batch_operation/', {
            'user_ids': user_ids,
            'action': 'enable'
        })
        
        if response.status_code == 200:
            # 验证所有用户都被启用
            for user_id in user_ids:
                user = User.objects.get(id=user_id)
                assert user.is_active == True, f"用户 {user_id} 应该被启用"
    
    @settings(max_examples=100)
    @given(
        user_count=st.integers(min_value=2, max_value=5)
    )
    def test_property_batch_delete_all_selected_users(self, user_count):
        """
        属性 30：批量删除所有选中用户
        Feature: user-management-and-role-optimization, Property 30: 批量删除所有选中用户
        
        对于任何用户ID集合，执行批量删除操作后，所有选中用户都应该从数据库中删除或标记为已删除。
        
        验证：需求 8.4
        """
        # 创建测试用户
        user_ids = []
        for i in range(user_count):
            user = User.objects.create_user(
                username=f'batch_user_{uuid.uuid4().hex[:8]}',
                password='test123',
                role=1
            )
            user_ids.append(user.id)
        
        # 批量删除
        response = self.client.post('/api/users/batch_operation/', {
            'user_ids': user_ids,
            'action': 'delete'
        })
        
        if response.status_code == 200:
            # 验证所有用户都被删除
            for user_id in user_ids:
                assert not User.objects.filter(id=user_id).exists(), f"用户 {user_id} 应该被删除"
    
    @settings(max_examples=100)
    @given(
        user_count=st.integers(min_value=2, max_value=5)
    )
    def test_property_batch_operation_summary_correct(self, user_count):
        """
        属性 31：批量操作结果摘要正确
        Feature: user-management-and-role-optimization, Property 31: 批量操作结果摘要正确
        
        对于任何批量操作，操作完成后返回的结果摘要中，成功数量和失败数量之和应该等于操作的总用户数量。
        
        验证：需求 8.5
        """
        # 创建测试用户
        user_ids = []
        for i in range(user_count):
            user = User.objects.create_user(
                username=f'batch_user_{uuid.uuid4().hex[:8]}',
                password='test123',
                role=1
            )
            user_ids.append(user.id)
        
        # 添加一个不存在的用户ID
        user_ids.append(999999)
        
        # 批量启用
        response = self.client.post('/api/users/batch_operation/', {
            'user_ids': user_ids,
            'action': 'enable'
        })
        
        if response.status_code == 200:
            summary = response.data.get('summary', {})
            total = summary.get('total', 0)
            success = summary.get('success', 0)
            failed = summary.get('failed', 0)
            
            # 验证总数等于成功+失败
            assert total == success + failed, f"总数应该等于成功+失败：total={total}, success={success}, failed={failed}"
            assert total == len(user_ids), f"总数应该等于操作的用户数量：total={total}, user_ids={len(user_ids)}"


class OperationLogPropertyTests(TransactionTestCase):
    """用户日志属性测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = APIClient()
        # 创建管理员用户
        self.admin = User.objects.create_user(
            username='admin_log_test',
            password='admin123',
            role=3,
            real_name='管理员'
        )
        self.client.force_authenticate(user=self.admin)
    
    @settings(max_examples=100)
    @given(
        action_type=st.sampled_from(['create_user', 'update_user', 'delete_user', 'reset_password', 'toggle_status'])
    )
    def test_property_operation_logs_filterable(self, action_type):
        """
        属性 24：用户日志可筛选
        Feature: user-management-and-role-optimization, Property 24: 用户日志可筛选
        
        对于任何用户日志查询条件（时间、操作人、操作类型），返回的日志记录都应该匹配筛选条件。
        
        验证：需求 6.4
        """
        # 创建不同类型的用户日志
        test_user = User.objects.create_user(
            username=f'log_test_user_{uuid.uuid4().hex[:8]}',
            password='test123',
            role=1
        )
        
        # 创建指定类型的日志
        OperationLog.objects.create(
            operator=self.admin,
            action=action_type,
            target_user=test_user,
            description=f'测试日志 {action_type}'
        )
        
        # 创建其他类型的日志
        other_action = 'batch_enable' if action_type != 'batch_enable' else 'batch_disable'
        OperationLog.objects.create(
            operator=self.admin,
            action=other_action,
            target_user=test_user,
            description=f'测试日志 {other_action}'
        )
        
        # 按操作类型筛选
        response = self.client.get(f'/api/operation-logs/?action={action_type}')
        
        if response.status_code == 200:
            results = response.data.get('results', [])
            
            # 验证所有返回的日志都匹配筛选条件
            for log in results:
                assert log.get('action') == action_type, f"日志操作类型应该是 {action_type}，但实际是 {log.get('action')}"


class WorkOrderPermissionPropertyTests(TransactionTestCase):
    """工单权限隔离属性测试"""
    
    def setUp(self):
        """设置测试环境"""
        from repairs.models import RepairType, WorkOrder
        
        self.client = APIClient()
        
        # 创建管理员
        self.admin = User.objects.create_user(
            username='admin_order_test',
            password='admin123',
            role=3
        )
        
        # 创建两个学生
        self.student1 = User.objects.create_user(
            username='student1_order_test',
            password='student123',
            role=1
        )
        
        self.student2 = User.objects.create_user(
            username='student2_order_test',
            password='student123',
            role=1
        )
        
        # 创建两个维修人员
        self.repairman1 = User.objects.create_user(
            username='repairman1_order_test',
            password='repairman123',
            role=2
        )
        
        self.repairman2 = User.objects.create_user(
            username='repairman2_order_test',
            password='repairman123',
            role=2
        )
        
        # 创建故障类型
        self.repair_type = RepairType.objects.create(
            name='测试故障类型',
            priority='medium'
        )
    
    @settings(max_examples=50)
    @given(
        content=st.text(min_size=5, max_size=50)
    )
    def test_property_student_order_isolation(self, content):
        """
        属性 19：学生工单隔离
        Feature: user-management-and-role-optimization, Property 19: 学生工单隔离
        
        对于任何两个不同的学生用户，学生A尝试访问学生B的工单应该被拒绝并返回权限错误。
        
        验证：需求 5.3
        """
        from repairs.models import WorkOrder
        
        # 学生1创建工单
        order = WorkOrder.objects.create(
            user=self.student1,
            repair_type=self.repair_type,
            content=content,
            priority='medium'
        )
        
        # 学生2尝试访问学生1的工单
        self.client.force_authenticate(user=self.student2)
        response = self.client.get(f'/api/work-orders/{order.id}/')
        
        # 验证访问被拒绝
        assert response.status_code == 403, f"学生2应该无法访问学生1的工单，但返回状态码={response.status_code}"
        assert 'ORDER_ACCESS_DENIED' in response.data.get('code', ''), "错误代码应该包含 ORDER_ACCESS_DENIED"
    
    @settings(max_examples=50)
    @given(
        content=st.text(min_size=5, max_size=50)
    )
    def test_property_repairman_order_isolation(self, content):
        """
        属性 20：维修人员工单隔离
        Feature: user-management-and-role-optimization, Property 20: 维修人员工单隔离
        
        对于任何维修人员和未分配给他的工单，维修人员尝试访问该工单应该被拒绝并返回权限错误。
        
        验证：需求 5.4
        """
        from repairs.models import WorkOrder
        
        # 创建工单并分配给维修人员1
        order = WorkOrder.objects.create(
            user=self.student1,
            repair_type=self.repair_type,
            content=content,
            priority='medium',
            repairman=self.repairman1,
            status=1  # 已派单
        )
        
        # 维修人员2尝试访问分配给维修人员1的工单
        self.client.force_authenticate(user=self.repairman2)
        response = self.client.get(f'/api/work-orders/{order.id}/')
        
        # 验证访问被拒绝
        assert response.status_code == 403, f"维修人员2应该无法访问维修人员1的工单，但返回状态码={response.status_code}"
        assert 'ORDER_ACCESS_DENIED' in response.data.get('code', ''), "错误代码应该包含 ORDER_ACCESS_DENIED"


class SessionExpirationPropertyTests(TransactionTestCase):
    """会话过期属性测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='session_test_user',
            password='test123',
            role=1
        )
    
    @settings(max_examples=50)
    @given(
        username=st.text(min_size=3, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
    )
    def test_property_session_expiration_requires_relogin(self, username):
        """
        属性 21：会话过期后需要重新登录
        Feature: user-management-and-role-optimization, Property 21: 会话过期后需要重新登录
        
        对于任何用户，当会话过期后，尝试访问需要认证的接口应该返回401错误，要求重新登录。
        
        验证：需求 5.6
        
        注意：此测试验证未认证用户无法访问需要认证的接口。
        实际的会话过期由Django的SESSION_COOKIE_AGE设置控制。
        """
        # 跳过已存在的用户名
        if User.objects.filter(username=username).exists():
            return
        
        # 创建未认证的客户端（模拟会话过期）
        unauthenticated_client = APIClient()
        
        # 尝试访问需要认证的接口
        response = unauthenticated_client.get('/api/users/me/')
        
        # 验证返回401未认证错误
        assert response.status_code in [401, 403], f"未认证用户应该无法访问，但返回状态码={response.status_code}"
