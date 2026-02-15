# 🚀 Supabase 快速配置指南

## ✅ 文件已修复

`src/services/supabase.js` 已经修复完成，现在需要配置您的 Supabase 信息。

---

## 📋 第1步：获取 Supabase 配置信息

### 1.1 登录 Supabase

访问：https://supabase.com/dashboard

### 1.2 选择你的项目

如果还没有项目：
1. 点击 "New Project"
2. 填写项目名称：`horse-year-greetings`
3. 设置数据库密码（记住这个密码）
4. 选择区域：推荐选择 "Southeast Asia (Singapore)"
5. 点击 "Create new project"

### 1.3 获取配置信息

在项目页面：
1. 点击左侧菜单 **"Settings"**
2. 点击子菜单 **"API"**
3. 找到以下信息：

#### Project URL
```
https://xxxxxxxxxxxxx.supabase.co
```

#### API Keys
找到 "Project API keys" 部分
复制 "anon public" 密钥
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ...
```

---

## 🔧 第2步：配置到项目中

### 2.1 打开配置文件

编辑文件：
```
C:\Users\王晋华\Desktop\新建文件夹\src\config\env.js
```

### 2.2 填入配置信息

将文件内容修改为：

```javascript
// src/config/env.js - Supabase 环境变量配置
module.exports = {
  // ✅ 替换为你的 Project URL（注意保留引号）
  SUPABASE_URL: 'https://xxxxxxxxxxxxx.supabase.co',

  // ✅ 替换为你的 anon public key（注意保留引号）
  SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ...'
}
```

**重要**：
- ✅ 保留单引号 `'`
- ✅ 复制完整的 URL 和密钥
- ✅ 不要有额外的空格或换行

### 2.3 保存文件

保存 `env.js` 文件。

---

## 🎯 第3步：创建数据库表（可选）

### 3.1 在 Supabase 控制台

1. 点击左侧 **"Table Editor"**

2. 创建表：

#### 表 1：greetings（祝福表）

点击 "New table"：
- **Name**: `greetings`
- **Columns**：
  ```sql
  id            int8          Primary Key
  template_id   int8
  message       text
  sender_name   text
  recipient_name text
  created_at     timestamptz
  ```

#### 表 2：photos（照片表）

点击 "New table"：
- **Name**: `photos`
- **Columns**:
  ```sql
  id            int8          Primary Key
  image_url     text
  image_path    text
  uploader_name text
  message       text
  is_public     bool
  created_at     timestamptz
  ```

---

## 🧪 第4步：测试连接

### 4.1 启动 Web 应用

```bash
# 在项目根目录
npm run dev
```

### 4.2 访问应用

打开浏览器访问：
```
http://localhost:3000
```

### 4.3 测试功能

1. ✅ 发送祝福功能
2. ✅ 上传照片功能
3. ✅ 查看统计数据

**如果正常**：配置成功！✅

**如果有错误**：检查配置信息和网络连接。

---

## 🔒 安全提示

### ⚠️ 重要提醒

**API 密钥安全**：
- ✅ 使用的是 `anon public` 密钥（可以公开）
- ⚠️ 不要使用 `service_role` 密钥（绝密！）
- ✅ 配置 Row Level Security (RLS) 规则

### 配置 RLS 规则（推荐）

在 Supabase 控制台：

1. 点击 **"Authentication"** → **"Policies"**
2. 选择 `greetings` 表
3. 添加策略：

```sql
-- 允许所有操作（开发阶段）
CREATE POLICY "Enable all access for greetings" ON greetings
FOR SELECT
USING true;

-- 或更严格的策略（生产环境）
CREATE POLICY "Users can insert their greetings" ON greetings
FOR INSERT
WITH CHECK (true);

CREATE POLICY "Users can view all greetings" ON greetings
FOR SELECT
USING (true);
```

同样为 `photos` 表添加策略。

---

## 📊 验证配置

### 检查清单

- [ ] `env.js` 文件已保存
- [ ] SUPABASE_URL 格式正确（https://...）
- [ ] SUPABASE_ANON_KEY 是完整的密钥
- [ ] 数据库表已创建
- [ ] RLS 策略已配置（可选）

### 测试结果

**成功的标志**：
```
✅ 数据库连接成功
✅ 可以保存祝福
✅ 可以上传照片
✅ 可以查询数据
✅ 统计功能正常
```

---

## 🎊 完成！

配置完成后，您的 Vue Web 应用就可以使用 Supabase 存储数据了！

**小程序版本**：
- 使用本地存储（wx.setStorageSync）
- 不需要配置 Supabase
- 直接使用 `马年新春小程序` 目录即可

---

**祝您使用愉快！** 🐴🧧🎊
