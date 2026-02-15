# Netlify 部署指南 🚀

Netlify 是另一个优秀的免费部署平台，操作简单，功能强大！

## 📋 准备工作

1. GitHub 账号
2. Netlify 账号（免费注册）
3. 您的项目代码

---

## 方法一：通过 GitHub 部署（推荐）

### 第 1 步：推送到 GitHub

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "🐴 马年春节祝福平台"

# 连接 GitHub 仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/horse-year-greetings.git

# 推送代码
git push -u origin main
```

### 第 2 步：连接 Netlify

1. 访问：https://app.netlify.com/start
2. 点击 "Add new site" → "Import an existing project"
3. 选择 "GitHub" 并授权
4. 选择 `horse-year-greetings` 仓库

### 第 3 步：配置构建设置

在 Netlify 构建配置页面填写：

```
构建命令：npm run build
发布目录：dist
```

### 第 4 步：设置环境变量

1. 展开 "Show advanced"
2. 在 "Environment variables" 中添加：

```
VITE_SUPABASE_URL = https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY = your-anon-key
```

3. 点击 "Deploy site"

### 第 5 步：完成部署

等待 1-2 分钟，部署完成后您会得到：
```
https://your-site-name.netlify.app
```

---

## 方法二：拖拽部署（超简单）

### 第 1 步：构建项目

```bash
npm install
npm run build
```

### 第 2 步：上传

1. 访问：https://app.netlify.com/drop
2. 将整个 `dist` 文件夹拖拽到页面中
3. 等待上传完成 ✅

就这么简单！

---

## 方法三：使用 Netlify CLI

### 安装 Netlify CLI

```bash
npm install -g netlify-cli
```

### 登录

```bash
netlify login
```

### 部署

```bash
# 构建
npm run build

# 部署
netlify deploy --prod --dir=dist
```

---

## ⚙️ 配置自定义域名

### 使用 Netlify 子域名

1. 进入 Site settings → Domain management
2. 点击 "Add custom domain"
3. 输入您想要的名称，如：`horse-year`
4. 获得：`https://horse-year.netlify.app`

### 使用自己的域名

1. 在 Domain management 添加您的域名
2. 在域名 DNS 设置中添加 CNAME 记录：
   ```
   CNAME yourdomain.com -> your-site.netlify.app
   ```

---

## 📊 Netlify 免费额度

| 项目 | 免费额度 |
|------|---------|
| **带宽** | 100GB/月 |
| **构建时间** | 300分钟/月 |
| **站点数量** | 无限 |
| **团队成员** | 1人 |
| **自动部署** | ✅ 支持 |
| **CDN** | 全球 CDN |
| **SSL 证书** | ✅ 免费 |
| **表单处理** | 100条/月 |

---

## 🔄 自动部署

设置后，每次推送代码到 GitHub：

```bash
git add .
git commit -m "Update: 更新内容"
git push
```

Netlify 会自动：
1. 检测到更新
2. 运行 `npm run build`
3. 部署新版本

---

## 🔧 netlify.toml 配置文件

在项目根目录创建 `netlify.toml`：

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

---

## 📦 部署检查清单

部署前检查：
- ✅ `npm run build` 能成功运行
- ✅ `dist` 文件夹生成了 `index.html`
- ✅ 环境变量已正确配置
- ✅ 本地测试无错误

---

## 🆚 Netlify vs Cloudflare Pages

| 特性 | Netlify | Cloudflare Pages |
|------|---------|------------------|
| **带宽** | 100GB/月 | ✅ **无限** |
| **国内速度** | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **功能丰富度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **上手难度** | ⭐ 非常简单 | ⭐⭐ 简单 |
| **额外功能** | 表单/函数/身份认证 | 主要是托管 |

---

## 💡 推荐选择

### 选择 Netlify 如果：
- ✅ 您需要表单处理功能
- ✅ 您需要 Serverless Functions
- ✅ 您需要更多构建工具支持
- ✅ 您喜欢更丰富的功能

### 选择 Cloudflare Pages 如果：
- ✅ 您需要无限带宽
- ✅ 您希望国内访问更快
- ✅ 您已经有 Cloudflare 账号
- ✅ 您只需要简单的静态托管

---

## 🎉 快速开始

```bash
# 1. 构建
npm run build

# 2. 部署（二选一）
# 方式A：拖拽 dist 文件夹到 https://app.netlify.com/drop
# 方式B：使用 Git 集成自动部署
```

---

## 📞 帮助文档

- Netlify 文档：https://docs.netlify.com/
- 部署指南：https://docs.netlify.com/site-deploys/overview/
- 环境变量：https://docs.netlify.com/site-deploys/environment-variables/

祝您部署成功！🎊🐴
