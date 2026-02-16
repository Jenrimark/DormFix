# DormFix API 文档

## 基础信息

- **Base URL**: `http://localhost:8000/api`
- **认证方式**: Session Authentication
- **数据格式**: JSON

## 测试账号

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 可以查看所有工单、派单、统计 |
| 维修员 | repairman1 | repair123 | 可以查看分配给自己的工单 |
| 学生 | student1 | student123 | 可以提交工单、查看自己的工单 |

## API 端点

### 1. 用户认证 (accounts)

#### 1.1 用户注册
```http
POST /api/accounts/users/register/
Content-Type: application/json

{
  "username": "test_user",
  "email": "test@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "role": 1,
  "phone": "13800138000",
  "dorm_code": "北一-305"
}
```

**响应**:
```json
{
  "message": "注册成功",
  "user": {
    "id": 1,
    "username": "test_user",
    "email": "test@example.com",
    "role": 1,
    "role_display": "学生",
    "phone": "13800138000",
    "dorm_code": "北一-305",
    "avatar": null,
    "created_at": "2026-01-18 10:00:00"
  }
}
```

#### 1.2 用户登录
```http
POST /api/accounts/users/login/
Content-Type: application/json

{
  "username": "student1",
  "password": "student123"
}
```

**响应**:
```json
{
  "message": "登录成功",
  "user": {
    "id": 5,
    "username": "student1",
    "email": "student1@dormfix.com",
    "role": 1,
    "role_display": "学生",
    "phone": "13900000001",
    "dorm_code": "北一-305",
    "avatar": null,
    "created_at": "2026-01-18 09:00:00"
  }
}
```

#### 1.3 用户登出
```http
POST /api/accounts/users/logout/
```

**响应**:
```json
{
  "message": "登出成功"
}
```

#### 1.4 获取当前用户信息
```http
GET /api/accounts/users/me/
```

**响应**: 同登录响应中的 user 对象

#### 1.5 修改密码
```http
PUT /api/accounts/users/change_password/
Content-Type: application/json

{
  "old_password": "student123",
  "new_password": "newpass123",
  "new_password_confirm": "newpass123"
}
```

#### 1.6 更新个人信息
```http
PUT /api/accounts/users/update_profile/
Content-Type: application/json

{
  "phone": "13900000002",
  "email": "newemail@example.com"
}
```

---

### 2. 故障类型 (repair-types)

#### 2.1 获取故障类型列表
```http
GET /api/repairs/repair-types/
```

**响应**:
```json
[
  {
    "id": 1,
    "name": "水电类",
    "priority": "high",
    "priority_display": "高",
    "description": "漏水、断电、照明等问题",
    "created_at": "2026-01-18 09:00:00"
  },
  ...
]
```

#### 2.2 获取单个故障类型
```http
GET /api/repairs/repair-types/{id}/
```

---

### 3. 工单管理 (work-orders)

#### 3.1 创建工单（学生）
```http
POST /api/repairs/work-orders/
Content-Type: application/json

{
  "repair_type": 1,
  "priority": "high",
  "content": "卫生间水龙头漏水严重，地面积水",
  "img_proof": null
}
```

**响应**:
```json
{
  "id": 6,
  "order_sn": "20260118001",
  "user": 5,
  "user_info": {
    "id": 5,
    "username": "student1",
    "dorm_code": "北一-305"
  },
  "repair_type": 1,
  "repair_type_info": {
    "id": 1,
    "name": "水电类"
  },
  "status": 0,
  "status_display": "待审核",
  "priority": "high",
  "priority_display": "紧急",
  "content": "卫生间水龙头漏水严重，地面积水",
  "img_proof": null,
  "repairman": null,
  "repairman_info": null,
  "create_time": "2026-01-18 10:30:00",
  "finish_time": null,
  "remark": null,
  "logs": [
    {
      "id": 1,
      "action": "submit",
      "action_display": "提交",
      "operator_info": {...},
      "remark": "工单提交",
      "create_time": "2026-01-18 10:30:00"
    }
  ],
  "comment": null
}
```

#### 3.2 获取工单列表
```http
GET /api/repairs/work-orders/
```

**查询参数**:
- `page`: 页码（默认 1）
- `page_size`: 每页数量（默认 10）
- `search`: 搜索关键词（工单编号、内容、用户名）
- `ordering`: 排序字段（如 `-create_time`）

#### 3.3 获取我的工单
```http
GET /api/repairs/work-orders/my_orders/
```

