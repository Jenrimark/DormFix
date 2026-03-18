#!/usr/bin/env python3
"""检查数据库中的工单数据"""

import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dormfix_backend.settings')
django.setup()

from repairs.models import WorkOrder
from accounts.models import User

print("=" * 50)
print("数据库检查报告")
print("=" * 50)

# 检查用户数量
user_count = User.objects.count()
print(f"\n用户总数: {user_count}")

# 显示所有用户
print("\n所有用户列表:")
for user in User.objects.all():
    print(f"  ID: {user.id}, 用户名: {user.username}, 角色: {user.get_role_display()}, 激活: {user.is_active}")

# 检查工单数量
order_count = WorkOrder.objects.count()
print(f"\n工单总数: {order_count}")

if order_count > 0:
    print("\n所有工单及其所属用户:")
    for order in WorkOrder.objects.all().order_by('-create_time'):
        print(f"  ID: {order.id}, 工单号: {order.order_sn}, 提交人ID: {order.user_id}, 提交人: {order.user.username if order.user else '未知'}, 状态: {order.get_status_display()}")
        print(f"    创建时间: {order.create_time}")
        print("-" * 40)
else:
    print("\n⚠️  数据库中没有工单数据！")
    print("\n可能的原因:")
    print("1. 数据库被重置或迁移")
    print("2. 前端提交工单时出错")
    print("3. 数据库文件被替换")

print("\n" + "=" * 50)
