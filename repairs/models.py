from django.db import models
from django.conf import settings
from django.utils import timezone
import random
import string


class RepairType(models.Model):
    """
    故障类型表
    """
    
    PRIORITY_CHOICES = (
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    )
    
    name = models.CharField(
        verbose_name='类型名称',
        max_length=50,
        unique=True,
        help_text='例如：水电类、家具类、门窗类、网络类'
    )
    
    priority = models.CharField(
        verbose_name='优先级',
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text='用于后台排序显示紧急程度'
    )
    
    description = models.TextField(
        verbose_name='描述',
        blank=True,
        null=True,
        help_text='类型说明'
    )
    
    created_at = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    
    class Meta:
        db_table = 'repair_types'
        verbose_name = '故障类型'
        verbose_name_plural = verbose_name
        ordering = ['id']
    
    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"


class WorkOrder(models.Model):
    """
    报修工单表 - 核心表
    """
    
    STATUS_CHOICES = (
        (0, '待审核'),
        (1, '已派单'),
        (2, '维修中'),
        (3, '已完成'),
        (4, '已取消'),
    )
    
    PRIORITY_CHOICES = (
        ('low', '不急'),
        ('medium', '一般'),
        ('high', '紧急'),
    )
    
    order_sn = models.CharField(
        verbose_name='工单编号',
        max_length=50,
        unique=True,
        help_text='格式：YYYYMMDD+随机码'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_orders',
        verbose_name='提交人',
        help_text='关联学生用户'
    )
    
    repair_type = models.ForeignKey(
        RepairType,
        on_delete=models.PROTECT,
        related_name='work_orders',
        verbose_name='故障类型'
    )
    
    status = models.IntegerField(
        verbose_name='状态',
        choices=STATUS_CHOICES,
        default=0,
        help_text='0:待审核, 1:已派单, 2:维修中, 3:已完成, 4:已取消'
    )
    
    priority = models.CharField(
        verbose_name='紧急程度',
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    content = models.TextField(
        verbose_name='故障描述',
        help_text='详细描述故障情况'
    )
    
    img_proof = models.ImageField(
        verbose_name='现场照片',
        upload_to='work_orders/%Y/%m/',
        blank=True,
        null=True,
        help_text='支持上传现场照片'
    )
    
    repairman = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_orders',
        verbose_name='维修人员',
        blank=True,
        null=True,
        help_text='派单后填充'
    )
    
    create_time = models.DateTimeField(
        verbose_name='提交时间',
        auto_now_add=True
    )
    
    finish_time = models.DateTimeField(
        verbose_name='完工时间',
        blank=True,
        null=True
    )
    
    remark = models.TextField(
        verbose_name='备注',
        blank=True,
        null=True,
        help_text='维修备注、耗材等'
    )
    
    class Meta:
        db_table = 'work_orders'
        verbose_name = '报修工单'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
        indexes = [
            models.Index(fields=['order_sn']),
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['repairman']),
        ]
    
    def __str__(self):
        return f"{self.order_sn} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        """重写 save 方法，自动生成工单编号"""
        if not self.order_sn:
            self.order_sn = self.generate_order_sn()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_order_sn():
        """生成工单编号：YYYYMMDD + 3位随机数"""
        date_str = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.digits, k=3))
        return f"{date_str}{random_str}"
    
    def is_pending(self):
        """是否待审核"""
        return self.status == 0
    
    def is_assigned(self):
        """是否已派单"""
        return self.status == 1
    
    def is_in_progress(self):
        """是否维修中"""
        return self.status == 2
    
    def is_completed(self):
        """是否已完成"""
        return self.status == 3
    
    def is_cancelled(self):
        """是否已取消"""
        return self.status == 4


class OrderLog(models.Model):
    """
    工单日志/流转记录表
    实现"可追溯"，记录每一个状态变化的瞬间
    """
    
    ACTION_CHOICES = (
        ('submit', '提交'),
        ('review', '审核'),
        ('assign', '派单'),
        ('start', '开始维修'),
        ('complete', '完工'),
        ('cancel', '取消'),
        ('comment', '评价'),
    )
    
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='关联工单'
    )
    
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='操作人',
        help_text='是谁派的单？是谁点的完工？'
    )
    
    action = models.CharField(
        verbose_name='动作',
        max_length=20,
        choices=ACTION_CHOICES,
        help_text='提交、审核、派单、完工、评价'
    )
    
    remark = models.TextField(
        verbose_name='备注',
        blank=True,
        null=True,
        help_text='例如：缺少零件，需采购'
    )
    
    create_time = models.DateTimeField(
        verbose_name='操作时间',
        auto_now_add=True
    )
    
    class Meta:
        db_table = 'order_logs'
        verbose_name = '工单日志'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
    
    def __str__(self):
        return f"{self.work_order.order_sn} - {self.get_action_display()}"


class Comment(models.Model):
    """
    评价表
    """
    
    work_order = models.OneToOneField(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='关联工单'
    )
    
    score = models.IntegerField(
        verbose_name='评分',
        help_text='1-5星',
        choices=[(i, f'{i}星') for i in range(1, 6)]
    )
    
    feedback = models.TextField(
        verbose_name='文字反馈',
        blank=True,
        null=True
    )
    
    create_time = models.DateTimeField(
        verbose_name='评价时间',
        auto_now_add=True
    )
    
    class Meta:
        db_table = 'comments'
        verbose_name = '评价'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
    
    def __str__(self):
        return f"{self.work_order.order_sn} - {self.score}星"


class StoredFile(models.Model):
    """
    将上传文件存入数据库，便于部署到平台时无本地磁盘依赖。
    """
    name = models.CharField(verbose_name='文件名', max_length=255)
    content = models.BinaryField(verbose_name='文件内容')
    content_type = models.CharField(verbose_name='MIME类型', max_length=128, default='application/octet-stream')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stored_files'
        verbose_name = '存储文件'
        verbose_name_plural = verbose_name
