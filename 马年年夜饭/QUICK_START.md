# 🎊 马年新春祝福平台 - 快速开始

## ✅ 当前状态：可以立即使用！

项目已配置为**本地存储模式**，所有数据保存在浏览器中，**无需任何配置即可测试所有功能**！

---

## 🚀 立即体验

开发服务器已启动：**http://localhost:3002**

### ✨ 可以测试的功能

1. **🧧 发送祝福**
   - 访问 http://localhost:3002/greeting
   - 选择喜欢的模板
   - 填写祝福语
   - 点击"生成祝福卡片"
   - ✅ 祝福会立即保存到浏览器

2. **📸 上传年夜饭**
   - 访问 http://localhost:3002/upload
   - 选择图片文件
   - 填写昵称和寄语
   - 点击"上传照片"
   - ✅ 图片会保存到浏览器

3. **🖼️ 查看照片墙**
   - 访问 http://localhost:3002/gallery
   - 查看所有上传的年夜饭照片
   - 点击照片可以大图预览

4. **🏠 首页**
   - 访问 http://localhost:3002
   - 查看最新祝福和统计数据

---

## 📦 当前模式：本地存储

- 数据保存在浏览器的 `localStorage` 中
- 不需要任何后端服务
- 适合演示、测试和学习
- ⚠️ **注意**：清除浏览器数据会丢失所有内容

---

## ☁️ 切换到 Supabase（生产环境使用）

如果想永久保存数据并多人共享，可以切换到 Supabase：

### 方式一：自动切换（推荐）

1. 打开文件：`src/services/index.js`
2. 将第 3 行的 `true` 改为 `false`：
   ```javascript
   const USE_LOCAL_STORAGE = false
   ```
3. 按照 `SUPABASE_SETUP.md` 配置 Supabase
4. 重启开发服务器

### 方式二：使用 Supabase

1. **注册 Supabase**
   - 访问 https://supabase.com
   - 用 GitHub 账号登录
   - 创建免费项目

2. **创建数据库表**
   - 在 Table Editor 中创建 `greetings` 表
   - 在 Table Editor 中创建 `photos` 表
   - 在 Storage 中创建 `dinner-photos` bucket

3. **配置环境变量**
   - 创建 `.env` 文件
   - 填入 Supabase URL 和 API Key

详细步骤请查看 `SUPABASE_SETUP.md`

---

## 🎨 功能特点

### ✅ 已实现
- 🎨 精美的春节主题界面
- 🧧 6种马年祝福模板
- 📸 图片上传（支持拖拽）
- 🖼️ 瀑布流照片墙
- 📊 实时统计数据
- 📱 响应式设计（支持手机/电脑）
- 🎊 各种喜庆动画效果

### 🎯 数据存储

| 模式 | 数据保存 | 多人共享 | 配置难度 | 适用场景 |
|------|---------|---------|---------|---------|
| **本地存储** | 浏览器 | ❌ | ⭐ | 测试、演示 |
| **Supabase** | 云端 | ✅ | ⭐⭐⭐ | 生产环境 |

---

## 🔧 常见问题

### Q: 数据保存在哪里？
**A:** 当前使用本地存储模式，数据保存在您的浏览器中。

### Q: 如何清除测试数据？
**A:** 在浏览器控制台运行：
```javascript
localStorage.clear()
location.reload()
```

### Q: 想要多人共享数据怎么办？
**A:** 切换到 Supabase 模式，详细步骤见 `SUPABASE_SETUP.md`

### Q: 本地存储会占用空间吗？
**A:** localStorage 通常有 5-10MB 限制，对于测试足够了。

### Q: 图片可以上传多大的？
**A:** localStorage 模式建议上传小图（< 1MB），Supabase 模式支持最大 50MB。

---

## 📝 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建版本
npm preview
```

---

## 🎉 开始使用

1. 打开浏览器访问 http://localhost:3002
2. 点击"发送祝福"试试看！
3. 上传一张年夜饭照片
4. 在照片墙上查看效果

祝您使用愉快！🎊🐴
