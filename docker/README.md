# DormFix Docker 部署完整指南

## 📋 目录结构

```
docker/
├── README.md                    # 本文件 - 完整部署指南
├── docker-compose.yml           # Docker Compose 配置
├── docker-compose.prod.yml      # 生产环境配置
├── backend.Dockerfile           # 后端 Dockerfile
├── frontend.Dockerfile          # 前端 Dockerfile
├── nginx.conf                   # Nginx 配置
├── .env.example                 # 环境变量示例
└── scripts/
    ├── init.sh                  # 初始化脚本
    ├── backup.sh                # 数据库备份脚本
    └── deploy.sh                # 一键部署脚本
```

---

## 🚀 快速开始（5分钟部署）

### 前置要求

1. **安装 Docker 和 Docker Compose**

**macOS:**
```bash
# 下载 Docker Desktop for Mac
# https://www.docker.com/products/docker-desktop

# 或使用 Homebrew
brew install --cask docker
```

**Ubuntu/Debian:**
```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER
newgrp docker
```

**Windows:**
```powershell
# 下载 Docker Desktop for Windows
# https://www.docker.com/products/docker-desktop
```

2. **验证安装**
```bash
docker --version
docker compose version
```

---

## 📦 部署步骤

### 步骤 1: 准备环境变量

```bash
# 进入 docker 目录
cd docker

# 复制环境变量模板
cp .env.example .env

# 编辑环境变量（重要！）
nano .env
```

修改以下关键配置：
```env
# Django 配置
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False

# 数据库配置
POSTGRES_DB=dormfix
POSTGRES_USER=dormfix
POSTGRES_PASSWORD=your-strong-password-here

# 前端配置
VITE_API_BASE_URL=http://localhost:8000/api
```

### 步骤 2: 构建并启动服务

```bash
# 开发环境（推荐先用这个测试）
docker compose up -d --build

# 或生产环境
docker compose -f docker-compose.prod.yml up -d --build
```

### 步骤 3: 初始化数据库

```bash
# 运行数据库迁移
docker compose exec backend python manage.py migrate

# 创建超级管理员
docker compose exec backend python manage.py createsuperuser

# 收集静态文件
docker compose exec backend python manage.py collectstatic --noinput
```

### 步骤 4: 访问应用

- **前端**: http://localhost
- **后端 API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

---

## 🛠️ 常用命令

### 服务管理

```bash
# 启动所有服务
docker compose up -d

# 停止所有服务
docker compose down

# 重启服务
docker compose restart

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### 数据库操作

```bash
# 进入数据库容器
docker compose exec db psql -U dormfix -d dormfix

# 备份数据库
docker compose exec db pg_dump -U dormfix dormfix > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
docker compose exec -T db psql -U dormfix dormfix < backup.sql

# 查看数据库大小
docker compose exec db psql -U dormfix -d dormfix -c "SELECT pg_size_pretty(pg_database_size('dormfix'));"
```

### 后端操作

```bash
# 进入后端容器
docker compose exec backend bash

# 运行 Django 命令
docker compose exec backend python manage.py <command>

# 创建新的迁移文件
docker compose exec backend python manage.py makemigrations

# 应用迁移
docker compose exec backend python manage.py migrate

# 创建超级用户
docker compose exec backend python manage.py createsuperuser

# Django Shell
docker compose exec backend python manage.py shell
```

### 前端操作

```bash
# 进入前端容器
docker compose exec frontend sh

# 重新构建前端
docker compose exec frontend npm run build

# 查看前端日志
docker compose logs -f frontend
```

### 清理和重置

```bash
# 停止并删除所有容器
docker compose down

# 删除所有容器和卷（警告：会删除数据库数据！）
docker compose down -v

# 删除所有镜像
docker compose down --rmi all

# 完全清理并重新开始
docker compose down -v --rmi all
docker compose up -d --build
```

---

## 🔧 高级配置

### 1. 使用自定义域名

编辑 `docker-compose.yml`，添加环境变量：

```yaml
environment:
  - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
  - CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. 配置 SSL/HTTPS

使用 Let's Encrypt 和 Certbot：

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

### 3. 性能优化

编辑 `docker-compose.yml`：

```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

### 4. 数据持久化

数据卷配置（已在 docker-compose.yml 中）：

```yaml
volumes:
  postgres_data:      # 数据库数据
  static_volume:      # 静态文件
  media_volume:       # 媒体文件
```

查看数据卷：
```bash
docker volume ls
docker volume inspect docker_postgres_data
```

---

## 📊 监控和日志

### 查看资源使用

```bash
# 查看容器资源使用
docker stats

# 查看特定容器
docker stats docker-backend-1
```

### 日志管理

```bash
# 实时查看所有日志
docker compose logs -f

# 查看最近 100 行日志
docker compose logs --tail=100

# 查看特定时间的日志
docker compose logs --since 2024-01-01T00:00:00

