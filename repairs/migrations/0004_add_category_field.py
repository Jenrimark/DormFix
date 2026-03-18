# Generated migration for adding category field to RepairType

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0003_workorder_accept_time_workorder_repair_description_and_more'),
    ]

    operations = [
        # 添加 category 字段
        migrations.AddField(
            model_name='repairtype',
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
                help_text='一级分类：水电、家具、门窗、网络等',
                max_length=20,
                verbose_name='故障类别'
            ),
        ),
        # 移除 name 字段的 unique 约束
        migrations.AlterField(
            model_name='repairtype',
            name='name',
            field=models.CharField(
                help_text='例如：水龙头漏水、灯泡不亮、桌椅损坏',
                max_length=50,
                verbose_name='具体问题'
            ),
        ),
        # 修改 Meta 选项
        migrations.AlterModelOptions(
            name='repairtype',
            options={
                'ordering': ['category', 'priority', 'id'],
                'verbose_name': '故障类型',
                'verbose_name_plural': '故障类型'
            },
        ),
        # 添加 unique_together 约束
        migrations.AlterUniqueTogether(
            name='repairtype',
            unique_together={('category', 'name')},
        ),
    ]
