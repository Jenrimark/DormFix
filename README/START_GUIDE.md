# DormFix 启动指南

## 🚀 快速启动

### 方式一：分别启动前后端（推荐）

#### 1. 启动后端服务

```bash
# 在项目根目录
./start_backend.sh
```

后端服务将在 `http://localhost:8000` 启动

#### 2. 启动前端服务

```bash
# 打开新的终端窗口
cd frontend
./start.sh
```

前端服务将在 `http://localhost:8000` 启动（使用 Python HTTP 服务器）

**注意**: 如果端口冲突，可以修改前端启动脚本中的端口号

### 方式二：只启动后端（前端通过文件访问）

```bash
# 启动后端
./start_backend.sh

# 在浏览器中直接打开前端文件
open frontend/index.html
```

---

## 📍 访问地址

### 后端服务
- **API 基础地址**: http://localhost:8000/api/
- **Admin 后台**: http://localhost:8000/admin/
- **API 文档**: 查看 `API_DOCUMENTATION.md`

### 前端页面
- **首页**: http://localhost:8000/index.html
- **工单提交**: http://localhost:8000/pages/submit-order.html
- **管理仪表盘**: http://localhost:8000/pages/admin-dashboard.html
- **工单跟踪**: http://localhost:8000/pages/order-tracking.html

---

## 👤 测试账号

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 可以查看所有工单、派单、统计 |
| 维修员 | repairman1 | repair123 | 可以查看分配给自己的工单 |
| 学生 | student1 | student123 | 可以提交工单、查看自己的工单 |

---

## 🧪 测试流程

### 1. 学生提交工单

1. 使用 `student1 / student123` 登录
2. 访问工单提交页面
3. 填写故障信息
4. 提交工单

### 2. 管理员派单

1. 使用 `admin / admin123` 登录
2. 访问管理仪表盘
3. 查看待处理工单
4. 点击"派单"按钮
5. 选择维修员

### 3. 维修员处理

1. 使用 `repairman1 / repair123` 登录
2. 查看分配的工单
3. 更新工单状态（开始维修 → 完工）

### 4. 学生评价

1. 使用 `student1 / student123` 登录
2. 查看已完成的工单
3. 提交评价（评分 + 反馈）

---

## 🔧 API 测试

### 使用 curl 测试

```bash
# 1. 登录
curl -X POST http://localhost:8000/api/accounts/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"student123"}' \
  -c cookies.txt

# 2. 获取当前用户信息
curl -X GET http://localhost:8000/api/accounts/users/me/ \
  -b cookies.txt

# 3. 获取故障类型列表
curl -X GET http://localhost:8000/api/repairs/repair-types/ \
  -b cookies.txt

# 4. 创建工单
curl -X POST http://localhost:8000/api/repairs/work-orders/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "repair_type": 1,
    "priority": "high",
    "content": "测试工单：卫生间水龙头漏水"
  }'

# 5. 获取我的工单
curl -X GET http://localhost:8000/api/repairs/work-orders/my_orders/ \
  -b cookies.txt
```

### 使用浏览器测试

1. 打开浏览器开发者工具（F12）
2. 访问前端页面
3. 在 Console 中执行：

```javascript
// 登录
fetch('http://localhost:8000/api/accounts/users/login/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  credentials: 'include',
  body: JSON.stringify({
    username: 'student1',
    password: 'student123'
  })
}).then(r => r.json()).then(console.log);

// 获取当前用户
fetch('http://localhost:8000/api/accounts/users/me/', {
  credentials: 'include'
}).then(r => r.json()).then(console.log);
```

---

## 📊 查看数据

### Admin 后台

1. 访问 http://localhost:8000/admin/
2. 使用 `admin / admin123` 登录
3. 可以查看和管理：
   - 用户
   - 故障类型
   - 工单
   - 工单日志
   - 评价

### 数据库

```bash
# 进入 Django Shell
source venv/bin/activate
python manage.py shell

# 查询数据
from accounts.models import User
from repairs.models import WorkOrder

# 查看所有用户
User.objects.all()

# 查看所有工单
WorkOrder.objects.all()

# 查看待处理工单
WorkOrder.objects.filter(status=0)
```

---

## 🐛 故障排查

### 1. 后端启动失败

**问题**: `ModuleNotFoundError`

**解决**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 数据库错误

**问题**: `no such table`

**解决**:
```bash
python manage.py migrate
python manage.py init_data
```

### 3. 端口被占用

**问题**: `Address already in use`

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
python manage.py runserver 8001
```

### 4. CORS 错误

**问题**: 前端无法访问后端 API

**解决**: 检查 `settings.py` 中的 CORS 配置
```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

### 5. 静态文件 404

**问题**: CSS/JS 文件加载失败

**解决**: 使用 Python HTTP 服务器启动前端
```bash
cd frontend
python3 -m http.server 8000
```

---

## 📝 开发模式

### 前端开发

```bash
cd frontend
python3 -m http.server 8000
```

修改 HTML/CSS/JS 文件后，刷新浏览器即可看到效果

### 后端开发

```bash
source venv/bin/activate
python manage.py runserver
```

Django 会自动检测代码变化并重新加载

### 数据库修改

```bash
# 修改 models.py 后
python manage.py makemigrations
python manage.py migrate
```

---

## 🔄 重置数据

### 重置数据库

```bash
# 删除数据库文件
rm db.sqlite3

# 重新迁移
python manage.py migrate

# 重新初始化数据
python manage.py init_data
```

### 重置特定应用

```bash
# 删除迁移文件
rm accounts/migrations/0*.py
rm repairs/migrations/0*.py

# 重新生成迁移
python manage.py makemigrations
python manage.py migrate
```

---

## 📚 相关文档

- **API 文档**: `API_DOCUMENTATION.md`
- **后端文档**: `BACKEND_README.md`
- **前端文档**: `frontend/README.md`
- **项目总览**: `PROJECT_OVERVIEW.md`
- **完成总结**: `FINAL_SUMMARY.md`

---

## 💡 提示

1. **首次启动**: 确保已运行 `python manage.py init_data` 初始化测试数据
2. **开发调试**: 使用浏览器开发者工具查看网络请求和控制台日志
3. **API 测试**: 推荐使用 Postman 或 curl 进行 API 测试
4. **数据查看**: 使用 Admin 后台查看和管理数据
5. **日志查看**: 查看 `logs/django.log` 了解后端运行情况

---

## 🎉 开始使用

现在你可以开始使用 DormFix 系统了！

1. 启动后端服务
2. 启动前端服务（或直接打开 HTML 文件）
3. 使用测试账号登录
4. 体验完整的工单流转流程

祝你使用愉快！🏠✨
