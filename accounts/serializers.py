from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_display', 
                  'phone', 'dorm_code', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'role', 'phone', 'dorm_code']
    
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