# 导出日志到文件
docker compose logs > logs_$(date +%Y%m%d_%H%M%S).txt
```

---

## 🐛 故障排查

### 问题 1: 容器无法启动

```bash
# 查看详细错误信息
docker compose logs backend

# 检查容器状态
docker compose ps

# 重新构建
docker compose up -d --build --force-recreate
```

### 问题 2: 数据库连接失败

```bash
# 检查数据库是否运行
docker compose ps db

# 查看数据库日志
docker compose logs db

# 测试数据库连接
docker compose exec backend python manage.py dbshell
```

### 问题 3: 静态文件 404

```bash
# 重新收集静态文件
docker compose exec backend python manage.py collectstatic --noinput --clear

# 检查静态文件卷
docker volume inspect docker_static_volume
```

### 问题 4: 前端无法访问后端

检查 CORS 配置：
```bash
# 查看后端环境变量
docker compose exec backend env | grep CORS

# 检查 Nginx 配置
docker compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### 问题 5: 端口冲突

```bash
# 查看端口占用
sudo lsof -i :80
sudo lsof -i :8000

# 修改 docker-compose.yml 中的端口映射
ports:
  - "8080:80"  # 改为 8080
```

---

## 🔐 安全最佳实践

### 1. 环境变量安全

```bash
# 不要提交 .env 文件到 Git
echo ".env" >> .gitignore

# 使用强密码
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
```

### 2. 数据库安全

```yaml
# 不要暴露数据库端口到外网
# 注释掉 docker-compose.yml 中的：
# ports:
#   - "5432:5432"
```

### 3. 定期更新

```bash
# 更新基础镜像
docker compose pull

# 重新构建
docker compose up -d --build
```

---

## 📦 备份和恢复

### 自动备份脚本

```bash
# 使用提供的备份脚本
chmod +x scripts/backup.sh
./scripts/backup.sh

# 设置定时备份（crontab）
crontab -e
# 添加：每天凌晨 2 点备份
0 2 * * * /path/to/docker/scripts/backup.sh
```

### 手动备份

```bash
# 备份数据库
docker compose exec db pg_dump -U dormfix dormfix > backup.sql

# 备份数据卷
docker run --rm -v docker_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_data_backup.tar.gz /data

# 备份整个项目
tar czf dormfix_backup_$(date +%Y%m%d).tar.gz ../DormFix
```

### 恢复数据

```bash
# 恢复数据库
docker compose exec -T db psql -U dormfix dormfix < backup.sql

# 恢复数据卷
docker run --rm -v docker_postgres_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/postgres_data_backup.tar.gz -C /
```

---

## 🚀 生产环境部署

### 1. 使用生产配置

```bash
# 使用生产环境配置文件
docker compose -f docker-compose.prod.yml up -d --build
```

### 2. 配置反向代理（推荐）

如果你有多个服务，建议使用 Nginx 作为反向代理：

```nginx
# /etc/nginx/sites-available/dormfix
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. 配置防火墙

```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 📈 性能优化建议

### 1. 数据库优化

```sql
-- 进入数据库
docker compose exec db psql -U dormfix dormfix

-- 创建索引
CREATE INDEX idx_workorder_status ON repairs_workorder(status);
CREATE INDEX idx_workorder_create_time ON repairs_workorder(create_time);

-- 分析表
ANALYZE repairs_workorder;
```

### 2. 缓存配置

添加 Redis 缓存（可选）：

```yaml
# 在 docker-compose.yml 中添加
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
```

### 3. 静态文件 CDN

使用 CDN 加速静态文件访问（生产环境推荐）。

---

## 🎯 一键部署脚本

使用提供的部署脚本：

```bash
# 赋予执行权限
chmod +x scripts/deploy.sh

# 运行部署
./scripts/deploy.sh

# 脚本会自动：
# 1. 检查 Docker 环境
# 2. 构建镜像
# 3. 启动服务
# 4. 运行迁移
# 5. 收集静态文件
# 6. 显示访问地址
```

---

## 📞 获取帮助

### 常用资源

- Docker 官方文档: https://docs.docker.com
- Docker Compose 文档: https://docs.docker.com/compose
- Django 部署指南: https://docs.djangoproject.com/en/4.2/howto/deployment

### 检查清单

部署前确认：
- [ ] 已修改 .env 文件中的敏感信息
- [ ] 已设置强密码
- [ ] 已配置正确的域名
- [ ] 已测试数据库连接
- [ ] 已备份重要数据
- [ ] 已配置防火墙规则
- [ ] 已设置 SSL 证书（生产环境）

---

## 🎉 完成！

现在你的 DormFix 应用已经通过 Docker 成功部署！

访问地址：
- 前端: http://localhost
- 后端: http://localhost:8000
- 管理后台: http://localhost:8000/admin

祝使用愉快！🚀
