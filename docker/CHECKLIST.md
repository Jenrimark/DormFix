# Docker 部署检查清单

## 部署前检查

### 环境准备
- [ ] 已安装 Docker (version >= 20.10)
- [ ] 已安装 Docker Compose (version >= 2.0)
- [ ] 服务器内存 >= 2GB
- [ ] 服务器磁盘空间 >= 10GB
- [ ] 已克隆项目代码

### 配置文件
- [ ] 已复制 `.env.example` 到 `.env`
- [ ] 已修改 `SECRET_KEY`（生产环境必须）
- [ ] 已设置强密码 `POSTGRES_PASSWORD`
- [ ] 已配置 `ALLOWED_HOSTS`
- [ ] 已配置 `CORS_ALLOWED_ORIGINS`
- [ ] 已设置 `DEBUG=False`（生产环境）

### 网络和域名
- [ ] 已配置域名 DNS 解析
- [ ] 已开放防火墙端口 80/443
- [ ] 已准备 SSL 证书（生产环境推荐）

---

## 部署步骤

### 1. 构建镜像
```bash
cd docker
docker compose build
```
- [ ] 后端镜像构建成功
- [ ] 前端镜像构建成功
- [ ] 无构建错误

### 2. 启动服务
```bash
docker compose up -d
```
- [ ] 数据库容器启动成功
- [ ] 后端容器启动成功
- [ ] 前端容器启动成功

### 3. 初始化数据库
```bash
docker compose exec backend python manage.py migrate
```
- [ ] 数据库迁移成功
- [ ] 无迁移错误

### 4. 创建管理员
```bash
docker compose exec backend python manage.py createsuperuser
```
- [ ] 超级用户创建成功
- [ ] 记录管理员账号密码

### 5. 收集静态文件
```bash
docker compose exec backend python manage.py collectstatic --noinput
```
- [ ] 静态文件收集成功

---

## 部署后测试

### 基础功能测试
- [ ] 前端页面可以访问 (http://localhost)
- [ ] 后端 API 可以访问 (http://localhost:8000/api)
- [ ] 管理后台可以访问 (http://localhost:8000/admin)
- [ ] 健康检查端点正常 (http://localhost:8000/api/health/)

### 用户功能测试
- [ ] 用户注册功能正常
- [ ] 用户登录功能正常
- [ ] 用户登出功能正常
- [ ] 密码重置功能正常

### 报修功能测试
- [ ] 学生可以提交报修
- [ ] 可以上传图片
- [ ] 维修员可以接单
- [ ] 维修员可以完成维修
- [ ] 管理员可以审核

### 管理功能测试
- [ ] 用户管理功能正常
- [ ] 工单管理功能正常
- [ ] 公告管理功能正常
- [ ] 操作日志功能正常

---

## 性能检查

### 响应时间
- [ ] 首页加载时间 < 2秒
- [ ] API 响应时间 < 500ms
- [ ] 图片上传成功

### 资源使用
```bash
docker stats
```
- [ ] 内存使用 < 80%
- [ ] CPU 使用正常
- [ ] 磁盘空间充足

---

## 安全检查

### 配置安全
- [ ] `DEBUG=False` (生产环境)
- [ ] `SECRET_KEY` 已修改
- [ ] 数据库密码强度足够
- [ ] 数据库端口未暴露到外网

### 网络安全
- [ ] 已配置 HTTPS (生产环境推荐)
- [ ] CORS 配置正确
- [ ] CSRF 保护启用
- [ ] 安全头配置正确

### 访问控制
- [ ] 管理后台需要登录
- [ ] API 需要认证
- [ ] 文件上传有大小限制

---

## 备份和监控

### 备份
- [ ] 已设置数据库自动备份
- [ ] 已测试备份恢复流程
- [ ] 备份文件存储在安全位置

### 监控
- [ ] 已配置日志收集
- [ ] 已设置健康检查
- [ ] 已配置告警通知（可选）

---

## 文档和交接

### 文档完整性
- [ ] 部署文档已更新
- [ ] 环境变量已记录
- [ ] 管理员账号已记录
- [ ] 域名和证书信息已记录

### 团队交接
- [ ] 已培训运维人员
- [ ] 已提供故障排查指南
- [ ] 已提供常用命令清单
- [ ] 已建立支持渠道

---

## 生产环境额外检查

### 高可用性
- [ ] 已配置负载均衡（如需要）
- [ ] 已配置数据库主从复制（如需要）
- [ ] 已配置自动重启策略

### 性能优化
- [ ] 已配置 CDN（如需要）
- [ ] 已配置缓存（Redis）（如需要）
- [ ] 已优化数据库索引

### 合规性
- [ ] 已配置日志审计
- [ ] 已配置数据加密
- [ ] 已通过安全扫描

---

## 常用命令速查

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启服务
docker compose restart

# 停止服务
docker compose down

# 备份数据库
./scripts/backup.sh

# 恢复数据库
./scripts/restore.sh backup.sql.gz

# 进入容器
docker compose exec backend bash
docker compose exec frontend sh
docker compose exec db psql -U dormfix dormfix
```

---

## 完成确认

部署完成后，请确认：

- [ ] 所有检查项都已完成
- [ ] 所有测试都已通过
- [ ] 备份策略已实施
- [ ] 监控已配置
- [ ] 文档已更新
- [ ] 团队已培训

**部署负责人签名**: _______________

**部署日期**: _______________

**备注**: _______________
