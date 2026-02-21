#!/bin/bash

# DormFix 一键部署脚本
# 使用方法: ./deploy.sh [dev|prod]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查 Docker 环境
check_docker() {
    print_info "检查 Docker 环境..."
    
    if ! command_exists docker; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    print_info "Docker 环境检查通过"
}

# 检查环境变量文件
check_env() {
    print_info "检查环境变量文件..."
    
    if [ ! -f .env ]; then
        print_warn ".env 文件不存在，从模板创建..."
        cp .env.example .env
        print_warn "请编辑 .env 文件并设置正确的配置"
        read -p "按回车键继续..."
    fi
    
    print_info "环境变量文件检查完成"
}

# 构建镜像
build_images() {
    print_info "开始构建 Docker 镜像..."
    
    if [ "$1" = "prod" ]; then
        docker compose -f docker-compose.prod.yml build
    else
        docker compose build
    fi
    
    print_info "镜像构建完成"
}

# 启动服务
start_services() {
    print_info "启动服务..."
    
    if [ "$1" = "prod" ]; then
        docker compose -f docker-compose.prod.yml up -d
    else
        docker compose up -d
    fi
    
    print_info "等待服务启动..."
    sleep 10
}

# 运行数据库迁移
run_migrations() {
    print_info "运行数据库迁移..."
    
    if [ "$1" = "prod" ]; then
        docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
    else
        docker compose exec -T backend python manage.py migrate
    fi
    
    print_info "数据库迁移完成"
}

# 收集静态文件
collect_static() {
    print_info "收集静态文件..."
    
    if [ "$1" = "prod" ]; then
        docker compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput
    else
        docker compose exec -T backend python manage.py collectstatic --noinput
    fi
    
    print_info "静态文件收集完成"
}

# 创建超级用户
create_superuser() {
    print_info "是否需要创建超级用户？(y/n)"
    read -p "> " create_user
    
    if [ "$create_user" = "y" ] || [ "$create_user" = "Y" ]; then
        if [ "$1" = "prod" ]; then
            docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
        else
            docker compose exec backend python manage.py createsuperuser
        fi
    fi
}

# 显示服务状态
show_status() {
    print_info "服务状态："
    
    if [ "$1" = "prod" ]; then
        docker compose -f docker-compose.prod.yml ps
    else
        docker compose ps
    fi
}

# 显示访问信息
show_access_info() {
    echo ""
    print_info "========================================="
    print_info "部署完成！"
    print_info "========================================="
    echo ""
    print_info "访问地址："
    print_info "  前端:        http://localhost"
    print_info "  后端 API:    http://localhost:8000/api"
    print_info "  管理后台:    http://localhost:8000/admin"
    echo ""
    print_info "常用命令："
    print_info "  查看日志:    docker compose logs -f"
    print_info "  停止服务:    docker compose down"
    print_info "  重启服务:    docker compose restart"
    echo ""
}

# 主函数
main() {
    echo ""
    print_info "========================================="
    print_info "DormFix Docker 部署脚本"
    print_info "========================================="
    echo ""
    
    # 获取部署模式
    MODE=${1:-dev}
    
    if [ "$MODE" != "dev" ] && [ "$MODE" != "prod" ]; then
        print_error "无效的部署模式: $MODE"
        print_info "使用方法: ./deploy.sh [dev|prod]"
        exit 1
    fi
    
    print_info "部署模式: $MODE"
    echo ""
    
    # 切换到 docker 目录
    cd "$(dirname "$0")/.."
    
    # 执行部署步骤
    check_docker
    check_env
    build_images "$MODE"
    start_services "$MODE"
    run_migrations "$MODE"
    collect_static "$MODE"
    create_superuser "$MODE"
    show_status "$MODE"
    show_access_info
    
    print_info "部署完成！🎉"
}

# 运行主函数
main "$@"
