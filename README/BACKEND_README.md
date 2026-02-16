# DormFix 后端开发文档

## 📋 项目信息

- **框架**: Django 4.2.9 + Django REST Framework 3.14.0
- **数据库**: SQLite (开发) / MySQL (生产)
- **Python 版本**: 3.9+
- **认证方式**: Session Authentication

## 🗂️ 项目结构

```
DormFix/
├── dormfix_backend/          # Django 项目配置
│   ├── settings.py           # 配置文件
│   ├── urls.py               # 主路由
│   └── wsgi.py               # WSGI 配置
├── accounts/                 # 用户认证应用
│   ├── models.py             # 用户模型
│   ├── serializers.py        # 序列化器
│   ├── views.py              # 视图
│   ├── admin.py              # Admin 配置
│   └── urls.py               # 路由
├── repairs/                  # 报修管理应用
│   ├── models.py             # 数据模型（工单、类型、日志、评价）
│   ├── serializers.py        # 序列化器
│   ├── views.py              # 视图
│   ├── permissions.py        # 权限类
│   ├── admin.py              # Admin 配置
│   ├── urls.py               # 路由
│   └── management/           # 管理命令
│       └── commands/
│           └── init_data.py  # 初始化数据
├── media/                    # 用户上传文件
├── logs/                     # 日志文件
├── venv/                     # 虚拟环境
├── manage.py                 # Django 管理脚本
├── requirements.txt          # 依赖包
├── start_backend.sh          # 启动脚本
└── API_DOCUMENTATION.md      # API 文档
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 确保已安装 Python 3.9+
python3 --version

# 创建虚拟环境（如果还没有）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库初始化

```bash
# 执行迁移
python manage.py migrate

# 初始化测试数据
python manage.py init_data
```

### 3. 启动服务

```bash
# 方式一：使用启动脚本（推荐）
./start_backend.sh

# 方式二：直接启动
python manage.py runserver
```

服务将在 `http://localhost:8000` 启动

### 4. 访问 Admin 后台

访问 `http://localhost:8000/admin/`

- 用户名: `admin`
- 密码: `admin123`

## 📊 数据模型

### 1. User (用户模型)

继承 Django 的 `AbstractUser`，添加了：

```python
- role: 角色（1:学生, 2:维修人员, 3:管理员）
- phone: 手机号
- dorm_code: 宿舍号
- avatar: 头像
```

### 2. RepairType (故障类型)

```python
- name: 类型名称
- priority: 优先级（low/medium/high）
- description: 描述
```

### 3. WorkOrder (工单)

```python
- order_sn: 工单编号（自动生成）
- user: 提交人（外键 -> User）
- repair_type: 故障类型（外键 -> RepairType）
- status: 状态（0-4）
- priority: 紧急程度（low/medium/high）
- content: 故障描述
- img_proof: 现场照片
- repairman: 维修人员（外键 -> User）
- create_time: 提交时间
- finish_time: 完工时间
- remark: 备注
```

### 4. OrderLog (工单日志)

```python
- work_order: 关联工单（外键 -> WorkOrder）
- operator: 操作人（外键 -> User）
- action: 动作（submit/review/assign/start/complete/cancel/comment）
- remark: 备注
- create_time: 操作时间
```

### 5. Comment (评价)

```python
- work_order: 关联工单（一对一 -> WorkOrder）
- score: 评分（1-5星）
- feedback: 文字反馈
- create_time: 评价时间
```

## 🔐 权限系统

### 权限类

- `IsStudent`: 学生权限
- `IsRepairman`: 维修人员权限
- `IsAdmin`: 管理员权限
- `IsOwnerOrAdmin`: 工单所有者或管理员权限

### 权限矩阵

| 操作 | 学生 | 维修员 | 管理员 |
|------|------|--------|--------|
| 创建工单 | ✅ | ❌ | ✅ |
| 查看自己的工单 | ✅ | ✅ | ✅ |
| 查看所有工单 | ❌ | ❌ | ✅ |
| 派单 | ❌ | ❌ | ✅ |
| 更新工单状态 | ❌ | ✅ | ✅ |
| 取消工单 | ✅ | ❌ | ✅ |
| 评价工单 | ✅ | ❌ | ✅ |
| 查看统计数据 | ❌ | ❌ | ✅ |

## 🛠️ API 端点

### 用户认证

- `POST /api/accounts/users/register/` - 用户注册
- `POST /api/accounts/users/login/` - 用户登录
- `POST /api/accounts/users/logout/` - 用户登出
- `GET /api/accounts/users/me/` - 获取当前用户信息
- `PUT /api/accounts/users/change_password/` - 修改密码
- `PUT /api/accounts/users/update_profile/` - 更新个人信息

