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

```bash
# 后端
cd DormFix
source venv/bin/activate          # 激活虚拟环境
pip install -r requirements.txt   # 安装依赖
python manage.py migrate          # 应用数据库迁移
python manage.py runserver        # 启动后端服务

# 或使用启动脚本
./start_backend.sh

# 前端
cd frontend-vue
npm install                       # 安装依赖
npm run dev                       # 启动前端开发服务器
```

- 后端 API：http://localhost:8000/api/
- Vue 前端：http://localhost:5173/
- Django Admin：http://localhost:8000/admin/

测试账号：**admin / admin123**（管理员）、**student1 / student123**（学生）。

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