#### 3.4 获取待处理工单（管理员）
```http
GET /api/repairs/work-orders/pending/
```

#### 3.5 派单（管理员）
```http
POST /api/repairs/work-orders/{id}/assign/
Content-Type: application/json

{
  "repairman_id": 2
}
```

**响应**:
```json
{
  "message": "派单成功",
  "order": {...}
}
```

#### 3.6 更新工单状态
```http
POST /api/repairs/work-orders/{id}/update_status/
Content-Type: application/json

{
  "status": 2,
  "remark": "开始维修"
}
```

**状态码**:
- `0`: 待审核
- `1`: 已派单
- `2`: 维修中
- `3`: 已完成
- `4`: 已取消

#### 3.7 工单统计（管理员）
```http
GET /api/repairs/work-orders/statistics/
```

**响应**:
```json
{
  "total": 100,
  "pending": 23,
  "assigned": 15,
  "in_progress": 47,
  "completed": 156,
  "cancelled": 5,
  "avg_response_time": 2.3
}
```

#### 3.8 故障类型分布（管理员）
```http
GET /api/repairs/work-orders/type_distribution/
```

**响应**:
```json
[
  {
    "repair_type__name": "水电类",
    "count": 45
  },
  {
    "repair_type__name": "家具类",
    "count": 28
  },
  ...
]
```

---

### 4. 评价管理 (comments)

#### 4.1 创建评价
```http
POST /api/repairs/comments/
Content-Type: application/json

{
  "work_order": 3,
  "score": 5,
  "feedback": "维修师傅很专业，服务态度好"
}
```

**响应**:
```json
{
  "id": 1,
  "work_order": 3,
  "score": 5,
  "feedback": "维修师傅很专业，服务态度好",
  "create_time": "2026-01-18 15:00:00"
}
```

#### 4.2 获取评价列表
```http
GET /api/repairs/comments/
```

---

## 权限说明

### 学生 (role=1)
- ✅ 创建工单
- ✅ 查看自己的工单
- ✅ 取消自己的工单
- ✅ 评价已完成的工单
- ❌ 查看其他人的工单
- ❌ 派单
- ❌ 查看统计数据

### 维修人员 (role=2)
- ✅ 查看分配给自己的工单
- ✅ 更新工单状态（开始维修、完工）
- ✅ 填写维修备注
- ❌ 创建工单
- ❌ 派单
- ❌ 查看统计数据

### 管理员 (role=3)
- ✅ 查看所有工单
- ✅ 审核工单
- ✅ 派单
- ✅ 查看统计数据
- ✅ 管理故障类型
- ✅ 管理用户

---

## 错误响应

### 400 Bad Request
```json
{
  "field_name": ["错误信息"]
}
```

### 401 Unauthorized
```json
{
  "detail": "身份认证信息未提供。"
}
```

### 403 Forbidden
```json
{
  "error": "权限不足"
}
```

### 404 Not Found
```json
{
  "detail": "未找到。"
}
```

---

## 测试示例

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

# 3. 创建工单
curl -X POST http://localhost:8000/api/repairs/work-orders/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "repair_type": 1,
    "priority": "high",
    "content": "测试工单"
  }'

# 4. 获取我的工单
curl -X GET http://localhost:8000/api/repairs/work-orders/my_orders/ \
  -b cookies.txt
```

### 使用 Postman 测试

1. 导入 API 端点
2. 先调用登录接口
3. Postman 会自动保存 Cookie
4. 后续请求会自动携带认证信息

---

## 前端集成示例

```javascript
// 登录
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/accounts/users/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // 重要：携带 Cookie
    body: JSON.stringify({ username, password })
  });
  return await response.json();
}

// 创建工单
async function createWorkOrder(data) {
  const response = await fetch('http://localhost:8000/api/repairs/work-orders/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data)
  });
  return await response.json();
}

// 获取工单列表
async function getWorkOrders() {
  const response = await fetch('http://localhost:8000/api/repairs/work-orders/my_orders/', {
    credentials: 'include'
  });
  return await response.json();
}
```

---

## 注意事项

1. **CORS**: 开发环境已配置允许所有来源，生产环境需要修改
2. **CSRF**: 使用 Session 认证时需要处理 CSRF Token
3. **文件上传**: 图片上传需要使用 `multipart/form-data`
4. **分页**: 列表接口默认分页，每页 10 条
5. **时间格式**: 统一使用 `YYYY-MM-DD HH:MM:SS` 格式

---

**DormFix API v1.0** - 让宿舍报修更简单 🏠✨
