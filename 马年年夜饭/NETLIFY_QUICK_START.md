# 🚀 Netlify 部署快速指南

## 方法一：拖拽部署（最简单⭐⭐⭐⭐⭐）

### 只需 3 步，1 分钟搞定！

#### 第 1 步：构建项目 ✅
```bash
npm run build
```
**已完成！** `dist` 文件夹已生成。

#### 第 2 步：访问 Netlify
打开浏览器访问：**https://app.netlify.com/drop**

#### 第 3 步：拖拽上传
1. 找到项目目录中的 `dist` 文件夹
2. 将整个 `dist` 文件夹**拖拽**到 Netlify 页面
3. 等待上传完成

#### 完成！🎉
您会得到一个免费域名：
```
https://amazing-mahatma-123456.netlify.app
```

---

## 方法二：通过 Git 部署（推荐⭐⭐⭐⭐⭐）

### 自动部署，推送代码自动更新！

#### 第 1 步：推送到 GitHub

```bash
# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "🐴 马年春节祝福平台"

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/horse-year-greetings.git

# 推送
git push -u origin main
```

#### 第 2 步：连接 Netlify

1. 访问：https://app.netlify.com/start
2. 点击 **"Add new site"** → **"Import an existing project"**
3. 选择 **"GitHub"** 并授权
4. 选择 `horse-year-greetings` 仓库

#### 第 3 步：配置构建

```
构建命令：npm run build
发布目录：dist
```

#### 第 4 步：部署

点击 **"Deploy site"**，等待 1-2 分钟。

#### 完成！🎉
每次推送代码，Netlify 会自动部署！

---

## 🎨 自定义域名（可选）

### 使用更友好的域名

#### 在 Netlify 中：

1. 进入您的站点
2. 点击 **"Site settings"**
3. 选择 **"Domain management"**
4. 点击 **"Add custom domain"**
5. 输入您想要的名称，如：`horse-year-newyear`

#### 获得：
```
https://horse-year-newyear.netlify.app
```

---

## 📊 您的网站功能

部署成功后，您的网站包含：

✅ **马年祝福发送** - 6 种精美模板
✅ **年夜饭图片收集** - 支持拖拽上传
✅ **照片墙展示** - 瀑布流布局
✅ **实时统计** - 祝福和照片数量
✅ **超级喜庆界面** - 马年元素满屏
✅ **动态效果** - 20+ 动画同时运行

---

## 💡 提示

### 当前模式：本地存储
- 数据保存在浏览器 localStorage
- 适合测试和演示
- 无需配置后端

### 切换到 Supabase（可选）
如果需要多人共享数据：
1. 注册 Supabase 账号
2. 创建项目
3. 配置环境变量
4. 修改 `src/services/index.js`

---

## 🔥 Netlify 免费额度

您使用的是 **Netlify 免费计划**：

| 项目 | 额度 |
|------|------|
| 带宽 | 100GB/月 |
| 构建时间 | 300分钟/月 |
| 站点数 | 无限 |
| 自定义域名 | 无限 |
| SSL 证书 | ✅ 免费 |
| 表单处理 | 100条/月 |
| CDN | ✅ 全球加速 |

**完全够用！** 🎊

---

## 🎁 部署成功后

### 分享您的网站：

将您的 Netlify 域名分享给朋友：
```
https://your-site-name.netlify.app
```

### 二维码：

1. 访问：https://www.qrcode-generator.com/
2. 输入您的网站链接
3. 生成二维码
4. 保存图片，分享到微信群！

---

## 🆘 常见问题

### Q: 构建失败怎么办？
**A:** 确保运行 `npm install` 和 `npm run build` 成功。

### Q: 上传后样式不对？
**A:** 清除浏览器缓存刷新（Ctrl + Shift + R）。

### Q: 想要修改网站内容？
**A:**
- 如果是拖拽部署：重新构建并上传
- 如果是 Git 部署：直接推送代码，自动更新

### Q: 可以绑定自己的域名吗？
**A:** 可以！在 Netlify 域名管理中添加您的域名。

---

## 📞 需要帮助？

- Netlify 文档：https://docs.netlify.com/
- 部署视频：https://www.youtube.com/watch?v=YM3v2T0Yq5E

---

## 🎊 立即部署！

**最快速的方式：拖拽部署**

```bash
# 1. 构建（已完成 ✅）
npm run build

# 2. 访问 https://app.netlify.com/drop
# 3. 拖拽 dist 文件夹
# 4. 完成！
```

祝您部署成功！🐴🧧🎊
