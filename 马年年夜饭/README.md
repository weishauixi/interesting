# 马年春节祝福与年夜饭图片收集平台 🐴🧧

一个基于 Vue 3 + Supabase 的轻量级春节祝福和年夜饭照片收集平台，无需微信小程序，跨平台可用。

## 功能特性

✨ **祝福发送**
- 6种马年主题祝福模板（龙马精神、红红火火、金玉满堂等）
- 自定义祝福语和祝福对象
- 生成精美的祝福卡片
- 支持链接分享和图片保存

📸 **年夜饭收集**
- 简单的图片上传流程（支持1-3张）
- 拖拽上传支持
- 添加昵称和新年寄语
- 公开/私密选项

🖼️ **照片墙展示**
- 瀑布流布局展示所有年夜饭照片
- 大图预览功能
- 点赞和评论数据展示

📊 **数据统计**
- 实时显示祝福发送总数
- 年夜饭照片上传统计
- 参与人数统计

## 技术栈

- **前端**: Vue 3 + Vue Router + Vite
- **后端/存储**: Supabase (提供 PostgreSQL + 文件存储)
- **部署**: Vercel / Netlify (免费)

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置 Supabase

1. 访问 [Supabase官网](https://supabase.com/) 注册账号（推荐用 GitHub 登录）
2. 点击 "New Project" 创建新项目
3. 填写项目信息：
   - Name: `horse-year-greetings` (或其他名字)
   - Database Password: 设置一个强密码
   - Region: 选择离你最近的区域
4. 等待项目创建完成（约1-2分钟）

### 3. 创建数据库表

在 Supabase Dashboard 中：

#### 创建 greetings 表
进入 Table Editor -> New table，创建：
- Table name: `greetings`
- 添加列：
  - `template_id` (int8)
  - `message` (text)
  - `sender_name` (text)
  - `recipient_name` (text)
  - `background_style` (text)

#### 创建 photos 表
创建新表：
- Table name: `photos`
- 添加列：
  - `image_url` (text)
  - `image_path` (text)
  - `uploader_name` (text)
  - `message` (text)
  - `is_public` (bool) - 默认值: `true`

### 4. 创建 Storage Bucket

进入 Storage -> New bucket：
- Name: `dinner-photos`
- Public bucket: ✓ (勾选，设置为公开)

### 5. 获取 API 凭证

1. 在 Project Settings -> API 中找到：
   - Project URL
   - anon public key

2. 创建 `.env` 文件：
```bash
cp .env.example .env
```

3. 编辑 `.env` 文件，填入你的 Supabase 配置：
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

### 6. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000 查看效果

### 7. 构建生产版本

```bash
npm run build
```

构建产物在 `dist` 目录

## Supabase 数据结构

### greetings 表（祝福）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int8 | 主键（自动生成）|
| template_id | int8 | 模板ID (1-6) |
| message | text | 祝福语 |
| sender_name | text | 发送者昵称 |
| recipient_name | text | 祝福对象 |
| background_style | text | 背景样式 |
| created_at | timestamp | 创建时间（自动生成）|

### photos 表（年夜饭照片）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int8 | 主键（自动生成）|
| image_url | text | 图片URL |
| image_path | text | 存储路径 |
| uploader_name | text | 上传者昵称 |
| message | text | 新年寄语 |
| is_public | bool | 是否公开 |
| created_at | timestamp | 创建时间（自动生成）|

### dinner-photos Storage（图片存储）
- Bucket名称: `dinner-photos`
- 访问权限: Public

## 免费部署到云端 🚀

### 推荐：Cloudflare Pages（无限带宽）

查看详细部署指南：`CLOUDFLARE_DEPLOY.md`

#### 快速开始：

1. **推送到 GitHub**
```bash
git init
git add .
git commit -m "🐴 马年春节祝福平台"
git remote add origin https://github.com/YOUR_USERNAME/horse-year-greetings.git
git push -u origin main
```

2. **部署到 Cloudflare Pages**
   - 访问：https://pages.cloudflare.com/
   - 连接 GitHub 仓库
   - 构建设置：`npm run build`，输出目录：`dist`
   - 配置环境变量（在 Supabase 获取）

3. **完成！**
   - 获得免费域名：`https://your-project.pages.dev`
   - 全球 CDN 加速
   - 自动 HTTPS

---

### 备选：Netlify（功能丰富）

查看详细部署指南：`NETLIFY_DEPLOY.md`

#### 超简单拖拽部署：

1. **构建项目**
```bash
npm run build
```

2. **上传到 Netlify**
   - 访问：https://app.netlify.com/drop
   - 拖拽 `dist` 文件夹到页面
   - 完成！

---

## 部署平台对比

| 平台 | 带宽 | 国内速度 | 推荐度 |
|------|------|---------|--------|
| **Cloudflare Pages** | ✅ 无限 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Netlify** | 100GB/月 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Vercel | 100GB/月 | ⭐⭐⭐ | ⭐⭐⭐ |
| GitHub Pages | 100GB/月 | ⭐⭐ | ⭐⭐⭐ |

---

## 旧版部署到 Vercel

1. 安装 Vercel CLI：
```bash
npm install -g vercel
```

2. 在项目根目录运行：
```bash
vercel
```

3. 按提示操作，部署时会自动询问环境变量，填入你的 Supabase 配置

### 方法二：通过 GitHub

1. 将代码推送到 GitHub
2. 访问 [vercel.com](https://vercel.com) 并导入项目
3. 在项目设置中添加环境变量：
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`

### 自定义域名

在 Vercel 项目设置中可以添加自定义域名，或使用 Vercel 提供的免费域名（如 `your-project.vercel.app`）

## Supabase 免费额度

- **数据库**: 500MB 存储
- **文件存储**: 1GB 存储
- **带宽**: 2GB/月
- **请求**: 50,000/月

对于这个项目来说，免费额度完全够用！

## 项目结构

```
horse-year-greetings/
├── src/
│   ├── components/          # 公共组件
│   ├── views/              # 页面组件
│   │   ├── Home.vue        # 首页
│   │   ├── Greeting.vue    # 发送祝福页
│   │   ├── Upload.vue      # 上传年夜饭页
│   │   └── Gallery.vue     # 年夜饭照片墙
│   ├── router/             # 路由配置
│   ├── services/           # API 服务
│   │   └── supabase.js    # Supabase 封装
│   ├── styles/             # 样式文件
│   ├── App.vue             # 根组件
│   └── main.js             # 入口文件
├── public/                 # 静态资源
├── .env                    # 环境变量（本地开发）
├── .env.example            # 环境变量示例
├── index.html              # HTML 模板
├── vite.config.js          # Vite 配置
├── package.json            # 项目配置
└── README.md               # 项目说明
```

## 自定义修改

### 修改祝福模板

编辑 `src/views/Greeting.vue` 中的 `templates` 数组：

```javascript
const templates = [
  {
    id: 1,
    name: '龙马精神',
    emoji: '🐴',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  // 添加更多模板...
]
```

### 修改主题颜色

编辑 `src/styles/main.css` 中的 CSS 变量：

```css
:root {
  --primary-color: #e74c3c;
  --secondary-color: #f39c12;
  --accent-color: #c0392b;
  /* 修改为你喜欢的颜色 */
}
```

### 添加新页面

1. 在 `src/views/` 创建新组件
2. 在 `src/router/index.js` 添加路由

## 常见问题

### 1. 图片上传失败

- 检查 Supabase Storage bucket 是否创建成功
- 确认 bucket 设置为 Public
- 检查文件大小是否超过限制（默认 50MB）
- 查看浏览器控制台错误信息

### 2. 数据保存失败

- 检 Supabase 表是否已创建
- 确认 Row Level Security (RLS) 策略允许公开读写
- 查看浏览器控制台错误信息

### 3. RLS 策略设置（推荐）

为了安全，建议开启 RLS 并添加策略：

在 Supabase Dashboard -> Authentication -> Policies 中添加：

**greetings 表**:
```sql
-- 允许所有人读取
CREATE POLICY "Public read" ON greetings
FOR SELECT USING (true);

-- 允许所有人插入
CREATE POLICY "Public insert" ON greetings
FOR INSERT WITH CHECK (true);
```

**photos 表**:
```sql
-- 允许所有人读取公开照片
CREATE POLICY "Public read" ON photos
FOR SELECT USING (is_public = true);

-- 允许所有人插入
CREATE POLICY "Public insert" ON photos
FOR INSERT WITH CHECK (true);
```

### 4. Vercel 部署后环境变量不生效

- 确保环境变量名以 `VITE_` 开头
- 重新部署项目：
  ```bash
  vercel --prod
  ```

## 替代方案

如果 Supabase 在你所在的地区访问不稳定，可以考虑：

1. **Firebase** - Google 提供的 BaaS，但可能需要科学上网
2. **直接使用图床 + GitHub Issues** - 图片用 imgbb，数据存 GitHub
3. **自建后端** - 用 Node.js + Express + MongoDB/MySQL

## License

MIT

## 祝大家马年大吉！🎊

龙马精神迎新春，马到成功行大运！
