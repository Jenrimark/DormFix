#!/bin/bash
echo "测试 my_orders API 接口"
echo "================================"

# 先登录获取 session
echo "1. 登录获取 session..."
curl -c cookies.txt -X POST http://127.0.0.1:8000/api/accounts/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"student123"}' \
  -s | python3 -m json.tool

echo -e "\n2. 调用 my_orders 接口..."
curl -b cookies.txt http://127.0.0.1:8000/api/repairs/work-orders/my_orders/ \
  -H "Content-Type: application/json" \
  -s -w "\n状态码: %{http_code}\n"

echo -e "\n================================"
rm -f cookies.txt
