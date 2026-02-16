#!/bin/bash

# DormFix 后端启动脚本（支持 MySQL：在项目根目录建 .env 写 DB_PASSWORD=你的密码 即可）

echo "🚀 启动 DormFix 后端服务..."
echo ""

# 加载 .env（若存在），使 DB_PASSWORD 生效、使用 MySQL
if [ -f .env ]; then
    set -a
    . .env
    set +a
    echo "📌 已加载 .env（使用 MySQL 数据库 DormFix）"
else
    echo "📌 未发现 .env，使用 SQLite（db.sqlite3）"
fi
echo ""

# 激活虚拟环境
source venv/bin/activate

# 执行迁移
echo "📊 执行数据库迁移..."
python manage.py migrate --noinput

echo ""
echo "✅ 后端服务准备就绪！"
echo ""
echo "📍 服务地址:"
echo "   - API: http://localhost:8000/api/"
echo "   - Admin: http://localhost:8000/admin/"
echo ""
echo "👤 测试账号:"
echo "   - 管理员: admin / admin123"
echo "   - 维修员: repairman1 / repair123"
echo "   - 学生: student1 / student123"
echo ""
echo "📖 API 文档: 查看 API_DOCUMENTATION.md"
echo ""
echo "按 Ctrl+C 停止服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 启动开发服务器
python manage.py runserver
