from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='文档标题')),
                ('role_scope', models.CharField(choices=[('student', '学生'), ('repairman', '维修人员'), ('all', '全部')], default='all', max_length=20, verbose_name='可见角色')),
                ('file', models.FileField(upload_to='knowledge_docs/%Y/%m/', verbose_name='知识文件')),
                ('original_filename', models.CharField(max_length=255, verbose_name='原始文件名')),
                ('extracted_text', models.TextField(blank=True, default='', verbose_name='提取文本')),
                ('parse_status', models.CharField(default='pending', help_text='pending/success/failed', max_length=20, verbose_name='解析状态')),
                ('parse_error', models.TextField(blank=True, default='', verbose_name='解析错误')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '知识文档',
                'verbose_name_plural': '知识文档',
                'db_table': 'knowledge_documents',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.AddIndex(
            model_name='knowledgedocument',
            index=models.Index(fields=['role_scope', 'is_active'], name='knowledge_d_role_sc_1e66b0_idx'),
        ),
        migrations.AddIndex(
            model_name='knowledgedocument',
            index=models.Index(fields=['parse_status', 'is_active'], name='knowledge_d_parse_s_6f710d_idx'),
        ),
    ]

