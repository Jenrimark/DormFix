#!/bin/bash

# DormFix 自动 Git 上传和系统检查脚本
# Auto Git Upload and Crawl Check Script for DormFix

set -e

echo "🚀 DormFix 自动 Git 上传和系统检查脚本"
echo "========================================="
echo ""

# 终端输出颜色配置
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 配置项
COMMIT_MESSAGE="${1:-自动提交: $(date '+%Y-%m-%d %H:%M:%S')}"
BRANCH=$(git branch --show-current)

# 检查是否为 Git 仓库
check_git_repo() {
    if [ ! -d .git ]; then
        echo -e "${RED}✗${NC} 不是 Git 仓库"
        echo "   初始化仓库: git init"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} 检测到 Git 仓库"
}

# 检查 Git 状态
check_git_status() {
    echo ""
    echo "📊 检查 Git 状态..."
    
    if [ -z "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}⚠${NC} 没有需要提交的更改"
        return 1
    else
        echo -e "${GREEN}✓${NC} 检测到更改"
        git status --short
        return 0
    fi
}

# 添加并提交更改
git_commit() {
    echo ""
    echo "📝 添加更改到 Git..."
    git add .
    
    echo ""
    echo "💾 提交更改..."
    git commit -m "$COMMIT_MESSAGE"
    echo -e "${GREEN}✓${NC} 更改已提交"
}

# 推送到远程仓库
git_push() {
    echo ""
    echo "📤 推送到远程仓库..."
    
    # 检查远程仓库是否存在
    if ! git remote | grep -q origin; then
        echo -e "${RED}✗${NC} 未配置远程仓库 'origin'"
        echo "   添加远程仓库: git remote add origin <url>"
        exit 1
    fi
    
    # 推送到远程
    if git push origin "$BRANCH"; then
        echo -e "${GREEN}✓${NC} 成功推送到 origin/$BRANCH"
    else
        echo -e "${RED}✗${NC} 推送失败"
        echo "   可能需要先拉取: git pull origin $BRANCH"
        exit 1
    fi
}

# 检查后端服务是否运行
check_backend() {
    echo ""
    echo "🔍 检查后端服务..."
    
    if curl -s http://localhost:8000/api/ > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} 后端服务正在运行"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} 后端服务未运行"
        echo "   启动命令: python manage.py runserver"
        return 1
    fi
}

# 检查前端服务是否运行
check_frontend() {
    echo ""
    echo "🔍 检查前端服务..."
    
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} 前端服务正在运行"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} 前端服务未运行"
        echo "   启动命令: cd frontend-vue && npm run dev"
        return 1
    fi
}

# 检查数据库
check_database() {
    echo ""
    echo "🔍 检查数据库..."
    
    if [ -f db.sqlite3 ]; then
        DB_SIZE=$(du -h db.sqlite3 | cut -f1)
        echo -e "${GREEN}✓${NC} 数据库存在 (大小: $DB_SIZE)"
        
        # 检查数据库连接
        if python manage.py shell -c "from django.db import connection; connection.ensure_connection()" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} 数据库连接成功"
        else
            echo -e "${YELLOW}⚠${NC} 数据库连接失败"
        fi
    else
        echo -e "${YELLOW}⚠${NC} 未找到数据库文件"
        echo "   运行迁移: python manage.py migrate"
    fi
}

# 检查 API 端点
check_api_endpoints() {
    echo ""
    echo "🔍 检查 API 端点..."
    
    if ! check_backend > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠${NC} 后端未运行，跳过 API 检查"
        return 1
    fi
    
    # 测试关键端点
    ENDPOINTS=(
        "http://localhost:8000/api/accounts/register/"
        "http://localhost:8000/api/accounts/login/"
        "http://localhost:8000/api/repairs/"
        "http://localhost:8000/api/announcements/"
    )
    
    for endpoint in "${ENDPOINTS[@]}"; do
        if curl -s -o /dev/null -w "%{http_code}" "$endpoint" | grep -q "200\|405\|403"; then
            echo -e "${GREEN}✓${NC} $endpoint"
        else
            echo -e "${RED}✗${NC} $endpoint"
        fi
    done
}

