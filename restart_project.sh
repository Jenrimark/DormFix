#!/bin/bash

echo "🔄 重启 DormFix 项目..."

# 停止后端
echo "⏹️  停止后端服务..."
pkill -f "manage.py runserver" 2>/dev/null

# 停止前端
echo "⏹️  停止前端服务..."
pkill -f "vite" 2>/dev/null

sleep 2

# 启动后端
echo "🚀 启动后端服务..."
./start_backend.sh &

sleep 3

# 启动前端
echo "🚀 启动前端服务..."
cd frontend-vue
npm run dev &

echo ""
echo "✅ 项目启动完成！"
echo ""
echo "📍 访问地址："
echo "   前端: http://localhost:5173"
echo "   后端: http://localhost:8000"
echo "   Admin: http://localhost:8000/admin"
echo ""
echo "👤 测试账号："
echo "   学生: student1 / student123"
echo "   维修员: repairman1 / repair123"
echo "   管理员: admin / admin123"
echo ""
