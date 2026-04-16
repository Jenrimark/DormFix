# DormFix — 宿舍报修工单管理系统

> 基于 Django REST Framework + Vue 3 的前后端分离宿舍报修平台，支持学生提交报修、维修员接单处理、管理员审核派单、系统反馈与 AI 知识问答。

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
| marked | ^16.x | AI 回答 Markdown 渲染 |
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

### 评价系统

- 学生可对**已完成工单**提交 1-5 星评价与文字反馈
- 每个工单仅允许评价一次，防止重复提交
- 评价结果用于维修质量追踪与管理员绩效分析
- 评价信息在工单详情中可直接查看（学生端与维修员端）

### 反馈系统（系统反馈 + 回复通知）

- 用户可提交系统反馈（功能建议/使用问题/投诉/其他）
- 管理员在后台统一处理反馈（状态流转 + 回复）
- 用户可在“反馈记录”查看处理进度和管理员回复
- 管理员回复后自动触发站内通知与红点提示，避免漏看

### AI 知识问答

- 学生与维修员可通过聊天式界面提问（支持流式输出）
- 回答优先结合管理员维护的文字知识库（FAQ/SOP/规则）
- 当知识库覆盖不足时，AI 会给出通用建议并提示以规则为准
- 管理员可维护知识条目并查看问答日志，持续优化回答质量

### 三类角色功能

**学生端**
- 注册登录（用户名/邮箱，角色默认为学生）
- 提交报修工单（选择故障类型、填写描述、上传现场图片）
- 实时查看工单进度（状态、维修员信息、时间线）
- 工单完成后提交星级评价与文字反馈
- 在待审核/已派单阶段可主动取消工单
- AI 知识问答（聊天式界面，支持流式输出）

**维修员端**
- 查看接单池（所有 status=1 且未被接取的工单）
- 主动接单，系统记录接单时间
- 开始维修，系统记录开始时间
- 完成维修，上传维修凭证图片或填写维修说明
- AI 知识问答（结合管理员录入规则/FAQ）

**管理员端**
- 工单审核（通过/拒绝，拒绝必须填写原因）
- 手动派单（指定维修员）
- 用户管理（创建/编辑/删除/启用/禁用/重置密码/批量操作）
- 数据仪表盘（工单统计、故障类型分布、趋势折线图、维修员绩效雷达图）
- 系统公告发布与管理
- 反馈管理（处理系统反馈、回复用户、更新状态）
- 操作日志查看（支持按操作人、操作类型、时间范围筛选）
- 知识库管理（纯文字录入 FAQ / SOP / 规则，按角色控制可见范围）

---

## 数据库设计

系统包含报修主流程、反馈通知和知识问答等核心数据表，主要包括：

| 表名 | 说明 |
|------|------|
| `users` | 用户表，含 role（1学生/2维修员/3管理员）、is_active、dorm_code 等字段 |
| `work_orders` | 工单表，含 status、repair_type、repairman、review_remark 等字段 |
| `order_logs` | 工单操作日志，记录每次状态变更的操作人与备注 |
| `stored_files` | 图片二进制存储表，存 filename、mime_type、content |
| `operation_logs` | 系统操作审计日志，记录用户管理等关键操作 |
| `knowledge_items` | 知识条目表（FAQ/SOP/规则，支持按角色可见） |
| `qa_logs` | 知识问答日志（问题、回答、成功状态、错误信息） |

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
├── feedbacks/              # 系统反馈模块
├── notifications/          # 站内通知模块
├── knowledge_base/         # AI知识问答与知识库管理
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

# （可选）生成演示数据：基于内置 9 个账号自动造全流程数据
python manage.py seed_demo_data

# 创建管理员账号
python manage.py createsuperuser

# 启动后端
python manage.py runserver
```

### 环境变量配置（统一放 `.env`）

项目所有运行配置统一从根目录 `.env` 读取。可先复制模板：

```bash
cp .env.example .env
```

常用配置说明：

```env
# Django 基础
DJANGO_SECRET_KEY=replace-with-your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库（DB_PASSWORD 为空则用 SQLite）
DB_PASSWORD=
DB_NAME=DormFix
DB_USER=root
DB_HOST=localhost
DB_PORT=3306