# 检查日志
check_logs() {
    echo ""
    echo "📋 检查最近日志..."
    
    if [ -d logs ]; then
        LOG_COUNT=$(find logs -name "*.log" 2>/dev/null | wc -l)
        echo -e "${GREEN}✓${NC} 找到 $LOG_COUNT 个日志文件"
        
        # 显示最近的错误（如果有）
        if [ -f logs/error.log ]; then
            ERROR_COUNT=$(wc -l < logs/error.log)
            if [ "$ERROR_COUNT" -gt 0 ]; then
                echo -e "${YELLOW}⚠${NC} 发现 $ERROR_COUNT 条错误记录"
                echo "   最近 5 条错误:"
                tail -n 5 logs/error.log | sed 's/^/   /'
            else
                echo -e "${GREEN}✓${NC} 日志中无错误"
            fi
        fi
    else
        echo -e "${YELLOW}⚠${NC} 未找到日志目录"
    fi
}

# 运行 Django 系统检查
run_django_checks() {
    echo ""
    echo "🔍 运行 Django 系统检查..."
    
    if python manage.py check --deploy 2>&1 | grep -q "System check identified no issues"; then
        echo -e "${GREEN}✓${NC} Django 检查通过"
    else
        echo -e "${YELLOW}⚠${NC} Django 检查发现问题:"
        python manage.py check --deploy 2>&1 | sed 's/^/   /'
    fi
}

# 检查依赖
check_dependencies() {
    echo ""
    echo "🔍 检查 Python 依赖..."
    
    if [ -f requirements.txt ]; then
        echo -e "${GREEN}✓${NC} 找到 requirements.txt"
        
        # 检查虚拟环境是否激活
        if [ -n "$VIRTUAL_ENV" ]; then
            echo -e "${GREEN}✓${NC} 虚拟环境已激活: $VIRTUAL_ENV"
        else
            echo -e "${YELLOW}⚠${NC} 虚拟环境未激活"
            echo "   激活命令: source venv/bin/activate"
        fi
    else
        echo -e "${RED}✗${NC} 未找到 requirements.txt"
    fi
}

# 主执行函数
main() {
    echo "开始自动化检查..."
    echo ""
    
    # Git 操作
    echo -e "${BLUE}═══ Git 操作 ═══${NC}"
    check_git_repo
    
    if check_git_status; then
        git_commit
        git_push
    fi
    
    # 系统健康检查
    echo ""
    echo -e "${BLUE}═══ 系统健康检查 ═══${NC}"
    check_dependencies
    check_database
    run_django_checks
    
    # 服务状态检查
    echo ""
    echo -e "${BLUE}═══ 服务状态 ═══${NC}"
    BACKEND_RUNNING=false
    FRONTEND_RUNNING=false
    
    if check_backend; then
        BACKEND_RUNNING=true
    fi
    
    if check_frontend; then
        FRONTEND_RUNNING=true
    fi
    
    # API 检查（仅当后端运行时）
    if [ "$BACKEND_RUNNING" = true ]; then
        check_api_endpoints
    fi
    
    # 日志检查
    check_logs
    
    # 总结
    echo ""
    echo -e "${BLUE}═══ 总结 ═══${NC}"
    echo ""
    echo "Git 状态:"
    echo "  分支: $BRANCH"
    echo "  最后提交: $(git log -1 --pretty=format:'%h - %s (%cr)')"
    echo ""
    echo "服务状态:"
    echo "  后端:  $([ "$BACKEND_RUNNING" = true ] && echo -e "${GREEN}运行中${NC}" || echo -e "${RED}已停止${NC}")"
    echo "  前端:  $([ "$FRONTEND_RUNNING" = true ] && echo -e "${GREEN}运行中${NC}" || echo -e "${RED}已停止${NC}")"
    echo ""
    echo "✅ 脚本执行完成!"
    echo ""
    echo "下一步操作:"
    echo "  • 启动后端: python manage.py runserver"
    echo "  • 启动前端: cd frontend-vue && npm run dev"
    echo "  • 查看日志: tail -f logs/error.log"
    echo ""
}

# 运行主函数
main
