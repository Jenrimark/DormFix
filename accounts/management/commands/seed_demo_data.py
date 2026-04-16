from datetime import timedelta
import mimetypes
import os
import random
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from accounts.models import User
from announcements.models import Announcement
from feedbacks.models import Feedback
from knowledge_base.models import KnowledgeItem, QALog
from notifications.models import Notification
from repairs.models import Comment, OrderLog, RepairType, StoredFile, WorkOrder


class Command(BaseCommand):
    help = '使用现有 9 个账号生成完整演示数据（工单/评价/反馈/通知/知识库/公告）'

    student_status_templates = [
        {'status': 0, 'label': '待审核'},
        {'status': 1, 'label': '已派单'},
        {'status': 2, 'label': '维修中'},
        {'status': 3, 'label': '已完成已评价', 'commented': True},
        {'status': 3, 'label': '已完成未评价', 'commented': False},
        {'status': 4, 'label': '已取消'},
    ]

    categories = ['水电', '家具', '门窗', '网络', '电器', '其他']
    priorities = ['high', 'medium', 'low', 'medium', 'high', 'low']
    contents = [
        '卫生间水龙头持续滴水，晚上噪音明显，地面也会有积水。',
        '宿舍椅子靠背松动，坐下时有明显晃动，存在安全隐患。',
        '阳台推拉窗卡顿严重，关闭后还有缝隙，雨天容易进水。',
        '宿舍 WiFi 时断时续，晚高峰经常掉线，影响上网课。',
        '空调制冷效果很差，开了很久也不凉，宿舍里比较闷热。',
        '公共区域灯光忽明忽暗，怀疑线路接触不良，希望尽快检查。',
    ]
    repair_notes = [
        '已检查故障点并完成维修处理，现场测试运行正常。',
        '更换损坏部件后再次测试，问题已解决。',
        '完成线路/结构调整，当前使用无异常。',
    ]
    review_remarks = [
        '情况属实，安排尽快处理。',
        '已审核通过，请维修员跟进。',
        '问题较为紧急，优先派单。',
    ]
    cancel_remarks = [
        '学生临时不在宿舍，申请取消。',
        '问题已自行处理，无需继续维修。',
        '已联系宿管线下解决，撤销本次工单。',
    ]
    comment_feedbacks = [
        '维修很及时，师傅态度很好，问题已经彻底解决。',
        '整体处理不错，但等待接单时间稍微有点久。',
        '维修后效果正常，过程沟通也比较顺畅。',
        '问题解决了，建议后续能再快一点到场。',
        '师傅认真负责，维修说明也写得很清楚。',
    ]
    feedback_templates = [
        {
            'category': Feedback.Category.SUGGESTION,
            'status': Feedback.Status.NEW,
            'content': '建议在工单列表中增加按宿舍号和时间筛选，查找会更方便。',
            'reply': '',
        },
        {
            'category': Feedback.Category.ISSUE,
            'status': Feedback.Status.IN_PROGRESS,
            'content': '反馈记录页面在手机上查看时，表格内容有些拥挤，希望适配更好。',
            'reply': '已收到，前端样式正在优化处理中。',
        },
        {
            'category': Feedback.Category.OTHER,
            'status': Feedback.Status.RESOLVED,
            'content': '希望维修完成后除了站内提醒，也能有更明显的红点提示。',
            'reply': '该建议已处理，系统已增加回复通知和红点提醒。',
        },
    ]
    knowledge_seed = [
        ('学生报修流程说明', 'faq', 'student', '学生提交报修后，工单会先进入待审核状态，管理员审核通过后再派单给维修员。'),
        ('工单状态含义', 'faq', 'all', '待审核表示管理员尚未审核；已派单表示已分配维修员；维修中表示师傅已开始处理；已完成表示维修结束；已取消表示流程终止。'),
        ('如何补充问题描述', 'faq', 'student', '描述问题时建议写清楚故障位置、出现时间、影响程度以及是否有安全隐患，便于快速定位。'),
        ('评价规则说明', 'rule', 'student', '已完成工单可评价一次，评价包含 1-5 星和文字反馈，提交后不能重复修改。'),
        ('维修员接单规范', 'sop', 'repairman', '维修员接单后应尽快确认现场情况，如需延期或无法处理，应及时备注并反馈管理员。'),
        ('维修开始前检查项', 'sop', 'repairman', '开始维修前需确认故障位置、断电/断水安全措施、维修工具和耗材是否齐备。'),
        ('维修完成说明规范', 'sop', 'repairman', '完工时需填写维修说明，必要时上传维修凭证图片，并写明更换部件或耗材情况。'),
        ('管理员审核建议', 'rule', 'all', '管理员审核工单时应优先关注安全风险、紧急程度和问题描述完整性。'),
        ('常见漏水问题处理', 'faq', 'all', '如遇持续漏水、地面积水等情况，应优先关闭水源并尽快报修，必要时联系宿管协助。'),
        ('网络问题排查建议', 'faq', 'all', '若宿舍网络异常，可先确认是否仅单个设备故障，再检查路由器、网线或校园网认证状态。'),
        ('空调报修提醒', 'rule', 'student', '空调类问题建议补充是否通电、是否制冷/制热异常、是否有异响或漏水现象。'),
        ('高峰期服务说明', 'rule', 'all', '报修高峰期处理时效可能略有延长，系统会尽量按紧急程度排序派单。'),
    ]

    announcements_seed = [
        ('宿舍报修高峰期说明', '近期报修量较大，系统会优先处理高风险和紧急工单，请同学们补充完整描述。'),
        ('空调与网络问题填报规范', '提交空调或网络问题时，请尽量描述故障表现、持续时间和影响范围。'),
        ('维修完成评价提醒', '已完成工单支持一次评价，评价将用于服务质量改进和绩效统计。'),
        ('系统反馈功能上线', '现已支持系统反馈与回复通知，欢迎同学们提出建议与问题。'),
    ]

    def handle(self, *args, **options):
        with transaction.atomic():
            users = self._load_users()
            admin = users['admin']
            repairmen = users['repairmen']
            students = users['students']

            self._ensure_demo_user_avatars(admin, repairmen, students)
            self._ensure_repair_types()
            self._clear_demo_data(admin, students)
            counts = self._seed_all(admin, repairmen, students)

        self.stdout.write(self.style.SUCCESS('演示数据生成完成'))
        for key, value in counts.items():
            self.stdout.write(f'- {key}: {value}')

    def _load_users(self):
        required = ['admin', 'repairman1', 'repairman2', 'repairman3', 'student1', 'student2', 'student3', 'student4', 'student5']
        user_map = {u.username: u for u in User.objects.filter(username__in=required)}
        missing = [username for username in required if username not in user_map]
        if missing:
            raise CommandError(f'缺少账号: {", ".join(missing)}')

        return {
            'admin': user_map['admin'],
            'repairmen': [user_map['repairman1'], user_map['repairman2'], user_map['repairman3']],
            'students': [user_map['student1'], user_map['student2'], user_map['student3'], user_map['student4'], user_map['student5']],
        }

    def _ensure_demo_user_avatars(self, admin, repairmen, students):
        """
        为内置账号补齐头像（avatar）。
        头像图片从本地 `数据库/dataset_images` 随机取素材。
        只有当 avatar 为空时才写入。
        """
        all_users = [admin, *repairmen, *students]
        for user in all_users:
            if user.avatar:
                continue

            user.avatar = self._make_dataset_image_content_file(
                filename_prefix=f'seed_demo_avatar_{user.username}',
            )
            user.save(update_fields=['avatar'])

    def _dataset_images_dir(self):
        return os.path.join(settings.BASE_DIR, '数据库', 'dataset_images')

    def _get_dataset_image_paths(self):
        """
        读取本地数据集图片路径（用于 mock 图片）。
        """
        if hasattr(self, '_dataset_image_paths_cache'):
            return self._dataset_image_paths_cache

        img_dir = self._dataset_images_dir()
        if not os.path.isdir(img_dir):
            raise CommandError(f'找不到数据集图片目录：{img_dir}')

        exts = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        paths = []
        for name in os.listdir(img_dir):
            ext = os.path.splitext(name)[1].lower()
            if ext in exts:
                p = os.path.join(img_dir, name)
                if os.path.isfile(p):
                    paths.append(p)

        if not paths:
            raise CommandError(f'图片目录为空：{img_dir}，请先把图片放到该目录')

        self._dataset_image_paths_cache = paths
        return paths

    def _make_dataset_image_content_file(self, filename_prefix):
        """
        从数据集图片目录随机挑一张，包装为 ImageField/Storage 可用的 ContentFile。
        """
        src_path = random.choice(self._get_dataset_image_paths())
        _, src_ext = os.path.splitext(src_path)
        src_ext = src_ext.lower() or '.jpg'

        dest_name = f'{filename_prefix}_{uuid.uuid4().hex}{src_ext}'
        with open(src_path, 'rb') as f:
            content_bytes = f.read()

        content = ContentFile(content_bytes, name=dest_name)
        content.content_type = mimetypes.guess_type(dest_name)[0] or 'application/octet-stream'
        return content

    def _ensure_repair_types(self):
        repair_type_defs = [
            ('水电', '水龙头漏水', 'high'),
            ('家具', '椅子损坏', 'medium'),
            ('门窗', '窗户卡顿', 'medium'),
            ('网络', '网络不稳定', 'medium'),
            ('电器', '空调不制冷', 'high'),
            ('其他', '公共照明异常', 'low'),
        ]
        for category, name, priority in repair_type_defs:
            RepairType.objects.get_or_create(
                category=category,
                name=name,
                defaults={
                    'priority': priority,
                    'description': f'{name} 默认数据类型',
                },
            )

    def _clear_demo_data(self, admin, students):
        student_ids = [s.id for s in students]
        WorkOrder.objects.filter(user_id__in=student_ids).delete()
        Feedback.objects.filter(user_id__in=student_ids).delete()
        Notification.objects.filter(user_id__in=student_ids).delete()
        # 兼容清理旧版数据：历史上标题带有“【演示】”前缀
        Announcement.objects.filter(
            Q(title__startswith='【演示】') | Q(title__in=[t for t, _ in self.announcements_seed]),
            author=admin,
        ).delete()
        KnowledgeItem.objects.filter(
            Q(title__startswith='【演示】') | Q(title__in=[t for t, _, _, _ in self.knowledge_seed]),
            # KnowledgeItem 只有 title/category 等字段，不带 author
        ).delete()
        QALog.objects.all().delete()
        # 图片字段存储在数据库的 StoredFile 中；删除工单不会自动删除 StoredFile，需要显式清理由 seed 生成的图片
        StoredFile.objects.filter(
            Q(name__startswith='seed_demo_') | Q(name__startswith='demo_seed_')
        ).delete()

    def _seed_all(self, admin, repairmen, students):
        counts = {
            '工单': 0,
            '评价': 0,
            '反馈': 0,
            '通知': 0,
            '知识条目': 0,
            '公告': 0,
            '问答日志': 0,
        }

        now = timezone.now()
        for student_index, student in enumerate(students):
            for template_index, template in enumerate(self.student_status_templates):
                created_at = now - timedelta(days=(student_index * 4 + template_index + 1), hours=template_index * 2)
                category = self.categories[(student_index + template_index) % len(self.categories)]
                priority = self.priorities[(student_index + template_index) % len(self.priorities)]
                content = self.contents[(student_index + template_index) % len(self.contents)]
                repairman = repairmen[(student_index + template_index) % len(repairmen)]
                status = template['status']
                order_sn = self._generate_order_sn(student_index, template_index)

                # 让前端能展示“图片缩略图”：所有状态补现场照片，已完成再补维修凭证
                img_proof = self._make_dataset_image_content_file(
                    filename_prefix=f'seed_demo_order_site_{order_sn}',
                )

                repair_proof_img = None
                if status == 3:
                    repair_proof_img = self._make_dataset_image_content_file(
                        filename_prefix=f'seed_demo_order_proof_{order_sn}',
                    )
                order = WorkOrder.objects.create(
                    order_sn=order_sn,
                    user=student,
                    category=category,
                    status=status,
                    priority=priority,
                    content=f'{content}（{student.dorm_code or student.real_name or student.username}）',
                    repairman=repairman if status in [1, 2, 3] else None,
                    reviewer=admin if status != 0 else None,
                    review_remark=self.review_remarks[(student_index + template_index) % len(self.review_remarks)] if status != 0 else None,
                    repair_description=self.repair_notes[(student_index + template_index) % len(self.repair_notes)] if status == 3 else '',
                    remark=self.cancel_remarks[(student_index + template_index) % len(self.cancel_remarks)] if status == 4 else '',
                    img_proof=img_proof,
                    repair_proof_img=repair_proof_img,
                )

                review_time = created_at + timedelta(hours=4) if status != 0 else None
                accept_time = review_time + timedelta(hours=3) if status in [1, 2, 3] else None
                start_time = accept_time + timedelta(hours=5) if status in [2, 3] else None
                finish_time = start_time + timedelta(hours=8) if status == 3 else None
                WorkOrder.objects.filter(pk=order.pk).update(
                    create_time=created_at,
                    review_time=review_time,
                    accept_time=accept_time,
                    start_time=start_time,
                    finish_time=finish_time,
                )
                order.refresh_from_db()
                counts['工单'] += 1

                self._create_order_logs(order, admin, repairman, created_at)

                if template.get('commented'):
                    comment_created_at = finish_time + timedelta(hours=6)
                    comment = Comment.objects.create(
                        work_order=order,
                        score=[5, 4, 5, 3, 5][student_index % 5],
                        feedback=self.comment_feedbacks[(student_index + template_index) % len(self.comment_feedbacks)],
                    )
                    Comment.objects.filter(pk=comment.pk).update(create_time=comment_created_at)
                    OrderLog.objects.create(
                        work_order=order,
                        operator=student,
                        action='comment',
                        remark=f'评分：{comment.score}星',
                    )
                    counts['评价'] += 1

            feedback_count, notification_count = self._create_feedbacks(student, admin, now - timedelta(days=student_index))
            counts['反馈'] += feedback_count
            counts['通知'] += notification_count

        counts['知识条目'] = self._create_knowledge_items()
        counts['公告'] = self._create_announcements(admin)
        counts['问答日志'] = self._create_qa_logs(students, repairmen)
        return counts

    def _generate_order_sn(self, student_index, template_index):
        date_str = timezone.now().strftime('%Y%m%d')
        suffix = f'{student_index + 1}{template_index + 1}8{(student_index + template_index) % 10}'
        return f'{date_str}{suffix}'

    def _create_order_logs(self, order, admin, repairman, created_at):
        logs = [
            ('submit', order.user, '学生提交报修', created_at),
        ]

        if order.status != 0:
            logs.append(('review_pass', admin, order.review_remark or '管理员审核通过', order.review_time))
        if order.status in [1, 2, 3]:
            logs.append(('assign', admin, f'派单给 {repairman.real_name or repairman.username}', order.accept_time - timedelta(minutes=30)))
            logs.append(('accept', repairman, '维修员已接单', order.accept_time))
        if order.status in [2, 3]:
            logs.append(('start', repairman, '维修员开始上门处理', order.start_time))
        if order.status == 3:
            logs.append(('complete', repairman, order.repair_description or '维修完成', order.finish_time))
        if order.status == 4:
            logs.append(('cancel', order.user, order.remark or '学生取消工单', created_at + timedelta(hours=6)))

        for action, operator, remark, log_time in logs:
            if not log_time:
                continue
            log = OrderLog.objects.create(
                work_order=order,
                operator=operator,
                action=action,
                remark=remark,
            )
            OrderLog.objects.filter(pk=log.pk).update(create_time=log_time)

    def _create_feedbacks(self, student, admin, base_time):
        feedback_count = 0
        notification_count = 0
        for idx, template in enumerate(self.feedback_templates):
            created_at = base_time - timedelta(days=idx + 1, hours=idx * 3)
            handled_at = created_at + timedelta(hours=12) if template['status'] != Feedback.Status.NEW else None
            feedback = Feedback.objects.create(
                user=student,
                category=template['category'],
                content=f'{template["content"]}（{student.real_name or student.username}）',
                contact=f'{student.username}@demo.local',
                status=template['status'],
                admin_reply=template['reply'] or None,
                handled_by=admin if template['status'] != Feedback.Status.NEW else None,
                handled_at=handled_at,
            )
            Feedback.objects.filter(pk=feedback.pk).update(created_at=created_at, updated_at=handled_at or created_at)
            feedback_count += 1

            if template['reply']:
                notification = Notification.objects.create(
                    user=student,
                    type=Notification.Type.FEEDBACK_REPLY,
                    title='你的反馈有新回复',
                    content=template['reply'],
                    feedback=feedback,
                    is_read=(idx % 2 == 0),
                )
                Notification.objects.filter(pk=notification.pk).update(created_at=(handled_at or created_at) + timedelta(minutes=5))
                notification_count += 1

        return feedback_count, notification_count

    def _create_knowledge_items(self):
        count = 0
        for title, category, role_scope, content in self.knowledge_seed:
            KnowledgeItem.objects.create(
                title=title,
                category=category,
                role_scope=role_scope,
                content=content,
                is_active=True,
            )
            count += 1
        return count

    def _create_announcements(self, admin):
        for idx, (title, content) in enumerate(self.announcements_seed):
            ann = Announcement.objects.create(
                title=title,
                content=content,
                author=admin,
                is_active=True,
            )
            Announcement.objects.filter(pk=ann.pk).update(created_at=timezone.now() - timedelta(days=idx + 1))
        return len(self.announcements_seed)

    def _create_qa_logs(self, students, repairmen):
        samples = [
            ('学生', students[0], '宿舍漏水先做什么？', '如发现持续漏水，建议先关闭水源并尽快提交工单；若有积水需注意防滑，并联系宿管协助。'),
            ('学生', students[1], '工单完成后还能再评价吗？', '每个已完成工单只允许评价一次，提交后不能重复修改，请在确认问题处理结果后再提交。'),
            ('学生', students[2], '审核一般多久完成？', '管理员会尽快审核，若问题紧急建议在描述中明确风险点，系统会优先安排处理。'),
            ('学生', students[3], '反馈记录在哪里看？', '你可以在导航中的“反馈”页面查看反馈记录、状态和管理员回复。'),
            ('维修人员', repairmen[0], '接单后第一步该做什么？', '接单后应先确认故障位置与影响范围，必要时联系学生确认现场情况，再准备工具和耗材。'),
            ('维修人员', repairmen[1], '完工时要填什么？', '维修完成后需填写维修说明，如有耗材或更换部件建议一并备注，必要时上传维修凭证。'),
            ('维修人员', repairmen[2], '知识库没有对应答案怎么办？', '可先根据通用维修规范给出稳妥建议，并提醒用户以管理员发布规则为准。'),
            ('学生', students[4], '网络波动怎么处理？', '可先确认是否仅单个设备异常，再检查宿舍路由器、网线或校园网认证状态，必要时提交网络类工单。'),
        ]
        count = 0
        for idx, (role, user, question, answer) in enumerate(samples):
            log = QALog.objects.create(
                user=user,
                role=role,
                question=question,
                answer=answer,
                success=True,
            )
            QALog.objects.filter(pk=log.pk).update(created_at=timezone.now() - timedelta(days=idx, hours=idx))
            count += 1
        return count

