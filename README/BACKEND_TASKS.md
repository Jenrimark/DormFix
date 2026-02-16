# DormFix 后端开发任务列表

按 COMPLETION_SUMMARY 中的「后端开发（Django）」拆分的可执行任务，便于逐项完成与核对。

---

## 1. 创建 Django 项目

| 任务 | 状态 | 说明 |
|-----|------|------|
| 使用 `django-admin startproject` 创建项目 | ✅ 已完成 | 项目名：`dormfix_backend` |
| 创建应用 `accounts`（用户） | ✅ 已完成 | `python manage.py startapp accounts` |
| 创建应用 `repairs`（报修） | ✅ 已完成 | `python manage.py startapp repairs` |
| 配置 `INSTALLED_APPS` | ✅ 已完成 | 已加入 rest_framework、corsheaders、accounts、repairs |
| 配置 `ROOT_URLCONF`、中间件 | ✅ 已完成 | 见 `dormfix_backend/settings.py` |

---

## 2. 配置数据库

| 任务 | 状态 | 说明 |
|-----|------|------|
| 开发环境使用 SQLite | ✅ 已完成 | `db.sqlite3`，运行 `migrate` 后自动生成 |
| 创建/初始化 SQLite 数据库文件 | ✅ 见下方 | 执行 `python manage.py migrate` 或 `./scripts/init_db.sh` |
| 生产环境可选 MySQL | 📋 可选 | 见 `scripts/create_mysql_db.sql` 与 `dormfix_backend/settings.py` 注释 |

**生成 SQLite 数据库文件：**
```bash
cd /Users/Jenrimark/Documents/CODE/DormFix
source venv/bin/activate
python manage.py migrate
# 生成文件：项目根目录下的 db.sqlite3
```

**若使用 MySQL：** 数据库名与项目名一致为 **DormFix**。先执行 `scripts/create_mysql_db.sql` 建库，再在 `settings.py` 中配置 `DATABASES['default']` 为 MySQL（`NAME`: `'DormFix'`）并运行 `migrate`。

---

## 3. 创建数据模型（5 张表）

| 表名 | 对应模型 | 状态 | 所在应用 |
|------|----------|------|----------|
| users | `accounts.User` | ✅ 已完成 | accounts |
| repair_types | `repairs.RepairType` | ✅ 已完成 | repairs |
| work_orders | `repairs.WorkOrder` | ✅ 已完成 | repairs |
| order_logs | `repairs.OrderLog` | ✅ 已完成 | repairs |
| comments | `repairs.Comment` | ✅ 已完成 | repairs |

| 任务 | 状态 |
|-----|------|
| 自定义用户模型（角色、手机、宿舍号、头像等） | ✅ 已完成 |
| 故障类型表（名称、优先级、描述） | ✅ 已完成 |
| 工单表（编号、状态、紧急程度、描述、图片、维修员、时间、备注） | ✅ 已完成 |
| 工单日志表（操作人、动作、备注、时间） | ✅ 已完成 |
| 评价表（工单、评分、文字反馈） | ✅ 已完成 |
| 执行 `makemigrations` 与 `migrate` | 📋 待执行（见上方「创建数据库」） |

---

## 4. 实现用户认证

| 任务 | 状态 | 说明 |
|-----|------|------|
| `AUTH_USER_MODEL = 'accounts.User'` | ✅ 已完成 | settings.py |
| 注册 API（用户名、邮箱、密码、角色、手机、宿舍号） | ✅ 已完成 | accounts 视图/序列化 |
| 登录 API（Session） | ✅ 已完成 | POST `/api/accounts/users/login/` |
| 登出 API | ✅ 已完成 | POST `/api/accounts/users/logout/` |
| 获取当前用户 API（/me/） | ✅ 已完成 | GET `/api/accounts/users/me/` |
| 修改密码、更新个人信息 | ✅ 已完成 | 见 API_DOCUMENTATION.md |

---

## 5. 开发 RESTful API

| 模块 | 状态 | 说明 |
|------|------|------|
| 故障类型 CRUD | ✅ 已完成 | `/api/repairs/repair-types/` |
| 工单创建、列表、我的工单、待处理、派单、更新状态 | ✅ 已完成 | `/api/repairs/work-orders/` 及 action |
| 工单统计、类型分布 | ✅ 已完成 | statistics、type_distribution |
| 评价创建 | ✅ 已完成 | `/api/repairs/comments/` |
| 分页、排序、筛选 | ✅ 已完成 | DRF 配置与 ViewSet |
| 统一时间格式 | ✅ 已完成 | REST_FRAMEWORK['DATETIME_FORMAT'] |

---

## 6. 图片上传处理

| 任务 | 状态 | 说明 |
|-----|------|------|
| 配置 MEDIA_URL、MEDIA_ROOT | ✅ 已完成 | settings.py |
| 用户头像上传（ImageField） | ✅ 已完成 | accounts.User.avatar |
| 工单现场照片上传 | ✅ 已完成 | repairs.WorkOrder.img_proof |
| 开发环境提供静态访问（可选） | 📋 可选 | 见 urls.py 中 static(settings.MEDIA_URL, document_root=...) |

---

## 7. 权限控制（RBAC）

| 任务 | 状态 | 说明 |
|-----|------|------|
| 角色定义（学生/维修人员/管理员） | ✅ 已完成 | User.ROLE_CHOICES |
| 学生：仅看自己的工单、提交工单、评价 | ✅ 已完成 | 见 repairs/views 权限类或过滤 |
| 维修员：仅看分配给自己的工单、更新状态 | ✅ 已完成 | 同上 |
| 管理员：看全部、派单、统计、待处理列表 | ✅ 已完成 | is_admin() 判断 |
| Session 认证 + 未登录返回 401 | ✅ 已完成 | DRF SessionAuthentication |

---

## 数据库文件与脚本说明

- **SQLite（默认）**  
  - 数据库文件：项目根目录下 **`db.sqlite3`**（执行 `migrate` 后自动创建）。  
  - 一键初始化（迁移 + 可选初始化数据）：  
    ```bash
    ./scripts/init_db.sh
    ```
    或手动：
    ```bash
    python manage.py migrate
    python manage.py init_data   # 若有该命令，用于创建测试账号与故障类型
    ```

- **MySQL（可选）**  
  - 建库脚本：**`scripts/create_mysql_db.sql`**（创建数据库 **DormFix**，与项目名一致）。  
  - 使用前需在 `dormfix_backend/settings.py` 中将 `DATABASES['default']` 改为 MySQL 配置，`NAME` 填 `'DormFix'`（可参考文件内注释）。

---

## 快速自检

```bash
# 1. 生成数据库文件（SQLite）
python manage.py migrate

# 2. 可选：创建测试数据
python manage.py init_data

# 3. 启动后端
python manage.py runserver
```

访问：  
- API：http://localhost:8000/api/  
- Admin：http://localhost:8000/admin/  

测试账号见 API_DOCUMENTATION.md。
