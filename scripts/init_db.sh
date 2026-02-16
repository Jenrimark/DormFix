#!/bin/bash
# DormFix 数据库初始化脚本（SQLite）
# 在项目根目录执行：./scripts/init_db.sh 或 bash scripts/init_db.sh

set -e
cd "$(dirname "$0")/.."

echo "📁 项目目录: $(pwd)"

# 可选：激活虚拟环境（若存在）
if [ -d "venv" ]; then
  echo "🔧 激活虚拟环境..."
  source venv/bin/activate
fi

echo "📊 执行数据库迁移（生成 db.sqlite3）..."
python manage.py migrate

if python manage.py help | grep -q init_data; then
  echo "📦 初始化测试数据..."
  python manage.py init_data
else
  echo "ℹ️  未找到 init_data 命令，跳过。可手动创建超级用户: python manage.py createsuperuser"
fi

echo "✅ 数据库文件已就绪: $(pwd)/db.sqlite3"
echo "🚀 启动后端: python manage.py runserver"
