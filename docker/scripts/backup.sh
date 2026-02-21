#!/bin/bash

# DormFix 数据库备份脚本
# 使用方法: ./backup.sh

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 配置
BACKUP_DIR="../backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="dormfix_backup_${DATE}.sql"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 切换到 docker 目录
cd "$(dirname "$0")/.."

print_info "开始备份数据库..."

# 备份数据库
if docker compose exec -T db pg_dump -U dormfix dormfix > "${BACKUP_DIR}/${BACKUP_FILE}"; then
    print_info "数据库备份成功: ${BACKUP_FILE}"
    
    # 压缩备份文件
    gzip "${BACKUP_DIR}/${BACKUP_FILE}"
    print_info "备份文件已压缩: ${BACKUP_FILE}.gz"
    
    # 删除 7 天前的备份
    find "$BACKUP_DIR" -name "dormfix_backup_*.sql.gz" -mtime +7 -delete
    print_info "已清理 7 天前的旧备份"
    
    # 显示备份文件大小
    BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}.gz" | cut -f1)
    print_info "备份文件大小: ${BACKUP_SIZE}"
else
    print_error "数据库备份失败"
    exit 1
fi

print_info "备份完成！"
