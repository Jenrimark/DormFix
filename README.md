# DormFix — 宿舍报修工单管理系统

> 基于 Django REST Framework + Vue 3 的前后端分离宿舍报修平台，支持学生提交报修、维修员接单处理、管理员审核派单与数据可视化统计。

---

## 项目概述

DormFix 针对高校宿舍报修流程中信息不透明、流转不规范、进度难追踪等痛点而设计。系统将报修全流程数字化，通过严格的工单状态机约束业务流转，三类角色各司其职，操作全程留有日志可追溯。

---

## 技术架构

### 整体架构

系统采用**前后端分离**架构，前端 SPA 与后端 RESTful API 通过 HTTP/JSON 通信，身份认证基于 Django Session + Cookie 机制。

```
┌─────────────────────────────────────────────────────┐
│                     客户端浏览器                      │
│         Vue 3 SPA（PC / 移动响应式）                  │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / JSON / Session Cookie
┌──────────────────────▼──────────────────────────────┐
│                   后端服务（Django）                   │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐ │
│  │ accounts │  │ repairs  │  │   announcements    │ │
│  │ 用户认证  │  │ 工单业务  │  │     公告管理        │ │
│  └──────────┘  └──────────┘  └────────────────────┘ │
│              Django REST Framework                   │
│              Django ORM                              │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              数据库（MySQL / SQLite）                  │
│         图片文件以二进制存入 StoredFile 表              │
└─────────────────────────────────────────────────────┘
```

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.x | 运行环境 |
| Django | 4.2 | Web 框架 |
| Django REST Framework | 3.x | RESTful API 构建 |
| django-cors-headers | — | 跨域处理 |
| MySQL / SQLite | — | 数据持久化（自动切换） |
| SimpleUI | — | Django Admin 美化 |

**认证方案**：Django Session 认证，登录后服务端生成 Session ID 通过 Cookie 返回，相比 JWT 更安全（会话数据存于服务端，客户端无法篡改）。

**文件存储**：自定义 `DatabaseStorage` 后端，图片以二进制写入 `StoredFile` 表，无需额外文件服务器，部署更简单。

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | ^3.4.0 | 响应式 UI 框架（Composition API） |
| Vite | ^5.0.0 | 构建工具，极速热更新 |
| Vue Router | ^4.2.5 | 前端路由，基于角色跳转 |
| Pinia | ^2.1.7 | 全局状态管理 |
| pinia-plugin-persistedstate | ^3.2.3 | 状态持久化（刷新不丢失登录态） |
| Tailwind CSS | ^3.4.0 | 原子化样式 |
| Axios | ^1.6.2 | HTTP 请求封装 |
| Chart.js + vue-chartjs | ^4.5.1 | 数据可视化图表 |
| @vueuse/core | ^14.2.1 | 组合式工具函数 |

---

## 核心功能

### 工单状态机

工单生命周期由有限状态机严格管控，单向流转，防止数据不一致：

```
学生提交 → [待审核 status=0]
              ↓ 管理员审核通过        ↓ 管理员拒绝 / 学生取消
         [已派单 status=1]         [已取消 status=4]
              ↓ 维修员接单 + 开始维修  ↓ 学生取消
         [维修中 status=2]
              ↓ 维修员完成 + 上传凭证
         [已完成 status=3]
```

### 三类角色功能

**学生端**
- 注册登录（用户名/邮箱，角色默认为学生）
- 提交报修工单（选择故障类型、填写描述、上传现场图片）
- 实时查看工单进度（状态、维修员信息、时间线）
- 工单完成后提交星级评价与文字反馈
- 在待审核/已派单阶段可主动取消工单

**维修员端**
- 查看接单池（所有 status=1 且未被接取的工单）
- 主动接单，系统记录接单时间
- 开始维修，系统记录开始时间
- 完成维修，上传维修凭证图片或填写维修说明

**管理员端**
- 工单审核（通过/拒绝，拒绝必须填写原因）
- 手动派单（指定维修员）
- 用户管理（创建/编辑/删除/启用/禁用/重置密码/批量操作）
- 数据仪表盘（工单统计、故障类型分布、趋势折线图、维修员绩效雷达图）
- 系统公告发布与管理
- 操作日志查看（支持按操作人、操作类型、时间范围筛选）

---

## 数据库设计

系统共 5 张核心业务表：

