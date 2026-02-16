# 改用 MySQL 后启动前后端

按下面做一次，之后每次启动照「三、日常启动」即可。

---

## 一、改成用 MySQL（只需做一次）

1. **在 Navicat 里建好数据库**
   - 运行项目里的 **`scripts/create_mysql_db.sql`**，或手动建库 **`DormFix`**，字符集 `utf8mb4`。

2. **在项目根目录建 `.env` 文件**  
   （与 `manage.py` 同级，不要提交到 git）

   ```bash
   DB_PASSWORD=你的MySQL的root密码
   ```

   保存后，Django 会自动用 MySQL，不再用 SQLite。

---

## 二、首次用 MySQL 时做一次迁移与初始化

在项目根目录执行（先激活虚拟环境）：

```bash
cd /Users/Jenrimark/Documents/CODE/DormFix
source venv/bin/activate
python manage.py migrate
python manage.py init_data
```

---

## 三、日常启动（前后端）

### 终端 1：后端

```bash
cd /Users/Jenrimark/Documents/CODE/DormFix
./start_backend.sh
```

（脚本会自动读 `.env` 里的 `DB_PASSWORD`，用 MySQL，并执行迁移、启动 8000 端口。）

### 终端 2：前端（Vue）

```bash
cd /Users/Jenrimark/Documents/CODE/DormFix/frontend-vue
npm run dev
```

---

## 四、访问地址

| 服务       | 地址 |
|------------|------|
| 前端（Vue） | http://localhost:5173/ |
| 后端 API   | http://localhost:8000/api/ |
| Admin 后台 | http://localhost:8000/admin/ |

测试账号：**admin / admin123**、**student1 / student123**、**repairman1 / repair123**。

---

## 五、若仍用 SQLite（不配 MySQL）

- 不建 `.env`，或建了但不写 `DB_PASSWORD`。
- 直接运行 `./start_backend.sh`，会使用项目下的 **db.sqlite3**。
