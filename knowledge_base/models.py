from django.conf import settings
from django.db import models


class KnowledgeItem(models.Model):
    class Category(models.TextChoices):
        FAQ = 'faq', 'FAQ'
        SOP = 'sop', '维修SOP'
        RULE = 'rule', '学校规则'

    class RoleScope(models.TextChoices):
        STUDENT = 'student', '学生'
        REPAIRMAN = 'repairman', '维修人员'
        ALL = 'all', '全部'

    title = models.CharField(max_length=200, verbose_name='标题')
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.FAQ,
        verbose_name='分类',
    )
    role_scope = models.CharField(
        max_length=20,
        choices=RoleScope.choices,
        default=RoleScope.ALL,
        verbose_name='可见角色',
    )
    content = models.TextField(verbose_name='知识内容')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'knowledge_items'
        verbose_name = '知识条目'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['role_scope', 'is_active']),
        ]

    def __str__(self):
        return f'{self.get_category_display()} - {self.title}'


class QALog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='qa_logs',
        verbose_name='提问用户',
    )
    role = models.CharField(max_length=20, verbose_name='用户角色')
    question = models.TextField(verbose_name='问题')
    answer = models.TextField(verbose_name='回答')
    success = models.BooleanField(default=True, verbose_name='是否成功')
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'qa_logs'
        verbose_name = '问答日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role', 'created_at']),
            models.Index(fields=['success', 'created_at']),
        ]

    def __str__(self):
        return f'QALog#{self.id} {self.role}'


class KnowledgeDocument(models.Model):
    class RoleScope(models.TextChoices):
        STUDENT = 'student', '学生'
        REPAIRMAN = 'repairman', '维修人员'
        ALL = 'all', '全部'

    title = models.CharField(max_length=200, verbose_name='文档标题')
    role_scope = models.CharField(
        max_length=20,
        choices=RoleScope.choices,
        default=RoleScope.ALL,
        verbose_name='可见角色',
    )
    file = models.FileField(upload_to='knowledge_docs/%Y/%m/', verbose_name='知识文件')
    original_filename = models.CharField(max_length=255, verbose_name='原始文件名')
    extracted_text = models.TextField(blank=True, default='', verbose_name='提取文本')
    parse_status = models.CharField(
        max_length=20,
        default='pending',
        verbose_name='解析状态',
        help_text='pending/success/failed',
    )
    parse_error = models.TextField(blank=True, default='', verbose_name='解析错误')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'knowledge_documents'
        verbose_name = '知识文档'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['role_scope', 'is_active']),
            models.Index(fields=['parse_status', 'is_active']),
        ]

    def __str__(self):
        return f'{self.title} ({self.original_filename})'

