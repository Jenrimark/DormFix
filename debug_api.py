#!/usr/bin/env python3
"""调试 my_orders API 接口"""

import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dormfix_backend.settings')
django.setup()

from repairs.models import WorkOrder
from repairs.serializers import WorkOrderSerializer
from accounts.models import User

print("=" * 50)
print("调试 WorkOrderSerializer")
print("=" * 50)

# 获取 student1（有工单的用户）
student = User.objects.get(username='student1')
print(f"\n测试用户: {student.username} (ID: {student.id})")

# 获取该学生的工单
orders = WorkOrder.objects.filter(user=student).select_related(
    'user', 'repairman', 'reviewer'
).prefetch_related('logs', 'comment')

print(f"工单数量: {orders.count()}")

if orders.exists():
    print("\n尝试序列化第一条工单...")
    order = orders.first()
    print(f"工单ID: {order.id}, 工单号: {order.order_sn}")
    
    try:
        serializer = WorkOrderSerializer(order)
        data = serializer.data
        print("✅ 序列化成功")
        print(f"返回字段: {list(data.keys())}")
    except Exception as e:
        print(f"❌ 序列化失败: {e}")
        traceback.print_exc()
    
    print("\n尝试序列化所有工单（模拟 my_orders 接口）...")
    try:
        serializer = WorkOrderSerializer(orders, many=True)
        data = serializer.data
        print(f"✅ 批量序列化成功，返回 {len(data)} 条工单")
    except Exception as e:
        print(f"❌ 批量序列化失败: {e}")
        traceback.print_exc()

print("\n" + "=" * 50)
