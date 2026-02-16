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
    
    phone = models.CharField(
        verbose_name='手机号',
        max_length=11,
        blank=True,
        null=True,
        help_text='11位手机号码'
    )
    
    dorm_code = models.CharField(
        verbose_name='宿舍号',
        max_length=50,
        blank=True,
        null=True,
        help_text='例如：北一-305'
    )
    
    avatar = models.ImageField(
        verbose_name='头像',
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        help_text='用户头像图片'
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
