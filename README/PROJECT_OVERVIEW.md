# DormFix 宿舍报修工单系统 - 项目总览

## 📋 项目信息

- **项目名称**: DormFix - 基于 Django 的宿舍报修工单系统
- **项目类型**: 本科毕业设计
- **技术栈**: Django 4.x + MySQL 8.0 + HTML5 + Tailwind CSS + JavaScript
- **设计系统**: UI UX Pro Max

## 🎯 项目目标

构建一个高可用、易扩展的 B/S 架构宿舍报修系统，实现从"报修-派单-维修-评价"的全生命周期闭环管理。

## 📁 项目结构

```
DormFix/
├── frontend/                    # 前端页面（已完成）
│   ├── pages/                   # HTML 页面
│   │   ├── submit-order.html    # 工单提交表单
│   │   ├── admin-dashboard.html # 管理员仪表盘
│   │   └── order-tracking.html  # 工单状态跟踪
│   ├── js/                      # JavaScript 交互逻辑
│   ├── css/                     # 自定义样式
│   ├── images/                  # 图片资源
│   ├── index.html               # 首页
│   ├── start.sh                 # 快速启动脚本
│   └── README.md                # 前端文档
├── 文档材料/                     # 论文相关文档
│   ├── 详细设计.md               # 系统详细设计
│   ├── 开题报告.docx
│   └── 基于Django的宿舍报修工单系统的设计与实现.pptx
├── .kiro/                       # Kiro AI 配置
├── .shared/                     # UI UX Pro Max 设计系统
└── PROJECT_OVERVIEW.md          # 本文档
```

## 🎨 设计系统

### 配色方案
- **主色**: `#7C3AED` (紫色) - 专业、现代、科技感
- **辅助色**: `#A78BFA` (浅紫色)
- **CTA 按钮**: `#F97316` (橙色) - 高对比度，引导操作
- **背景**: `#FAF5FF` (浅紫背景)
- **文字**: `#4C1D95` (深紫色)

### 字体系统
- **标题**: Fira Code (等宽字体，适合数据展示)
- **正文**: Fira Sans (清晰易读，专业感)

### UI 风格
- Data-Dense Dashboard（数据密集型仪表板）
- 响应式设计（支持 375px / 768px / 1024px / 1440px）
- 平滑过渡动画（150-300ms）
- WCAG AA 无障碍访问标准

## 🗄️ 数据库设计

### 核心数据表

#### 1. 用户信息表 (Users)
```python
- id: 主键
- username: 用户名
- role: 角色（1:学生, 2:维修人员, 3:管理员）
- phone: 手机号
- dorm_code: 宿舍号
- avatar: 头像
```

#### 2. 报修工单表 (WorkOrder)
```python
- id: 主键
- order_sn: 工单编号（YYYYMMDD+随机码）
- user_id: 外键 -> Users
- type_id: 外键 -> RepairType
- status: 状态（0:待审核, 1:已派单, 2:维修中, 3:已完成, 4:已取消）
- content: 故障描述
- img_proof: 现场照片
- repairman_id: 外键 -> Users（维修员）
- priority: 紧急程度（low/medium/high）
- create_time: 提交时间
- finish_time: 完工时间
```

#### 3. 故障类型表 (RepairType)
```python
- id: 主键
- name: 类型名（水电类、家具类、门窗类、网络类、其他）
- priority: 优先级
```

#### 4. 工单日志表 (OrderLog)
```python
- id: 主键
- order_id: 外键 -> WorkOrder
- operator: 操作人
- action: 动作（提交、审核、派单、完工、评价）
- remark: 备注
- create_time: 操作时间
```

#### 5. 评价表 (Comment)
```python
- id: 主键
- order_id: 外键 -> WorkOrder
- score: 评分（1-5星）
- feedback: 文字反馈
- create_time: 评价时间
```

## 🔄 核心业务流程

### 流程一：学生报修
```
1. 学生登录系统
2. 进入"提交报修"页面
3. 填写表单（故障类型、描述、照片、紧急程度）
4. 提交 -> 后端生成 order_sn
5. 状态置为 0（待审核）
6. 写入 OrderLog
```

### 流程二：管理员派单
```
1. 管理员登录系统
2. 查看"待处理工单"列表
3. 点击"派单"按钮
4. 选择空闲维修员
5. 更新工单 status=1，写入 repairman_id
6. 写入 OrderLog（派单记录）
7. 通知维修员（可选）
```

### 流程三：维修闭环
```
1. 维修员登录系统
2. 查看"我的待办"
3. 点击"开始维修" -> status=2
4. 到达现场维修
5. 点击"完工" -> 填写备注 -> status=3
6. 写入 OrderLog（完工记录）
7. 通知学生评价
8. 学生提交评价 -> 写入 Comment 表
```

