# DormFix - 宿舍报修工单管理系统

**让宿舍报修更简单、更高效** 🏠✨

基于 Django 的宿舍报修工单系统，支持学生提交报修、维修员接单、管理员派单与数据统计。

---

## 🚀 快速开始

### 数据库配置

项目支持 **SQLite**（默认）和 **MySQL** 两种数据库：

#### 方式一：使用 SQLite（推荐新手）
无需配置，开箱即用！系统会自动使用 `db.sqlite3` 文件。

#### 方式二：使用 MySQL
1. 创建 `.env` 文件（项目根目录）：
   ```bash
   DB_PASSWORD=你的MySQL密码
   ```

2. 创建数据库：
   ```sql
   CREATE DATABASE DormFix CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. 系统会自动检测 `.env` 中的 `DB_PASSWORD`，如果存在则使用 MySQL


### 启动项目

#### 方式一：手动启动（推荐新手）

```bash
# 1. 克隆项目
git clone https://github.com/Jenrimark/DormFix.git
cd DormFix

# 2. 创建虚拟环境并安装后端依赖
python3 -m venv venv
source venv/bin/activate         
venv\Scripts\activate
pip install -r requirements.txt

# 3. 初始化数据库
python manage.py migrate

# 4. 创建管理员账号（首次运行必须）
python manage.py createsuperuser
# 按提示输入用户名、邮箱（可选）、密码

# 5. 启动后端服务
python manage.py runserver

# 6. 前端设置（新开一个终端）
cd frontend-vue
npm install                       # 安装依赖
npm run dev                       # 启动前端开发服务器
```

#### 方式二：使用初始化脚本（快速）

```bash
# 1. 克隆项目
git clone https://github.com/Jenrimark/DormFix.git
cd DormFix

# 2. 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 运行数据库初始化脚本
bash scripts/init_db.sh
# 或
./scripts/init_db.sh

# 4. 创建管理员账号
python manage.py createsuperuser

# 5. 启动后端
./start_backend.sh
# 或
python manage.py runserver

# 6. 前端设置（新终端）
cd frontend-vue
npm install
npm run dev
```

#### 访问地址

- 后端 API：http://localhost:8000/api/
- Vue 前端：http://localhost:5173/
- Django Admin：http://localhost:8000/admin/

#### 首次使用

1. 使用 `createsuperuser` 创建的管理员账号登录
2. 在管理后台创建测试用户（学生、维修员）
3. 或使用 Django Admin 手动添加用户

### 数据库迁移说明

当你修改了模型（models.py）或拉取了新代码后，需要运行迁移：

```bash
# 查看迁移状态
python manage.py showmigrations

# 应用所有迁移
python manage.py migrate

# 如果你修改了模型，需要先生成迁移文件
python manage.py makemigrations
python manage.py migrate
```

---

## � 主要功能

- 🎓 **学生端**：在线提交报修、实时跟踪工单状态、上传现场照片
- 🔧 **维修员端**：接单池、我的工单、开始维修、完成维修（上传凭证）
- 👨‍💼 **管理员端**：工单审核、数据可视化仪表盘、智能派单、用户管理、公告管理、操作日志
- 📢 **系统公告**：管理员发布公告，首页展示最新通知
- 📊 **数据统计**：实时数据展示、工单分析、性能指标

## 🛠 技术栈

- **后端**：Django 4.2 + Django REST Framework + MySQL/SQLite
- **前端**：Vue 3 + Vite + Tailwind CSS + Pinia
- **其他**：Axios、Vue Router

---

DormFix © 2026 · 毕业设计
