from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, OperationLog


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_display', 
                  'phone', 'dorm_code', 'avatar', 'avatar_url', 'student_id', 'school', 
                  'campus', 'class_number', 'real_name', 'bio', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_avatar_url(self, obj):
        """返回头像的完整 URL 或 base64"""
        if obj.avatar:
            try:
                # 如果头像存储在数据库中，返回访问 URL
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.avatar.url)
                return obj.avatar.url
            except:
                return None
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户个人信息更新序列化器（除了角色，其他都可以编辑）"""
    
    class Meta:
        model = User
        fields = ['email', 'phone', 'real_name', 'bio', 'avatar', 
                  'student_id', 'school', 'campus', 'class_number', 'dorm_code']
    
    def validate_phone(self, value):
        """验证手机号格式"""
        if value and len(value) != 11:
            raise serializers.ValidationError("手机号必须是11位")
        return value


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'role', 'phone', 'dorm_code', 'student_id', 'school', 
                  'campus', 'class_number', 'real_name']
    
    def validate(self, attrs):
        """验证密码一致性"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("两次密码不一致")
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """验证用户名和密码"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("用户名或密码错误")
            if not user.is_active:
                raise serializers.ValidationError("用户已被禁用")
            attrs['user'] = user
        else:
            raise serializers.ValidationError("必须提供用户名和密码")
        
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    def validate(self, attrs):
        """验证新密码一致性"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("两次新密码不一致")
        return attrs


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    
    operator_username = serializers.CharField(source='operator.username', read_only=True)
    operator_real_name = serializers.CharField(source='operator.real_name', read_only=True)
    target_user_username = serializers.CharField(source='target_user.username', read_only=True)
    target_user_real_name = serializers.CharField(source='target_user.real_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = OperationLog
        fields = ['id', 'operator', 'operator_username', 'operator_real_name',
                  'action', 'action_display', 'target_user', 'target_user_username',
                  'target_user_real_name', 'target_order', 'description',
                  'ip_address', 'created_at']
        read_only_fields = ['id', 'created_at']
