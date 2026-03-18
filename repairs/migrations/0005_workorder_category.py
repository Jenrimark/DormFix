# Migration to add category field to WorkOrder and remove repair_type

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0004_add_category_field'),
    ]

    operations = [
        # 添加 category 字段
        migrations.AddField(
            model_name='workorder',
            name='category',
            field=models.CharField(
                choices=[
                    ('水电', '水电'),
                    ('家具', '家具'),
                    ('门窗', '门窗'),
                    ('网络', '网络'),
                    ('电器', '电器'),
                    ('其他', '其他')
                ],
                default='其他',
                help_text='水电、家具、门窗、网络、电器、其他',
                max_length=20,
                verbose_name='故障类别'
            ),
            preserve_default=False,
        ),
        # 移除 repair_type 外键
        migrations.RemoveField(
            model_name='workorder',
            name='repair_type',
        ),
    ]
