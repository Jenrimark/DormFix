from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Type(models.TextChoices):
        FEEDBACK_REPLY = 'feedback_reply', '反馈回复'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='接收人',
    )

    type = models.CharField(
        max_length=30,
        choices=Type.choices,
        default=Type.FEEDBACK_REPLY,
        db_index=True,
        verbose_name='通知类型',
    )

    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')

    is_read = models.BooleanField(default=False, db_index=True, verbose_name='已读')

    feedback = models.ForeignKey(
        'feedbacks.Feedback',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='关联反馈',
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'notifications'
        verbose_name = '站内通知'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'created_at']),
        ]

    def __str__(self):
        return f'Notification#{self.id} to {self.user_id}'

