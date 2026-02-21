from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import User, OperationLog
from .serializers import (
    UserSerializer, UserRegisterSerializer, 
    UserLoginSerializer, ChangePasswordSerializer,
    UserProfileUpdateSerializer, OperationLogSerializer
)
import secrets
import string


class IsAdmin(BasePermission):
    """管理员权限"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin()


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """根据不同的 action 设置不同的权限"""
        if self.action in ['register', 'login']:
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """用户注册"""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '注册成功',
                'user': UserSerializer(user, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """用户登录"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # 检查账号状态
            if not user.is_active:
                return Response(
                    {'error': '账号已被禁用，请联系管理员', 'code': 'ACCOUNT_DISABLED'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            login(request, user)
            return Response({
                'message': '登录成功',
                'user': UserSerializer(user, context={'request': request}).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """用户登出"""
        logout(request)
        return Response({'message': '登出成功'})
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def change_password(self, request):
        """修改密码"""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # 验证旧密码
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'error': '旧密码错误'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 设置新密码
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': '密码修改成功'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """更新个人信息（只能更新部分字段）"""
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # 返回完整的用户信息，包含 avatar_url
            user_serializer = UserSerializer(user, context={'request': request})
            return Response({
                'message': '信息更新成功',
                'user': user_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def upload_avatar(self, request):
        """上传头像"""
        user = request.user
        avatar = request.FILES.get('avatar')
        
        if not avatar:
            return Response(
                {'error': '请选择头像文件'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证文件类型
        if not avatar.content_type.startswith('image/'):
            return Response(
                {'error': '只能上传图片文件'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证文件大小（5MB）
        if avatar.size > 5 * 1024 * 1024:
            return Response(
                {'error': '图片大小不能超过 5MB'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.avatar = avatar
        user.save()
        
        # 使用 UserSerializer 并传入 request context
        serializer = UserSerializer(user, context={'request': request})
        
        return Response({
            'message': '头像上传成功',
            'user': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def list_all(self, request):
        """管理员获取所有用户列表（支持搜索和角色筛选）"""
        queryset = User.objects.all()
        
        # 搜索功能：按用户名、真实姓名搜索
        search = request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | 
                Q(real_name__icontains=search)
            )
        
        # 角色筛选
        role = request.query_params.get('role', '').strip()
        if role:
            try:
                role_int = int(role)
                if role_int in [1, 2, 3]:
                    queryset = queryset.filter(role=role_int)
            except ValueError:
                pass
        
        # 状态筛选
        is_active = request.query_params.get('is_active', '').strip()
        if is_active:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() == 'false':
                queryset = queryset.filter(is_active=False)
        
        # 排序
        queryset = queryset.order_by('-created_at')
        
        # 序列化
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def create_user(self, request):
        """管理员创建用户"""
        # 验证用户名唯一性
        username = request.data.get('username', '').strip()
        if not username:
            return Response(
                {'error': '用户名不能为空', 'code': 'USERNAME_REQUIRED'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': '用户名已存在', 'code': 'USERNAME_EXISTS', 'field': 'username'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建用户
        password = request.data.get('password', 'password123')  # 默认密码
        role = request.data.get('role', 1)
        real_name = request.data.get('real_name', '')
        phone = request.data.get('phone', '')
        email = request.data.get('email', '')
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                role=role,
                real_name=real_name,
                phone=phone,
                email=email
            )
            
            # 记录用户日志
            OperationLog.objects.create(
                operator=request.user,
                action='create_user',
                target_user=user,
                description=f'创建用户 {username}',
                ip_address=self._get_client_ip(request)
            )
            
            return Response({
                'message': '用户创建成功',
                'user': UserSerializer(user, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['put'], permission_classes=[IsAdmin])
    def update_user(self, request, pk=None):
        """管理员更新用户信息"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在', 'code': 'USER_NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 不能操作自己
        if user.id == request.user.id:
            return Response(
                {'error': '无法修改当前登录的账号', 'code': 'CANNOT_MODIFY_SELF'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 如果目标用户是管理员，只有超级管理员（admin）可以操作
        if user.role == 3 and request.user.username != 'admin':
            return Response(
                {'error': '只有超级管理员可以管理其他管理员账号', 'code': 'INSUFFICIENT_PERMISSION'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 更新字段
        old_role = user.role
        
        if 'real_name' in request.data:
            user.real_name = request.data['real_name']
        if 'phone' in request.data:
            user.phone = request.data['phone']
        if 'email' in request.data:
            user.email = request.data['email']
        if 'role' in request.data:
            user.role = request.data['role']
        
        user.save()
        
        # 记录用户日志
        description = f'更新用户 {user.username}'
        if old_role != user.role:
            description += f'，角色从 {old_role} 修改为 {user.role}'
        
        OperationLog.objects.create(
            operator=request.user,
            action='update_user',
            target_user=user,
            description=description,
            ip_address=self._get_client_ip(request)
        )
        
        return Response({
            'message': '用户信息更新成功',
            'user': UserSerializer(user, context={'request': request}).data
        })
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAdmin])
    def delete_user(self, request, pk=None):
        """管理员删除用户"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在', 'code': 'USER_NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 防止删除自己
        if user.id == request.user.id:
            return Response(
                {'error': '无法删除当前登录的管理员账号', 'code': 'CANNOT_DELETE_SELF'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 如果目标用户是管理员，只有超级管理员（admin）可以操作
        if user.role == 3 and request.user.username != 'admin':
            return Response(
                {'error': '只有超级管理员可以删除其他管理员账号', 'code': 'INSUFFICIENT_PERMISSION'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        username = user.username
        
        # 记录用户日志（在删除前）
        OperationLog.objects.create(
            operator=request.user,
            action='delete_user',
            target_user=None,  # 用户即将被删除，不关联
            description=f'删除用户 {username}',
            ip_address=self._get_client_ip(request)
        )
        
        # 删除用户
        user.delete()
        
        return Response({
            'message': '用户删除成功'
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reset_password(self, request, pk=None):
        """管理员重置用户密码"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在', 'code': 'USER_NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 不能操作自己
        if user.id == request.user.id:
            return Response(
                {'error': '无法重置当前登录账号的密码', 'code': 'CANNOT_RESET_SELF'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 如果目标用户是管理员，只有超级管理员（admin）可以操作
        if user.role == 3 and request.user.username != 'admin':
            return Response(
                {'error': '只有超级管理员可以重置其他管理员的密码', 'code': 'INSUFFICIENT_PERMISSION'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 生成随机密码（8位，包含字母和数字）
        new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        
        # 设置新密码
        user.set_password(new_password)
        user.save()
        
        # 记录用户日志
        OperationLog.objects.create(
            operator=request.user,
            action='reset_password',
            target_user=user,
            description=f'重置用户 {user.username} 的密码',
            ip_address=self._get_client_ip(request)
        )
        
        return Response({
            'message': '密码重置成功',
            'new_password': new_password
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def toggle_status(self, request, pk=None):
        """管理员启用/禁用用户"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在', 'code': 'USER_NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 不能操作自己
        if user.id == request.user.id:
            return Response(
                {'error': '无法修改当前登录账号的状态', 'code': 'CANNOT_MODIFY_SELF'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 如果目标用户是管理员，只有超级管理员（admin）可以操作
        if user.role == 3 and request.user.username != 'admin':
            return Response(
                {'error': '只有超级管理员可以修改其他管理员的状态', 'code': 'INSUFFICIENT_PERMISSION'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 切换状态
        user.is_active = not user.is_active
        user.save()
        
        # 记录用户日志
        action_desc = '启用' if user.is_active else '禁用'
        OperationLog.objects.create(
            operator=request.user,
            action='toggle_status',
            target_user=user,
            description=f'{action_desc}用户 {user.username}',
            ip_address=self._get_client_ip(request)
        )
        
        return Response({
            'message': f'用户已{action_desc}',
            'user': UserSerializer(user, context={'request': request}).data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def batch_operation(self, request):
        """管理员批量操作用户"""
        user_ids = request.data.get('user_ids', [])
        operation = request.data.get('action', '')  # 'enable', 'disable', 'delete'
        
        if not user_ids:
            return Response(
                {'error': '请选择要操作的用户', 'code': 'NO_USERS_SELECTED'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if operation not in ['enable', 'disable', 'delete']:
            return Response(
                {'error': '无效的操作类型', 'code': 'INVALID_OPERATION'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 统计结果
        success_count = 0
        failed_count = 0
        failed_items = []
        
        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
                
                # 防止操作自己
                if user.id == request.user.id:
                    failed_count += 1
                    failed_items.append({
                        'user_id': user_id,
                        'error': '无法操作当前登录的管理员账号'
                    })
                    continue
                
                # 如果目标用户是管理员，只有超级管理员（admin）可以操作
                if user.role == 3 and request.user.username != 'admin':
                    failed_count += 1
                    failed_items.append({
                        'user_id': user_id,
                        'error': '只有超级管理员可以操作其他管理员账号'
                    })
                    continue
                
                if operation == 'enable':
                    user.is_active = True
                    user.save()
                    action_type = 'batch_enable'
                    action_desc = '批量启用'
                elif operation == 'disable':
                    user.is_active = False
                    user.save()
                    action_type = 'batch_disable'
                    action_desc = '批量禁用'
                elif operation == 'delete':
                    username = user.username
                    user.delete()
                    action_type = 'batch_delete'
                    action_desc = '批量删除'
                    # 记录删除日志（用户已删除，不关联target_user）
                    OperationLog.objects.create(
                        operator=request.user,
                        action=action_type,
                        target_user=None,
                        description=f'{action_desc}用户 {username}',
                        ip_address=self._get_client_ip(request)
                    )
                    success_count += 1
                    continue
                
                # 记录用户日志（非删除操作）
                OperationLog.objects.create(
                    operator=request.user,
                    action=action_type,
                    target_user=user,
                    description=f'{action_desc}用户 {user.username}',
                    ip_address=self._get_client_ip(request)
                )
                
                success_count += 1
                
            except User.DoesNotExist:
                failed_count += 1
                failed_items.append({
                    'user_id': user_id,
                    'error': '用户不存在'
                })
            except Exception as e:
                failed_count += 1
                failed_items.append({
                    'user_id': user_id,
                    'error': str(e)
                })
        
        # 返回操作结果摘要
        return Response({
            'success': True,
            'message': '批量操作完成',
            'summary': {
                'total': len(user_ids),
                'success': success_count,
                'failed': failed_count
            },
            'failed_items': failed_items
        })
    
    def _get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip



class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """用户日志视图集（只读）"""
    
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        """获取用户日志列表，支持筛选"""
        queryset = OperationLog.objects.all()
        
        # 按操作人筛选
        operator_id = self.request.query_params.get('operator_id', '').strip()
        if operator_id:
            try:
                queryset = queryset.filter(operator_id=int(operator_id))
            except ValueError:
                pass
        
        # 按操作类型筛选
        action = self.request.query_params.get('action', '').strip()
        if action:
            queryset = queryset.filter(action=action)
        
        # 按时间范围筛选
        start_date = self.request.query_params.get('start_date', '').strip()
        end_date = self.request.query_params.get('end_date', '').strip()
        
        if start_date:
            try:
                from datetime import datetime
                start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(created_at__gte=start_datetime)
            except ValueError:
                pass
        
        if end_date:
            try:
                from datetime import datetime, timedelta
                end_datetime = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                queryset = queryset.filter(created_at__lt=end_datetime)
            except ValueError:
                pass
        
        # 按目标用户筛选
        target_user_id = self.request.query_params.get('target_user_id', '').strip()
        if target_user_id:
            try:
                queryset = queryset.filter(target_user_id=int(target_user_id))
            except ValueError:
                pass
        
        # 排序
        queryset = queryset.order_by('-created_at')
        
        return queryset
