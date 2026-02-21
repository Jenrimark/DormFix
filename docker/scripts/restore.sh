#!/bin/bash

# DormFix 数据库恢复脚本
# 使用方法: ./restore.sh <backup_file>

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查参数
if [ -z "$1" ]; then
    print_error "请指定备份文件"
    print_info "使用方法: ./restore.sh <backup_file>"
    exit 1
fi

BACKUP_FILE="$1"

# 检查备份文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    print_error "备份文件不存在: $BACKUP_FILE"
    exit 1
fi

# 切换到 docker 目录
cd "$(dirname "$0")/.."

print_warn "警告: 此操作将覆盖当前数据库！"
read -p "确定要继续吗？(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    print_info "操作已取消"
    exit 0
fi

print_info "开始恢复数据库..."

# 解压备份文件（如果是 .gz 格式）
if [[ "$BACKUP_FILE" == *.gz ]]; then
    print_info "解压备份文件..."
    gunzip -c "$BACKUP_FILE" | docker compose exec -T db psql -U dormfix dormfix
else
    docker compose exec -T db psql -U dormfix dormfix < "$BACKUP_FILE"
fi

print_info "数据库恢复完成！"
