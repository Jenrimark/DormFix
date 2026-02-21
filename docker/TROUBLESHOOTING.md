# Docker 部署故障排查指南

## 常见问题和解决方案

### 1. 容器无法启动

**症状**: `docker compose up` 后容器立即退出

**排查步骤**:
```bash
# 查看容器状态
docker compose ps

# 查看详细日志
docker compose logs backend
docker compose logs frontend
docker compose logs db

# 检查容器退出代码
docker compose ps -a
```

**常见原因**:
- 环境变量配置错误
- 端口被占用
- 数据库连接失败

**解决方案**:
```bash
# 重新构建并启动
docker compose down
docker compose up -d --build --force-recreate
```

---

### 2. 数据库连接失败

**症状**: 后端日志显示 "could not connect to server"

**排查步骤**:
```bash
# 检查数据库容器状态
docker compose ps db

# 查看数据库日志
docker compose logs db

# 测试数据库连接
docker compose exec db psql -U dormfix -d dormfix -c "SELECT 1"
```

**解决方案**:
```bash
# 1. 确保数据库容器正在运行
docker compose up -d db

# 2. 等待数据库完全启动
sleep 10

# 3. 重启后端
docker compose restart backend
```

---

### 3. 静态文件 404

**症状**: 前端样式丢失，管理后台无样式

**解决方案**:
```bash
# 重新收集静态文件
docker compose exec backend python manage.py collectstatic --noinput --clear

# 检查静态文件卷
docker volume inspect docker_static_volume

# 重启 Nginx
docker compose restart frontend
```

---

### 4. 前端无法访问后端 API

**症状**: 浏览器控制台显示 CORS 错误或 502

**排查步骤**:
```bash
# 检查后端是否运行
docker compose ps backend

# 测试后端 API
curl http://localhost:8000/api/health/

# 检查 Nginx 配置
docker compose exec frontend cat /etc/nginx/conf.d/default.conf
```

**解决方案**:
```bash
# 1. 检查环境变量
docker compose exec backend env | grep CORS

# 2. 更新 CORS 配置
# 编辑 .env 文件
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1

# 3. 重启服务
docker compose restart backend frontend
```

---

### 5. 端口冲突

**症状**: "port is already allocated"

**排查步骤**:
```bash
# 查看端口占用
sudo lsof -i :80
sudo lsof -i :8000
sudo lsof -i :5432

# 或使用 netstat
netstat -tuln | grep -E '80|8000|5432'
```

**解决方案**:
```bash
# 方案 1: 停止占用端口的服务
sudo systemctl stop nginx  # 如果是 Nginx
sudo systemctl stop apache2  # 如果是 Apache

# 方案 2: 修改 docker-compose.yml 中的端口映射
# 将 "80:80" 改为 "8080:80"
```

---

### 6. 容器内存不足

**症状**: 容器频繁重启，日志显示 "Killed"

**排查步骤**:
```bash
# 查看容器资源使用
docker stats

# 查看系统内存
free -h
```

**解决方案**:
```bash
# 1. 增加 Docker 内存限制
# 编辑 docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G

# 2. 减少 Gunicorn workers
command: gunicorn ... --workers 2

# 3. 清理未使用的资源
docker system prune -a
```

---

### 7. 数据库迁移失败

**症状**: "django.db.utils.OperationalError"

**解决方案**:
```bash
# 1. 检查数据库是否可访问
docker compose exec backend python manage.py dbshell

# 2. 手动运行迁移
docker compose exec backend python manage.py migrate --fake-initial

# 3. 如果需要重置数据库
docker compose down -v
docker compose up -d
docker compose exec backend python manage.py migrate
```

---

### 8. 文件上传失败

**症状**: 上传图片时报错

**排查步骤**:
```bash
# 检查媒体文件卷
docker volume inspect docker_media_volume

# 检查目录权限
docker compose exec backend ls -la /app/media
```

**解决方案**:
```bash
# 创建媒体目录并设置权限
docker compose exec backend mkdir -p /app/media
docker compose exec backend chmod 755 /app/media
```

---

### 9. 前端构建失败

**症状**: "npm ERR!" 或构建超时

**解决方案**:
```bash
# 1. 清理 npm 缓存
docker compose exec frontend npm cache clean --force

# 2. 重新构建前端镜像
docker compose build --no-cache frontend

# 3. 增加构建超时时间
# 编辑 frontend.Dockerfile
RUN npm ci --timeout=600000
```

---

### 10. SSL/HTTPS 配置问题

**症状**: "ERR_SSL_PROTOCOL_ERROR"

**解决方案**:
```bash
# 1. 检查证书文件
ls -la docker/ssl/

# 2. 验证证书
openssl x509 -in docker/ssl/cert.pem -text -noout

# 3. 测试 SSL 配置
docker compose exec frontend nginx -t

# 4. 重新加载 Nginx
docker compose exec frontend nginx -s reload
```

---

## 日志分析

### 查看实时日志
```bash
# 所有服务
docker compose logs -f

# 特定服务
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db

# 最近 100 行
docker compose logs --tail=100 backend
```

### 导出日志
```bash
# 导出所有日志
docker compose logs > logs_$(date +%Y%m%d_%H%M%S).txt

# 导出特定时间段
docker compose logs --since 2024-01-01T00:00:00 > logs.txt
```

---

## 性能优化

### 1. 数据库优化
```bash
# 进入数据库
docker compose exec db psql -U dormfix dormfix

# 分析慢查询
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

# 创建索引
CREATE INDEX idx_workorder_status ON repairs_workorder(status);
```

### 2. 清理磁盘空间
```bash
# 清理未使用的镜像
docker image prune -a

# 清理未使用的卷
docker volume prune

# 清理所有未使用的资源
docker system prune -a --volumes
```

### 3. 监控资源使用
```bash
# 实时监控
docker stats

# 查看磁盘使用
docker system df
```

---

## 紧急恢复

### 完全重置
```bash
# 警告：这将删除所有数据！
docker compose down -v --rmi all
rm -rf ../staticfiles ../media
docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

### 从备份恢复
```bash
# 恢复数据库
./scripts/restore.sh ../backups/dormfix_backup_20240101.sql.gz

# 重启服务
docker compose restart
```

---

## 获取帮助

如果以上方法都无法解决问题：

1. 收集完整日志
```bash
docker compose logs > full_logs.txt
docker compose ps > containers_status.txt
docker system info > system_info.txt
```

2. 检查 GitHub Issues
3. 联系技术支持

---

## 预防措施

### 定期维护
```bash
# 每周备份数据库
./scripts/backup.sh

# 每月清理旧日志
find logs/ -name "*.log" -mtime +30 -delete

# 每月更新镜像
docker compose pull
docker compose up -d --build
```

### 监控检查清单
- [ ] 磁盘空间 > 20%
- [ ] 内存使用 < 80%
- [ ] 数据库连接正常
- [ ] 备份文件存在
- [ ] SSL 证书未过期
