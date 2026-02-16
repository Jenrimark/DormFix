-- DormFix MySQL 数据库创建脚本（数据库名与项目名一致：DormFix）
-- 使用方式：mysql -u root -p < scripts/create_mysql_db.sql
-- 或在 MySQL 客户端中执行以下语句

CREATE DATABASE IF NOT EXISTS `DormFix`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 创建专用用户（可选，生产环境建议使用）
-- CREATE USER IF NOT EXISTS 'dormfix'@'localhost' IDENTIFIED BY '你的密码';
-- GRANT ALL PRIVILEGES ON `DormFix`.* TO 'dormfix'@'localhost';
-- FLUSH PRIVILEGES;

-- 使用该数据库
USE `DormFix`;

-- 表结构由 Django migrate 自动创建，无需在此建表。
-- 配置好 settings.py 中的 MySQL 后执行：
--   python manage.py migrate
--   python manage.py init_data
