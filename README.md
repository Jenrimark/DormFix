# DormFix - 宿舍报修工单管理系统

**让宿舍报修更简单、更高效** 🏠✨

基于 Django + 前端（静态 HTML / Vue3+Vite）的宿舍报修工单系统，支持学生提交报修、维修员接单、管理员派单与数据统计。

---

## 🚀 快速开始

```bash
# 后端
cd DormFix && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver

# 前端（新终端）二选一：
cd frontend && python3 -m http.server 8080          # 静态前端
# 或
cd frontend-vue && npm install && npm run dev      # Vue3 前端
```

- 后端 API：http://localhost:8000/api/
- 静态前端：http://localhost:8080/index.html
- Vue 前端：http://localhost:5173/

测试账号：**admin / admin123**（管理员）、**student1 / student123**（学生）。

---

## 📚 文档

**所有 Markdown 文档已收纳在 [README/](README/) 文件夹中**，便于集中查看：

- [README/README.md](README/README.md) — **文档索引**（推荐先看）
- [README/项目说明.md](README/项目说明.md) — 完整项目说明
- [README/API_DOCUMENTATION.md](README/API_DOCUMENTATION.md) — API 文档
- [README/BACKEND_TASKS.md](README/BACKEND_TASKS.md) — 后端任务与数据库
- 更多见 [README/](README/) 内列表

---

DormFix © 2026 · 软件工程毕业设计
