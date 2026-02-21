# 🚀 DormFix Docker 快速开始

## 5 分钟部署指南

### 1. 安装 Docker

**macOS:**
```bash
brew install --cask docker
```

**Ubuntu:**
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

### 2. 配置环境变量

```bash
cd docker
cp .env.example .env
nano .env  # 修改密码和配置
```

### 3. 一键部署

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 4. 访问应用

- 前端: http://localhost
- 后端: http://localhost:8000
- 管理后台: http://localhost:8000/admin

## 常用命令

```bash
# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 备份数据库
./scripts/backup.sh
```

## 完整文档

查看 [README.md](README.md) 获取完整部署文档。
