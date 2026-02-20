from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from .models import User
from .serializers import (
    UserSerializer, UserRegisterSerializer, 
    UserLoginSerializer, ChangePasswordSerializer,
    UserProfileUpdateSerializer
)


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
