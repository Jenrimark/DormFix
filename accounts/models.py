from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型
    继承 Django 的 AbstractUser，添加宿舍报修系统特定字段
    """
    
    ROLE_CHOICES = (
        (1, '学生'),
        (2, '维修人员'),
        (3, '管理员'),
    )
    
    role = models.IntegerField(
        verbose_name='角色',
        choices=ROLE_CHOICES,
        default=1,
        help_text='1:学生, 2:维修人员, 3:管理员'
    )
    
    # 基本信息
    phone = models.CharField(
        verbose_name='手机号',
        max_length=11,
        blank=True,
        null=True,
        help_text='11位手机号码'
    )
    
    avatar = models.ImageField(
        verbose_name='头像',
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        help_text='用户头像图片'
    )
    
    # 学生专属字段（创建后不可修改）
    student_id = models.CharField(
        verbose_name='学号',
        max_length=20,
        blank=True,
        null=True,
        help_text='学生学号'
    )
    
    school = models.CharField(
        verbose_name='学校',
        max_length=100,
        blank=True,
        null=True,
        help_text='所属学校'
    )
    
    campus = models.CharField(
        verbose_name='校区',
        max_length=50,
        blank=True,
        null=True,
        help_text='所属校区'
    )
    
    class_number = models.CharField(
        verbose_name='班号',
        max_length=50,
        blank=True,
        null=True,
        help_text='班级编号'
    )
    
    dorm_code = models.CharField(
        verbose_name='宿舍号',
        max_length=50,
        blank=True,
        null=True,
        help_text='例如：北一-305'
    )
    
    # 可编辑字段
    real_name = models.CharField(
        verbose_name='真实姓名',
        max_length=50,
        blank=True,
        null=True,
        help_text='用户真实姓名'
    )
    
    bio = models.TextField(
        verbose_name='个人简介',
        blank=True,
        null=True,
        help_text='个人简介'
    )
    
    is_active = models.BooleanField(
        verbose_name='账号状态',
        default=True,
        help_text='False表示账号已禁用'
    )
    
    created_at = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_student(self):
        """判断是否为学生"""
        return self.role == 1
    
    def is_repairman(self):
        """判断是否为维修人员"""
        return self.role == 2
    
    def is_admin(self):
        """判断是否为管理员"""
        return self.role == 3
    
    def can_login(self):
        """检查用户是否可以登录"""
        return self.is_active and self.is_authenticated


class OperationLog(models.Model):
    """
    用户日志表
    记录系统中的重要操作，用于审计和追溯
    """
    
    ACTION_CHOICES = (
        ('create_user', '创建用户'),
        ('update_user', '更新用户'),
        ('delete_user', '删除用户'),
        ('reset_password', '重置密码'),
        ('toggle_status', '切换状态'),
        ('assign_order', '派单'),
        ('update_order_status', '更新工单状态'),
        ('batch_enable', '批量启用'),
        ('batch_disable', '批量禁用'),
        ('batch_delete', '批量删除'),
    )
    
    operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='operations',
        verbose_name='操作人'
    )
    
    action = models.CharField(
        verbose_name='操作类型',
        max_length=50,
        choices=ACTION_CHOICES
    )
    
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='target_logs',
        verbose_name='目标用户'
    )
    
    target_order = models.ForeignKey(
        'repairs.WorkOrder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='目标工单'
    )
    
    description = models.TextField(
        verbose_name='操作描述',
        blank=True,
        help_text='详细描述操作内容'
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name='IP地址',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(
        verbose_name='操作时间',
        auto_now_add=True
    )
    
    class Meta:
        db_table = 'operation_logs'
        verbose_name = '用户日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['operator']),
            models.Index(fields=['action']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.operator} - {self.get_action_display()} - {self.created_at}"
