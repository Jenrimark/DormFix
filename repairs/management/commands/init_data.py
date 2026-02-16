from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from repairs.models import RepairType, WorkOrder, OrderLog
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = '初始化测试数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')
        
        # 1. 创建用户
        self.stdout.write('创建用户...')
        
        # 创建管理员
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dormfix.com',
                'role': 3,
                'phone': '13800000000',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✓ 创建管理员: admin (密码: admin123)'))
        
        # 创建维修人员
        repairmen = []
        for i in range(1, 4):
            repairman, created = User.objects.get_or_create(
                username=f'repairman{i}',
                defaults={
                    'email': f'repairman{i}@dormfix.com',
                    'role': 2,
                    'phone': f'1380000000{i}',
                }
            )
            if created:
                repairman.set_password('repair123')
                repairman.save()
                self.stdout.write(self.style.SUCCESS(f'✓ 创建维修员: repairman{i} (密码: repair123)'))
            repairmen.append(repairman)
        
        # 创建学生
        students = []
        dorms = ['北一-305', '南二-208', '东三-412', '西四-501', '北二-106']
        for i in range(1, 6):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@dormfix.com',
                    'role': 1,
                    'phone': f'1390000000{i}',
                    'dorm_code': dorms[i-1],
                }
            )
            if created:
                student.set_password('student123')
                student.save()
                self.stdout.write(self.style.SUCCESS(f'✓ 创建学生: student{i} (密码: student123, 宿舍: {dorms[i-1]})'))
            students.append(student)
        
        # 2. 创建故障类型
        self.stdout.write('\n创建故障类型...')
        repair_types_data = [
            {'name': '水电类', 'priority': 'high', 'description': '漏水、断电、照明等问题'},
            {'name': '家具类', 'priority': 'medium', 'description': '床、桌椅、柜子等家具问题'},
            {'name': '门窗类', 'priority': 'medium', 'description': '门锁、窗户、玻璃等问题'},
            {'name': '网络类', 'priority': 'high', 'description': '网络故障、网口损坏等'},
            {'name': '其他', 'priority': 'low', 'description': '其他类型的报修'},
        ]
        
        repair_types = []
        for data in repair_types_data:
            repair_type, created = RepairType.objects.get_or_create(
                name=data['name'],
                defaults={
                    'priority': data['priority'],
                    'description': data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ 创建故障类型: {data["name"]}'))
            repair_types.append(repair_type)
        
        # 3. 创建测试工单
        self.stdout.write('\n创建测试工单...')
        
        work_orders_data = [
            {
                'user': students[0],
                'repair_type': repair_types[0],
                'priority': 'high',
                'content': '卫生间水龙头漏水严重，地面积水，需要紧急处理',
                'status': 2,  # 维修中
                'repairman': repairmen[0],
            },
            {
                'user': students[1],
                'repair_type': repair_types[2],
                'priority': 'medium',
                'content': '宿舍门锁有点松动，关门时需要用力',
                'status': 0,  # 待审核
            },
            {
                'user': students[0],
                'repair_type': repair_types[1],
                'priority': 'low',
                'content': '空调不制热，需要检修',
                'status': 3,  # 已完成
                'repairman': repairmen[0],
                'finish_time': timezone.now() - timedelta(days=2),
            },
            {
                'user': students[2],
                'repair_type': repair_types[3],
                'priority': 'high',
                'content': '宿舍网络无法连接，网口指示灯不亮',
                'status': 1,  # 已派单
                'repairman': repairmen[1],
            },
            {
                'user': students[3],
                'repair_type': repair_types[1],
                'priority': 'medium',
                'content': '书桌抽屉损坏，无法正常开关',
                'status': 3,  # 已完成
                'repairman': repairmen[2],
                'finish_time': timezone.now() - timedelta(days=5),
            },
        ]
        
        for i, data in enumerate(work_orders_data):
            # 设置创建时间（模拟不同时间提交）
            create_time = timezone.now() - timedelta(days=random.randint(0, 7))
            
            work_order = WorkOrder.objects.create(
                user=data['user'],
                repair_type=data['repair_type'],
                priority=data['priority'],
                content=data['content'],
                status=data['status'],
                repairman=data.get('repairman'),
                finish_time=data.get('finish_time'),
            )
            work_order.create_time = create_time
            work_order.save()
            
            # 创建对应的日志
            OrderLog.objects.create(
                work_order=work_order,
                operator=data['user'],
                action='submit',
                remark='工单提交',
                create_time=create_time
            )
            
            if data['status'] >= 1 and data.get('repairman'):
                OrderLog.objects.create(
                    work_order=work_order,
                    operator=admin,
                    action='assign',
                    remark=f'派单给 {data["repairman"].username}',
                    create_time=create_time + timedelta(minutes=30)
                )
            
            if data['status'] >= 2:
                OrderLog.objects.create(
                    work_order=work_order,
                    operator=data['repairman'],
                    action='start',
                    remark='开始维修',
                    create_time=create_time + timedelta(hours=1)
                )
            
            if data['status'] == 3:
                OrderLog.objects.create(
                    work_order=work_order,
                    operator=data['repairman'],
                    action='complete',
                    remark='维修完成',
                    create_time=data['finish_time']
                )
            
            self.stdout.write(self.style.SUCCESS(f'✓ 创建工单: {work_order.order_sn} ({work_order.get_status_display()})'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ 数据初始化完成！'))
        self.stdout.write('\n登录信息：')
        self.stdout.write('管理员: admin / admin123')
        self.stdout.write('维修员: repairman1 / repair123')
        self.stdout.write('学生: student1 / student123')
