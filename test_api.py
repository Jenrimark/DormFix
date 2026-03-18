#!/usr/bin/env python3
"""测试 my_orders API 接口"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dormfix_backend.settings')
django.setup()

from django.test import RequestFactory
from repairs.views import WorkOrderViewSet
from accounts.models import User

# 创建请求工厂
factory = RequestFactory()

# 获取 student1 用户 (有6个工单)
student = User.objects.get(username='student1')

if not student:
    print("❌ 没有找到学生用户")
    exit(1)

print(f"测试用户: {student.username} (角色: {student.get_role_display()})")
print("=" * 50)

# 创建模拟请求
request = factory.get('/api/repairs/work-orders/my_orders/')
request.user = student

# 调用视图
viewset = WorkOrderViewSet()
viewset.request = request
viewset.format_kwarg = None
viewset.action = 'my_orders'  # 设置 action 属性

try:
    response = viewset.my_orders(request)
    print(f"✅ API 响应状态码: {response.status_code}")
    print(f"✅ 返回数据类型: {type(response.data)}")
    
    if isinstance(response.data, dict):
        print(f"✅ 数据结构: {list(response.data.keys())}")
        if 'results' in response.data:
            print(f"✅ 工单数量: {len(response.data['results'])}")
            if response.data['results']:
                print("\n前3条工单:")
                for order in response.data['results'][:3]:
                    print(f"  - ID: {order.get('id')}, 工单号: {order.get('order_sn')}, 状态: {order.get('status_display')}")
        else:
            print(f"✅ 工单数量: {len(response.data)}")
    elif isinstance(response.data, list):
        print(f"✅ 工单数量: {len(response.data)}")
        if response.data:
            print("\n前3条工单:")
            for order in response.data[:3]:
                print(f"  - ID: {order.get('id')}, 工单号: {order.get('order_sn')}, 状态: {order.get('status_display')}")
    
except Exception as e:
    print(f"❌ API 调用失败: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50)
