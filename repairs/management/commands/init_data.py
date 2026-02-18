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
                'real_name': '系统管理员',
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
                    'real_name': f'维修员{i}',
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
        schools = ['清华大学', '北京大学', '复旦大学', '上海交通大学', '浙江大学']
        campuses = ['本部', '东校区', '西校区', '南校区', '北校区']
        for i in range(1, 6):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@dormfix.com',
                    'role': 1,
                    'phone': f'1390000000{i}',
                    'dorm_code': dorms[i-1],
                    'student_id': f'2024{10000 + i}',
                    'school': schools[i-1],
                    'campus': campuses[i-1],
                    'class_number': f'计算机{i}班',
                    'real_name': f'学生{i}',
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
            # 水电类
            {'name': '水电类 - 漏水', 'priority': 'high', 'description': '水龙头、水管、马桶漏水等'},
            {'name': '水电类 - 断电', 'priority': 'high', 'description': '宿舍断电、跳闸、电路故障'},
            {'name': '水电类 - 照明', 'priority': 'medium', 'description': '灯管损坏、开关失灵、灯不亮'},
            {'name': '水电类 - 插座', 'priority': 'high', 'description': '插座损坏、松动、无电'},
            {'name': '水电类 - 热水器', 'priority': 'medium', 'description': '热水器不工作、漏水、温度异常'},
            
            # 家具类
            {'name': '家具类 - 床铺', 'priority': 'medium', 'description': '床板松动、床架损坏、床垫问题'},
            {'name': '家具类 - 桌椅', 'priority': 'low', 'description': '书桌、椅子损坏、抽屉故障'},
            {'name': '家具类 - 衣柜', 'priority': 'low', 'description': '柜门脱落、锁具损坏、隔板问题'},
            {'name': '家具类 - 空调', 'priority': 'medium', 'description': '空调不制冷/制热、漏水、噪音大'},
            
            # 门窗类
            {'name': '门窗类 - 门锁', 'priority': 'high', 'description': '门锁损坏、钥匙丢失、无法开关'},
            {'name': '门窗类 - 门框', 'priority': 'medium', 'description': '门框变形、门关不严、门轴损坏'},
            {'name': '门窗类 - 窗户', 'priority': 'medium', 'description': '窗户关不严、窗框松动'},
            {'name': '门窗类 - 玻璃', 'priority': 'high', 'description': '玻璃破损、裂缝'},
            
            # 卫生间
            {'name': '卫生间 - 马桶', 'priority': 'high', 'description': '马桶堵塞、冲水故障、漏水'},
            {'name': '卫生间 - 下水道', 'priority': 'high', 'description': '下水道堵塞、反味、排水不畅'},
            {'name': '卫生间 - 淋浴', 'priority': 'medium', 'description': '花洒损坏、水温异常、水压不足'},
            {'name': '卫生间 - 洗手池', 'priority': 'medium', 'description': '洗手池堵塞、水龙头损坏'},
            
            # 网络通讯
            {'name': '网络类 - 网络故障', 'priority': 'high', 'description': '无法上网、网速慢、频繁断网'},
            {'name': '网络类 - 网口损坏', 'priority': 'medium', 'description': '网口松动、接触不良、指示灯不亮'},
            {'name': '网络类 - 路由器', 'priority': 'medium', 'description': 'WiFi信号弱、路由器故障'},
            
            # 墙面地面
            {'name': '墙面地面 - 墙面', 'priority': 'low', 'description': '墙面脱落、开裂、渗水'},
            {'name': '墙面地面 - 地板', 'priority': 'medium', 'description': '地板损坏、翘起、积水'},
            {'name': '墙面地面 - 天花板', 'priority': 'medium', 'description': '天花板漏水、脱落'},
            
            # 消防安全
            {'name': '消防安全 - 烟雾报警器', 'priority': 'high', 'description': '报警器故障、误报、不响应'},
            {'name': '消防安全 - 灭火器', 'priority': 'high', 'description': '灭火器过期、损坏、缺失'},
            
            # 其他设施
            {'name': '其他 - 窗帘', 'priority': 'low', 'description': '窗帘损坏、轨道故障'},
            {'name': '其他 - 晾衣架', 'priority': 'low', 'description': '晾衣架损坏、绳子断裂'},
            {'name': '其他 - 垃圾桶', 'priority': 'low', 'description': '垃圾桶损坏、缺失'},
            {'name': '其他 - 其他问题', 'priority': 'low', 'description': '其他未分类的报修问题'},
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
