# DormFix 前端 (Vue 3 + Vite)

基于 **Vue 3** + **Vite** 的响应式前端，支持**热更新（HMR）**，修改代码后浏览器自动刷新。

## 技术栈

- **Vue 3** - 组合式 API (Composition API)
- **Vite 5** - 构建与开发服务器，实时热更新
- **Vue Router 4** - 前端路由
- **Pinia** - 状态管理（用户信息）
- **Tailwind CSS 3** - 样式（沿用原设计：主色 #7C3AED、CTA #F97316）
- **Axios** - 请求封装，代理到 Django 后端

## 环境要求

- Node.js 18+
- 后端 Django 已启动在 `http://localhost:8000`

## 启动方式

```bash
# 进入前端目录
cd frontend-vue

# 安装依赖（首次）
npm install

# 开发模式（Vite 实时响应）
npm run dev
```

浏览器访问：**http://localhost:5173**

- 开发时 Vite 会把 `/api` 代理到 `http://localhost:8000`，无需单独配置跨域。
- 修改任意 `.vue` / `.js` 文件保存后，页面会**自动热更新**。

## 构建与预览

```bash
# 构建生产包
npm run build

# 本地预览构建结果
npm run preview
```

## 目录结构

```
frontend-vue/
├── index.html
├── package.json
├── vite.config.js      # 开发代理 /api -> localhost:8000
├── tailwind.config.js
├── postcss.config.js
└── src/
    ├── main.js
    ├── App.vue
    ├── style.css
    ├── api/            # 接口封装
    ├── router/         # 路由
    ├── stores/         # Pinia（用户状态）
    ├── components/     # 公共组件
    └── views/          # 页面
```

## 页面与路由

| 路径 | 说明 |
|------|------|
| `/` | 首页 |
| `/login` | 登录 |
| `/register` | 注册 |
| `/submit` | 提交报修工单 |
| `/orders` | 我的工单 |
| `/admin` | 管理仪表盘（管理员） |
| `/profile` | 个人中心 |
| `/settings` | 系统设置 |

## 测试账号

与后端一致：管理员 `admin` / `admin123`，维修员 `repairman1` / `repair123`，学生 `student1` / `student123`。
