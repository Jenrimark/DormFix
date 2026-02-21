from django.db import models
from accounts.models import User


class Announcement(models.Model):
    """系统公告模型"""
    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements', verbose_name='发布者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    
    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
        verbose_name = '系统公告'
        verbose_name_plural = '系统公告'
    
    def __str__(self):
        return self.title
