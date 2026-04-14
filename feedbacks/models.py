from django.conf import settings
from django.db import models


class Feedback(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', '新提交'
        IN_PROGRESS = 'in_progress', '处理中'
        RESOLVED = 'resolved', '已解决'
        CLOSED = 'closed', '已关闭'

    class Category(models.TextChoices):
        SUGGESTION = 'suggestion', '功能建议'
        ISSUE = 'issue', '使用问题'
        COMPLAINT = 'complaint', '投诉'
        OTHER = 'other', '其他'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='提交人',
    )

    category = models.CharField(
        verbose_name='类别',
        max_length=30,
        choices=Category.choices,
        default=Category.OTHER,
    )

    content = models.TextField(verbose_name='反馈内容')

    contact = models.CharField(
        verbose_name='联系方式',
        max_length=100,
        blank=True,
        null=True,
        help_text='可填手机号/邮箱/微信等，便于联系',
    )

    status = models.CharField(
        verbose_name='状态',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )

    admin_reply = models.TextField(
        verbose_name='管理员回复',
        blank=True,
        null=True,
    )

    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='handled_feedbacks',
        blank=True,
        null=True,
        verbose_name='处理人',
    )
    handled_at = models.DateTimeField(blank=True, null=True, verbose_name='处理时间')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'feedbacks'
        verbose_name = '系统反馈'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f'Feedback#{self.id} {self.user_id} {self.status}'