## ✅ 已完成功能

### 前端页面（100%）
- ✅ 首页（index.html）
- ✅ 工单提交表单（submit-order.html）
  - 表单验证
  - 图片上传预览
  - 实时字符计数
  - 紧急程度选择
- ✅ 管理员仪表盘（admin-dashboard.html）
  - KPI 卡片展示
  - ECharts 数据可视化
  - 工单列表
  - 派单功能
- ✅ 工单状态跟踪（order-tracking.html）
  - 状态筛选
  - 时间线展示
  - 评价功能
  - 联系维修员

### 交互逻辑（100%）
- ✅ 表单实时验证
- ✅ 图片上传和预览
- ✅ 图表自动响应式
- ✅ 模态框交互
- ✅ Toast 提示消息
- ✅ 平滑过渡动画

### 设计系统（100%）
- ✅ UI UX Pro Max 集成
- ✅ 响应式布局
- ✅ 无障碍访问
- ✅ 配色和字体系统

## 🚧 待开发功能

### 后端开发（Django）
- [ ] 搭建 Django 项目结构
- [ ] 配置 MySQL 数据库
- [ ] 创建数据模型（Models）
- [ ] 实现用户认证系统
- [ ] 开发 API 接口
  - [ ] 工单 CRUD
  - [ ] 派单接口
  - [ ] 状态更新接口
  - [ ] 评价接口
- [ ] 图片上传处理
- [ ] 权限控制（RBAC）

### 前后端集成
- [ ] 替换模拟数据为真实 API
- [ ] CSRF Token 保护
- [ ] 用户会话管理
- [ ] 错误处理和提示

### 功能增强
- [ ] 工单详情页面
- [ ] 维修员工作台
- [ ] 消息通知系统
- [ ] 数据导出功能
- [ ] 用户个人中心
- [ ] 系统设置页面

### 测试与部署
- [ ] 单元测试
- [ ] 功能测试
- [ ] 压力测试
- [ ] Nginx + uWSGI 部署
- [ ] 生产环境配置

## 🚀 快速开始

### 查看前端页面

```bash
# 方式一：使用启动脚本
cd frontend
./start.sh

# 方式二：直接启动 Python 服务器
cd frontend
python3 -m http.server 8000

# 然后访问
# http://localhost:8000/index.html
```

### 页面访问地址
- 首页: http://localhost:8000/index.html
- 工单提交: http://localhost:8000/pages/submit-order.html
- 管理仪表盘: http://localhost:8000/pages/admin-dashboard.html
- 工单跟踪: http://localhost:8000/pages/order-tracking.html

## 📝 论文要点

### 技术亮点
1. **MTV 架构**: Django 标准模式，前后端职责清晰
2. **状态机设计**: 工单流转的可视化展示
3. **数据可视化**: ECharts 图表展示关键指标
4. **响应式设计**: 移动优先，多端适配
5. **用户体验优化**: 
   - 表单实时验证
   - 加载状态反馈
   - 平滑过渡动画
6. **无障碍访问**: WCAG AA 标准实现
7. **权限控制**: RBAC 三级权限隔离

### 创新点
1. **工单流转可追溯**: OrderLog 表记录每个状态变化
2. **数据驱动决策**: 通过维修数据统计设施故障率
3. **UI/UX 专业化**: 基于 UI UX Pro Max 设计系统
4. **移动端优化**: 学生主要通过手机报修

## 📊 项目进度

- [x] 需求分析（100%）
- [x] 数据库设计（100%）
- [x] 前端页面开发（100%）
- [ ] 后端开发（0%）
- [ ] 前后端集成（0%）
- [ ] 测试与优化（0%）
- [ ] 部署上线（0%）

## 📞 下一步计划

1. **搭建 Django 后端**
   - 创建 Django 项目
   - 配置数据库连接
   - 创建数据模型

2. **实现核心 API**
   - 用户认证接口
   - 工单 CRUD 接口
   - 派单和状态更新接口

3. **前后端联调**
   - 替换模拟数据
   - 测试完整流程
   - 修复 Bug

4. **功能完善**
   - 添加通知系统
   - 实现数据导出
   - 优化性能

## 🎓 毕业论文章节建议

1. **绪论**
   - 研究背景和意义
   - 国内外研究现状
   - 研究内容和方法

2. **系统分析**
   - 需求分析
   - 可行性分析
   - 功能模块划分

3. **系统设计**
   - 总体架构设计
   - 数据库设计
   - 接口设计

4. **系统实现**
   - 开发环境搭建
   - 核心模块实现
   - 关键代码展示

5. **系统测试**
   - 测试方案
   - 测试用例
   - 测试结果分析

6. **总结与展望**
   - 工作总结
   - 不足与改进
   - 未来展望

---

**DormFix** - 让宿舍报修更简单 🏠✨
