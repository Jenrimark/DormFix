# DormFix 前端页面

基于 UI UX Pro Max 设计系统构建的宿舍报修工单系统前端页面。

## 📁 项目结构

```
frontend/
├── pages/              # HTML 页面
│   ├── submit-order.html       # 工单提交表单（学生端）
│   ├── admin-dashboard.html    # 管理员仪表盘
│   └── order-tracking.html     # 工单状态跟踪
├── js/                 # JavaScript 交互逻辑
│   ├── submit-order.js
│   ├── admin-dashboard.js
│   └── order-tracking.js
├── css/                # 自定义样式（预留）
└── images/             # 图片资源（预留）
```

## 🎨 设计系统

### 配色方案
- **主色**: `#7C3AED` (紫色) - 专业、现代
- **辅助色**: `#A78BFA` (浅紫色)
- **CTA按钮**: `#F97316` (橙色) - 高对比度
- **背景**: `#FAF5FF` (浅紫背景)
- **文字**: `#4C1D95` (深紫色)

### 字体
- **标题**: Fira Code (等宽字体，适合数据展示)
- **正文**: Fira Sans (清晰易读)

### UI 风格
- Data-Dense Dashboard（数据密集型仪表板）
- 响应式设计，支持移动端
- 平滑过渡动画（150-300ms）
- 无障碍访问支持

## 📄 页面说明

### 1. 工单提交表单 (submit-order.html)

**功能特性**:
- ✅ 自动填充宿舍号
- ✅ 故障类型选择（5种类型）
- ✅ 实时字符计数（最多500字）
- ✅ 手机号验证（11位）
- ✅ 图片上传（最多3张，单张5MB）
- ✅ 紧急程度选择（不急/一般/紧急）
- ✅ 表单验证和提交反馈

**使用场景**: 学生提交报修申请

**访问方式**:
```bash
open frontend/pages/submit-order.html
```

### 2. 管理员仪表盘 (admin-dashboard.html)

**功能特性**:
- ✅ 4个核心 KPI 卡片（待处理/处理中/本月完成/平均响应时间）
- ✅ 工单趋势图（ECharts 折线图）
- ✅ 故障类型分布饼图
- ✅ 待处理工单列表
- ✅ 派单功能
- ✅ 侧边栏导航

**使用场景**: 管理员监控系统运行状态、派单

**访问方式**:
```bash
open frontend/pages/admin-dashboard.html
```

### 3. 工单状态跟踪 (order-tracking.html)

**功能特性**:
- ✅ 工单状态筛选（全部/待审核/已派单/维修中/已完成）
- ✅ 时间线展示工单流转过程
- ✅ 实时状态更新（动画效果）
- ✅ 联系维修员功能
- ✅ 取消工单功能
- ✅ 评价服务功能（5星评分 + 文字反馈）

**使用场景**: 学生/维修员查看工单进度

**访问方式**:
```bash
open frontend/pages/order-tracking.html
```

## 🚀 快速开始

### 方式一：直接打开 HTML 文件

```bash
# macOS
open frontend/pages/submit-order.html
open frontend/pages/admin-dashboard.html
open frontend/pages/order-tracking.html

# Linux
xdg-open frontend/pages/submit-order.html

# Windows
start frontend/pages/submit-order.html
```

### 方式二：使用本地服务器（推荐）

```bash
# Python 3
cd frontend
python3 -m http.server 8000

# 然后访问
# http://localhost:8000/pages/submit-order.html
# http://localhost:8000/pages/admin-dashboard.html
# http://localhost:8000/pages/order-tracking.html
```

## 🎯 核心交互功能

### 工单提交表单
- 实时字符计数
- 手机号格式验证（失焦时触发）
- 图片上传预览和删除
- 紧急程度单选（带视觉反馈）
- 表单提交动画（按钮状态变化）

### 管理员仪表盘
- ECharts 图表自动响应式调整
- 派单按钮点击确认
- Toast 提示消息
- 表格行悬停高亮

### 工单跟踪
- 状态筛选切换
- 时间线动画（当前步骤脉冲效果）
- 评价模态框（星级评分交互）
- 工单卡片展开/收起

## 📱 响应式断点

页面已针对以下断点优化：
- **Mobile**: 375px
- **Tablet**: 768px
- **Desktop**: 1024px
- **Large Desktop**: 1440px

## ♿ 无障碍访问

- ✅ 所有表单输入都有 label
- ✅ 按钮有明确的文字说明
- ✅ 颜色对比度符合 WCAG AA 标准（4.5:1）
- ✅ 键盘导航支持
- ✅ Focus 状态可见
- ✅ 支持 prefers-reduced-motion

## 🔧 技术栈

- **HTML5**: 语义化标签
- **Tailwind CSS**: 通过 CDN 引入（生产环境建议本地构建）
- **JavaScript**: 原生 ES6+，无框架依赖
- **ECharts**: 数据可视化图表库
- **Google Fonts**: Fira Code + Fira Sans

## 📝 待办事项

### 与 Django 后端集成
- [ ] 替换模拟数据为真实 API 调用
- [ ] 添加 CSRF Token 保护
- [ ] 实现用户认证和权限控制
- [ ] 图片上传到服务器
- [ ] WebSocket 实时通知

### 功能增强
- [ ] 工单详情页面
- [ ] 维修员工作台
- [ ] 数据导出功能
- [ ] 消息通知中心
- [ ] 用户个人中心

### 性能优化
- [ ] 图片懒加载
- [ ] 代码分割
- [ ] 本地构建 Tailwind CSS（减小体积）
- [ ] Service Worker 离线支持

## 🎓 毕业论文要点

这些页面展示了以下技术点，可以在论文中重点描述：

1. **前端架构设计**: MTV 模式中的 Template 层实现
2. **响应式设计**: 移动优先的设计理念
3. **用户体验优化**: 
   - 表单实时验证
   - 加载状态反馈
   - 平滑过渡动画
4. **数据可视化**: ECharts 图表展示关键指标
5. **无障碍访问**: WCAG AA 标准实现
6. **状态机设计**: 工单流转的可视化展示

## 📞 联系方式

如有问题，请查看项目文档或联系开发团队。

---

**DormFix** - 让宿舍报修更简单 🏠✨
