# DormFix 本地 MySQL + Navicat 操作指南

按顺序完成：**Navicat 建库** → **本机安装 MySQL 驱动** → **Django 迁移与初始化** → **启动前后端**。

---

## 一、Navicat 操作（创建数据库）

### 1. 确保已有 MySQL 连接

- 打开 **Navicat**，左侧是否有 **localhost**（或你本机 MySQL）连接？
- 连接信息应为：
  - **主机**：`localhost`
  - **端口**：`3306`
  - **用户名**：`root`
  - **密码**：`root`（你之前说大概率是这个，不对就改成你的实际密码）
- 若没有该连接：左上角 **连接** → **MySQL** → 填上述信息 → 测试连接 → 确定。

### 2. 创建数据库 DormFix

**方式 A：用项目里的 SQL 脚本（推荐）**

1. 在 Navicat 里**选中你的 localhost 连接**（不要选具体数据库）。
2. 菜单栏 **文件** → **运行 SQL 文件**（或按说明的“打开并执行”）。
3. 选择项目里的文件：**`DormFix/scripts/create_mysql_db.sql`**。
4. 编码选 **UTF-8**，点击 **开始** 执行。
5. 执行成功后，左侧刷新，应能看到数据库 **`DormFix`**。

**方式 B：在 Navicat 里手动建库**

1. 在 **localhost** 连接上**右键** → **新建数据库**。
2. **数据库名** 填：**`DormFix`**（与项目名一致）。
3. **字符集** 选：**`utf8mb4`**。
4. **排序规则** 选：**`utf8mb4_unicode_ci`**。
5. 确定后，左侧会出现 **DormFix**。

到此步为止，Navicat 里已经有一个空的 **DormFix** 数据库，表由下面 Django 的 `migrate` 来创建。

---

## 二、本机安装 MySQL 客户端（便于安装 mysqlclient）

Django 通过 **mysqlclient** 连 MySQL，需要本机有 MySQL 的 C 库和 `mysql_config`（Navicat 不提供这些，需单独装）。

### macOS（推荐 Homebrew）

```bash
# 安装 MySQL 和 pkg-config（mysqlclient 编译需要）
brew install mysql pkg-config
```

若已装过 MySQL，可只装 pkg-config：

```bash
brew install pkg-config
```

### Windows

- 安装 [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) 或 [MySQL Installer](https://dev.mysql.com/downloads/installer/)（会带 C 库和头文件）。
- 安装时勾选 **Development Components** 或 **C Include/Lib**。
- 安装后把 MySQL 的 `bin` 加入系统 PATH（以便后续若有命令行工具可用）。

### 验证（可选）

在终端执行（仅 macOS/Linux，且 MySQL 在 PATH 里时）：

```bash
mysql_config --version
```

有输出即说明本机 MySQL 客户端可用，再装 Python 的 mysqlclient 会顺利很多。

---

## 三、项目配置确认

后端已按本地 MySQL 配置好，无需改代码，只需确认：

- **数据库名**：`DormFix`（与 Navicat 里一致）
- **用户**：`root`
- **密码**：默认 `root`；若你的 MySQL 密码不是 `root`，可：
  - 在项目根目录执行：`export DB_PASSWORD=你的密码`，再运行 Django；
  - 或直接改 `dormfix_backend/settings.py` 里 `PASSWORD` 为你的密码。

---

## 四、安装依赖并执行迁移

在项目根目录 **DormFix** 下执行（建议先激活虚拟环境）：

```bash
cd /Users/Jenrimark/Documents/CODE/DormFix
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py init_data
```

说明：

- **`pip install -r requirements.txt`**：会安装 **mysqlclient**，若本机已按上面装好 MySQL + pkg-config，一般能安装成功。
- **`migrate`**：在 **DormFix** 库里创建所有表（users、work_orders 等）。
- **`init_data`**：插入测试账号和故障类型等（若项目里有该命令）。

执行完后可在 **Navicat** 里打开 **DormFix**，刷新表列表，应能看到多张表。

---

## 五、启动后端与前端

### 1. 启动后端（Django）

```bash
cd /Users/Jenrimark/Documents/CODE/DormFix
source venv/bin/activate
python manage.py runserver
```

- 后端地址：**http://localhost:8000**
- API：**http://localhost:8000/api/**
- Admin：**http://localhost:8000/admin/**

### 2. 启动前端（二选一）

**方式 A：Vue3 + Vite（推荐，热更新）**

```bash
cd /Users/Jenrimark/Documents/CODE/DormFix/frontend-vue
npm install
npm run dev
```

- 前端地址：**http://localhost:5173**

**方式 B：静态前端**

```bash
cd /Users/Jenrimark/Documents/CODE/DormFix/frontend
python3 -m http.server 8080
```

- 前端地址：**http://localhost:8080/index.html**

---

## 六、测试账号（init_data 后可用）

| 角色   | 用户名      | 密码       |
|--------|-------------|------------|
| 管理员 | admin       | admin123   |
| 维修员 | repairman1  | repair123  |
| 学生   | student1    | student123 |

---

## 七、若密码不是 root

- **方式 1（推荐）**：在运行 Django 前设置环境变量：
  ```bash
  export DB_PASSWORD=你的MySQL密码
  python manage.py runserver
  ```
- **方式 2**：直接改 `dormfix_backend/settings.py` 里：
  ```python
  'PASSWORD': os.environ.get('DB_PASSWORD', 'root'),  # 把 'root' 改成你的密码
  ```

---

## 八、忘记 MySQL 密码怎么办

### 方案一：继续用 SQLite（零配置）

项目已支持「未配置 MySQL 时自动用 SQLite」。不建 `.env`、不填 `DB_PASSWORD`，直接运行即可，数据在项目根目录的 **`db.sqlite3`** 里。适合本地开发、演示，无需记 MySQL 密码。

### 方案二：重置 MySQL root 密码（macOS）

若 MySQL 是用 **Homebrew** 装的：

1. 停止 MySQL：
   ```bash
   brew services stop mysql
   ```
2. 免密启动（跳过权限）：
   ```bash
   mysqld_safe --skip-grant-tables &
   ```
3. 无密码登录并改密（把 `新密码` 换成你要设的密码）：
   ```bash
   mysql -u root
   # 在 MySQL 里执行：
   FLUSH PRIVILEGES;
   ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
   EXIT;
   ```
4. 关掉免密进程，正常启动：
   ```bash
   killall mysqld
   brew services start mysql
   ```
5. 在项目根目录建 **`.env`**，写：`DB_PASSWORD=新密码`。

若 MySQL 是 **官网 dmg 安装** 的：打开「系统偏好设置」→「MySQL」→ 有「Initialize Database」或文档里的重置说明，按官方步骤重置 root 密码。

### 方案三：用 Navicat 改密码（若还能连上）

若你还能用其他账号或「无密码」连上 localhost：在 Navicat 里右键该连接 → **编辑连接** → **高级**，或连上后在「用户」里找到 `root@localhost`，修改密码并保存。

---

## 九、相关文件速查

| 说明           | 路径 |
|----------------|------|
| MySQL 建库 SQL | `scripts/create_mysql_db.sql` |
| Django 数据库配置 | `dormfix_backend/settings.py`（DATABASES） |
| 后端任务与数据库说明 | `README/BACKEND_TASKS.md` |

按上述顺序：**Navicat 建库 DormFix** → **本机装 MySQL 客户端** → **pip install + migrate + init_data** → **runserver + 前端**，即可用原来的 MySQL 完整跑通前后端。