### 故障类型

- `GET /api/repairs/repair-types/` - 获取故障类型列表
- `POST /api/repairs/repair-types/` - 创建故障类型（管理员）
- `GET /api/repairs/repair-types/{id}/` - 获取单个故障类型
- `PUT /api/repairs/repair-types/{id}/` - 更新故障类型（管理员）
- `DELETE /api/repairs/repair-types/{id}/` - 删除故障类型（管理员）

### 工单管理

- `GET /api/repairs/work-orders/` - 获取工单列表
- `POST /api/repairs/work-orders/` - 创建工单
- `GET /api/repairs/work-orders/{id}/` - 获取工单详情
- `PUT /api/repairs/work-orders/{id}/` - 更新工单
- `DELETE /api/repairs/work-orders/{id}/` - 删除工单
- `GET /api/repairs/work-orders/my_orders/` - 获取我的工单
- `GET /api/repairs/work-orders/pending/` - 获取待处理工单（管理员）
- `POST /api/repairs/work-orders/{id}/assign/` - 派单（管理员）
- `POST /api/repairs/work-orders/{id}/update_status/` - 更新工单状态
- `GET /api/repairs/work-orders/statistics/` - 工单统计（管理员）
- `GET /api/repairs/work-orders/type_distribution/` - 故障类型分布（管理员）

### 评价管理

- `GET /api/repairs/comments/` - 获取评价列表
- `POST /api/repairs/comments/` - 创建评价
- `GET /api/repairs/comments/{id}/` - 获取评价详情

详细 API 文档请查看 `API_DOCUMENTATION.md`

## 🧪 测试账号

| 角色 | 用户名 | 密码 | 宿舍号 |
|------|--------|------|--------|
| 管理员 | admin | admin123 | - |
| 维修员1 | repairman1 | repair123 | - |
| 维修员2 | repairman2 | repair123 | - |
| 维修员3 | repairman3 | repair123 | - |
| 学生1 | student1 | student123 | 北一-305 |
| 学生2 | student2 | student123 | 南二-208 |
| 学生3 | student3 | student123 | 东三-412 |
| 学生4 | student4 | student123 | 西四-501 |
| 学生5 | student5 | student123 | 北二-106 |

## 📝 开发指南

### 添加新的 API 端点

1. 在对应的 `views.py` 中添加视图方法
2. 在 `serializers.py` 中添加序列化器（如需要）
3. 在 `urls.py` 中注册路由
4. 更新 API 文档

### 添加新的数据模型

1. 在 `models.py` 中定义模型
2. 运行 `python manage.py makemigrations`
3. 运行 `python manage.py migrate`
4. 在 `admin.py` 中注册模型
5. 创建对应的序列化器和视图

### 自定义管理命令

在 `app/management/commands/` 目录下创建 Python 文件：

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '命令描述'
    
    def handle(self, *args, **options):
        # 命令逻辑
        pass
```

运行：`python manage.py command_name`

## 🔧 配置说明

### settings.py 关键配置

```python
# 自定义用户模型
AUTH_USER_MODEL = 'accounts.User'

# 媒体文件
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS 配置
CORS_ALLOW_ALL_ORIGINS = True  # 开发环境
CORS_ALLOW_CREDENTIALS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

## 🚀 部署指南

### 生产环境配置

1. **修改 settings.py**:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]
```

2. **配置 MySQL**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dormfix',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

3. **收集静态文件**:
```bash
python manage.py collectstatic
```

4. **使用 Gunicorn + Nginx**:
```bash
pip install gunicorn
gunicorn dormfix_backend.wsgi:application --bind 0.0.0.0:8000
```

## 📊 日志

日志文件位置：`logs/django.log`

日志级别：INFO

查看日志：
```bash
tail -f logs/django.log
```

## 🐛 常见问题

### 1. 迁移错误

```bash
# 删除所有迁移文件（保留 __init__.py）
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 重新生成迁移
python manage.py makemigrations
python manage.py migrate
```

### 2. 权限错误

确保用户已登录并具有相应权限。检查 `permissions.py` 中的权限类。

### 3. CORS 错误

检查 `settings.py` 中的 CORS 配置，确保前端域名在允许列表中。

## 📚 参考资料

- [Django 官方文档](https://docs.djangoproject.com/)
- [Django REST Framework 文档](https://www.django-rest-framework.org/)
- [Django 最佳实践](https://django-best-practices.readthedocs.io/)

---

**DormFix Backend** - 专业的宿舍报修管理系统后端 🏠✨
