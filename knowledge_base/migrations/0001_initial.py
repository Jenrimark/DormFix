from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('category', models.CharField(choices=[('faq', 'FAQ'), ('sop', '维修SOP'), ('rule', '学校规则')], default='faq', max_length=20, verbose_name='分类')),
                ('role_scope', models.CharField(choices=[('student', '学生'), ('repairman', '维修人员'), ('all', '全部')], default='all', max_length=20, verbose_name='可见角色')),
                ('content', models.TextField(verbose_name='知识内容')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '知识条目',
                'verbose_name_plural': '知识条目',
                'db_table': 'knowledge_items',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='QALog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=20, verbose_name='用户角色')),
                ('question', models.TextField(verbose_name='问题')),
                ('answer', models.TextField(verbose_name='回答')),
                ('success', models.BooleanField(default=True, verbose_name='是否成功')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='错误信息')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='qa_logs', to=settings.AUTH_USER_MODEL, verbose_name='提问用户')),
            ],
            options={
                'verbose_name': '问答日志',
                'verbose_name_plural': '问答日志',
                'db_table': 'qa_logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='knowledgeitem',
            index=models.Index(fields=['category', 'is_active'], name='knowledge_it_categor_62c4b8_idx'),
        ),
        migrations.AddIndex(
            model_name='knowledgeitem',
            index=models.Index(fields=['role_scope', 'is_active'], name='knowledge_it_role_sc_fc4df9_idx'),
        ),
        migrations.AddIndex(
            model_name='qalog',
            index=models.Index(fields=['role', 'created_at'], name='qa_logs_role_92c5ba_idx'),
        ),
        migrations.AddIndex(
            model_name='qalog',
            index=models.Index(fields=['success', 'created_at'], name='qa_logs_success_3d487c_idx'),
        ),
    ]