# 知识问答（大模型）
LLM_API_KEY=
# OpenAI: https://api.openai.com/v1
# 阿里 DashScope(OpenAI兼容): https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
LLM_TIMEOUT_SECONDS=30
```

数据库切换规则：`DB_PASSWORD` 非空时自动切换为 MySQL，否则使用 SQLite。

### 前端

```bash
cd frontend-vue
npm install
npm run dev
```

### 内置账号与演示数据说明

系统预置了 9 个账号，并提供一键生成演示数据的命令，方便测试与答辩演示：

- 管理员：`admin`
- 维修员：`repairman1`、`repairman2`、`repairman3`
- 学生：`student1`、`student2`、`student3`、`student4`、`student5`

执行 `python manage.py seed_demo_data` 后，会自动生成：

- 工单：`30` 条（每个学生 6 条，覆盖：待审核 / 已派单 / 维修中 / 已完成已评价 / 已完成未评价 / 已取消）
- 评价：`5` 条（部分已完成工单带评价与评价日志）
- 系统反馈：`15` 条（覆盖新提交 / 处理中 / 已解决等状态）
- 通知：`10` 条（管理员回复反馈后触发的站内通知与红点数据）
- 知识条目：`12` 条（FAQ / 维修SOP / 规则，带“【演示】”前缀）
- 公告：`4` 条（演示用系统公告）
- 问答日志：`8` 条（学生/维修员的历史提问与回答）

> 说明：`seed_demo_data` 只使用上述 9 个账号，不会创建新用户；重复执行会清理旧的演示数据后重新生成，便于多次重置测试环境。

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
| 认证 | `POST /api/accounts/users/register/` | 用户注册 |
| 认证 | `POST /api/accounts/users/login/` | 用户登录 |
| 认证 | `POST /api/accounts/users/logout/` | 用户登出 |
| 工单 | `POST /api/repairs/work-orders/` | 提交报修工单 |
| 工单 | `GET /api/repairs/work-orders/my_orders/` | 查看我的工单 |
| 工单 | `POST /api/repairs/work-orders/{id}/review/` | 管理员审核工单 |
| 工单 | `POST /api/repairs/work-orders/{id}/assign/` | 管理员派单 |
| 工单 | `POST /api/repairs/work-orders/{id}/accept/` | 维修员接单 |
| 工单 | `POST /api/repairs/work-orders/{id}/start_repair/` | 维修员开始维修 |
| 工单 | `POST /api/repairs/work-orders/{id}/complete_repair/` | 维修员完成维修 |
| 反馈 | `POST /api/feedbacks/` | 提交系统反馈 |
| 反馈 | `GET /api/feedbacks/my/` | 查看我的反馈 |
| 知识问答 | `POST /api/knowledge/ask/` | 非流式问答 |
| 知识问答 | `POST /api/knowledge/ask_stream/` | 流式问答（SSE） |
| 知识库 | `GET/POST/PUT/DELETE /api/knowledge/` | 管理员维护文字知识条目 |
| 公告 | `GET /api/announcements/latest/` | 最新公告 |

---

## 设计亮点

- **无文件系统依赖**：图片存入数据库 `StoredFile` 表，部署到任何平台无需配置文件存储
- **数据库自动切换**：通过 `.env` 中 `DB_PASSWORD` 是否存在自动选择 SQLite / MySQL，开发生产无缝切换
- **全程操作审计**：用户管理、工单流转均写入操作日志，支持多维度筛选查询
- **状态机保护**：工单状态单向流转，后端严格校验每步操作的前置状态，防止越权操作
- **角色权限隔离**：学生只能看自己的工单，维修员只能操作分配给自己的工单，管理员专属接口均有 `IsAdmin` 权限校验

---

DormFix © 2026 · 毕业设计项目