| 表名 | 说明 |
|------|------|
| `users` | 用户表，含 role（1学生/2维修员/3管理员）、is_active、dorm_code 等字段 |
| `work_orders` | 工单表，含 status、repair_type、repairman、review_remark 等字段 |
| `order_logs` | 工单操作日志，记录每次状态变更的操作人与备注 |
| `stored_files` | 图片二进制存储表，存 filename、mime_type、content |
| `operation_logs` | 系统操作审计日志，记录用户管理等关键操作 |

---

## 项目结构

```
DormFix/
├── dormfix_backend/        # Django 项目配置
│   ├── settings.py         # 数据库自动切换、Session、CORS、日志配置
│   └── urls.py
├── accounts/               # 用户认证与管理模块
│   ├── models.py           # User、OperationLog
│   ├── views.py            # 注册、登录、用户 CRUD、批量操作
│   └── serializers.py
├── repairs/                # 工单业务模块
│   ├── models.py           # WorkOrder、RepairType、OrderLog
│   ├── views.py            # 工单 CRUD、审核、派单、接单、完工、统计
│   └── storage_db.py       # 自定义数据库文件存储后端
├── announcements/          # 公告模块
├── frontend-vue/           # Vue 3 前端
│   ├── src/views/          # 各角色页面（登录、提交报修、仪表盘等）
│   ├── src/components/     # 通用组件（图表、对话框、通知等）
│   ├── src/stores/         # Pinia 状态管理
│   └── src/api/            # Axios 请求封装
└── logs/                   # 运行日志
```

---

## 快速启动

### 环境要求

- Python 3.8+
- Node.js 18+

### 后端

```bash
# 克隆项目
git clone https://github.com/Jenrimark/DormFix.git
cd DormFix

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser

# 启动后端
python manage.py runserver
```

### 数据库切换（可选）

默认使用 SQLite，开箱即用。切换 MySQL 只需在项目根目录创建 `.env`：

```env
DB_PASSWORD=你的MySQL密码
DB_NAME=DormFix
DB_USER=root
DB_HOST=localhost
DB_PORT=3306
```

系统检测到 `DB_PASSWORD` 非空时自动切换为 MySQL。

### 前端

```bash
cd frontend-vue
npm install
npm run dev
```

### 访问地址

| 服务 | 地址 |
|------|------|
| Vue 前端 | http://localhost:5173 |
| 后端 API | http://localhost:8000/api/ |
| Django Admin | http://localhost:8000/admin/ |

---

## API 接口概览

| 模块 | 接口 | 说明 |
|------|------|------|
| 认证 | `POST /api/users/register/` | 用户注册 |
| 认证 | `POST /api/users/login/` | 用户登录 |
| 认证 | `POST /api/users/logout/` | 用户登出 |
| 工单 | `POST /api/work-orders/` | 提交报修工单 |
| 工单 | `GET /api/work-orders/my_orders/` | 学生查看自己的工单 |
| 工单 | `POST /api/work-orders/{id}/review/` | 管理员审核工单 |
| 工单 | `POST /api/work-orders/{id}/assign/` | 管理员派单 |
| 工单 | `POST /api/work-orders/{id}/accept/` | 维修员接单 |
| 工单 | `POST /api/work-orders/{id}/start_repair/` | 维修员开始维修 |
| 工单 | `POST /api/work-orders/{id}/complete_repair/` | 维修员完成维修 |
| 统计 | `GET /api/work-orders/statistics/` | 工单统计数据 |
| 统计 | `GET /api/work-orders/repairman_performance/` | 维修员绩效 |
| 用户 | `POST /api/users/{id}/toggle_status/` | 启用/禁用用户 |
| 用户 | `POST /api/users/batch_operation/` | 批量操作用户 |
| 日志 | `GET /api/operation-logs/` | 操作审计日志 |
| 公告 | `GET /api/announcements/latest/` | 最新公告（公开） |

---

## 设计亮点

- **无文件系统依赖**：图片存入数据库 `StoredFile` 表，部署到任何平台无需配置文件存储
- **数据库自动切换**：通过 `.env` 中 `DB_PASSWORD` 是否存在自动选择 SQLite / MySQL，开发生产无缝切换
- **全程操作审计**：用户管理、工单流转均写入操作日志，支持多维度筛选查询
- **状态机保护**：工单状态单向流转，后端严格校验每步操作的前置状态，防止越权操作
- **角色权限隔离**：学生只能看自己的工单，维修员只能操作分配给自己的工单，管理员专属接口均有 `IsAdmin` 权限校验

---

DormFix © 2026 · 毕业设计项目
