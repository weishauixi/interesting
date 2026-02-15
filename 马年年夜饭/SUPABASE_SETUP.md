# Supabase 快速设置指南 🚀

## 第一步：注册和创建项目

1. 访问 https://supabase.com
2. 点击 "Start your project"
3. 使用 GitHub 账号登录（推荐）
4. 点击 "New Project"

填写以下信息：
- **Name**: `horse-year-greetings` (或任意名称)
- **Database Password**: 设置一个强密码并记住它
- **Region**: 选择 `Southeast Asia (Singapore)`（如果你在中国）
- **Pricing Plan**: 选择 Free（免费版）

点击 "Create new project"，等待 1-2 分钟完成创建。

## 第二步：创建数据库表

### 创建 greetings 表

在左侧菜单找到 **Table Editor**，点击 **New table**：

填写以下信息：
- **Name**: `greetings`
- **Description**: `春节祝福表`

添加以下列：

| Column name | Type | Default | Description |
|-------------|------|---------|-------------|
| template_id | int8 | - | 模板ID |
| message | text | - | 祝福语 |
| sender_name | text | - | 发送者昵称 |
| recipient_name | text | - | 祝福对象 |
| background_style | text | - | 背景样式 |

点击 **Save** 创建表。

### 创建 photos 表

同样在 **Table Editor** 点击 **New table**：

填写以下信息：
- **Name**: `photos`
- **Description**: `年夜饭照片表`

添加以下列：

| Column name | Type | Default | Description |
|-------------|------|---------|-------------|
| image_url | text | - | 图片URL |
| image_path | text | - | 存储路径 |
| uploader_name | text | - | 上传者昵称 |
| message | text | - | 新年寄语 |
| is_public | bool | true | 是否公开 |

点击 **Save** 创建表。

## 第三步：创建存储 Bucket

1. 在左侧菜单找到 **Storage**
2. 点击 **New bucket**
3. 填写信息：
   - **Name**: `dinner-photos`
   - **Public bucket**: ✅ 勾选（非常重要！）
4. 点击 **Create bucket**

## 第四步：获取 API 凭证

1. 点击左侧的 **Settings** (齿轮图标)
2. 选择 **API**
3. 复制以下信息：
   - **Project URL**: 类似 `https://xxxxx.supabase.co`
   - **anon public key**: 一段很长的密钥

## 第五步：配置本地环境

1. 在项目根目录创建 `.env` 文件：
```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# 或直接创建
New-Item -Path .env -ItemType File
```

2. 编辑 `.env` 文件，填入你的凭证：
```
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

## 第六步：启动项目

```bash
npm run dev
```

访问 http://localhost:3000 查看效果！

## 可选：设置 RLS 策略（推荐）

为了安全，建议设置访问策略：

1. 在 **Authentication** -> **Policies** 中
2. 为 `greetings` 表添加：
   - `Enable read access to everyone`: 允许所有人读取
   - `Enable insert access to everyone`: 允许所有人插入

3. 为 `photos` 表添加：
   - `Enable read access to everyone`: 允许所有人读取
   - `Enable insert access to everyone`: 允许所有人插入

## 常见问题

### Q: Supabase 访问慢怎么办？
A: 可以尝试更换 Region，或使用 Cloudflare Workers 作为代理。

### Q: 图片上传失败？
A: 检查 Storage bucket 是否设置为 Public。

### Q: 数据保存失败？
A: 检查 RLS 策略是否允许公开访问，或者在开发阶段可以暂时关闭 RLS。

## 需要帮助？

- Supabase 文档: https://supabase.com/docs
- Vue 文档: https://vuejs.org
- Vite 文档: https://vitejs.dev
