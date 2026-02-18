# 更新日志

## 2026-02-18 - 提交工单功能增强

### 新增功能

1. **故障类型下拉选择**
   - 添加了清晰的下拉框选择故障类型
   - 显示"请选择故障类型"提示文本
   - 必填字段标记（红色星号）

2. **紧急程度三级分类**
   - 不急：可以等待处理
   - 一般：尽快处理（默认选项）
   - 紧急：需要立即处理
   - 每个选项都有详细说明

3. **图片上传功能**
   - 支持从相册选择图片
   - 支持拍照上传（移动端）
   - 图片预览功能
   - 可删除已选择的图片
   - 文件类型验证（仅支持图片）
   - 文件大小限制（最大 5MB）
   - 支持 JPG、PNG 格式

### 技术实现

#### 前端改进
- 使用 FormData 支持文件上传
- 添加图片预览和删除功能
- 改进表单 UI，增加必填标记
- 优化下拉框选项说明文字
- 添加文件验证逻辑

#### 后端支持
- 数据库已有 `img_proof` 字段（ImageField）
- 使用数据库存储文件（DatabaseStorage）
- 支持 multipart/form-data 请求

#### API 更新
- `createWorkOrder` 函数支持 FormData
- 自动检测并设置正确的 Content-Type

### 数据库
- 无需新的迁移（img_proof 字段已存在）
- 使用 StoredFile 模型存储文件到数据库

### 用户体验改进
- 清晰的表单标签和说明
- 必填字段标记
- 实时字符计数（问题描述）
- 图片预览功能
- 友好的错误提示
- 响应式设计，移动端友好

### 文件说明
- `frontend-vue/src/views/SubmitOrderView.vue` - 提交工单页面
- `frontend-vue/src/api/index.js` - API 配置
- `repairs/models.py` - 数据库模型
- `repairs/serializers.py` - 序列化器
- `repairs/views.py` - 后端视图
