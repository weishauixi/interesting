# 情绪星云 / 符号漂流 / 时间褶皱

一个抽象交互小程序，通过粒子动画、触摸交互和随机内容生成，创造独特的视觉体验。

## 核心功能

### 1. 全屏粒子动画
- 使用 Canvas 2D API 实现
- 三种随机形状：圆形、三角形、方形
- 粒子带有轨迹拖尾效果
- 每次打开随机配色方案

### 2. 交互方式
| 操作 | 效果 |
|------|------|
| 触摸 | 触发粒子分裂爆发 |
| 滑动 | 改变附近粒子运动方向 |
| 长按 | 保存当前画面到相册 |

### 3. 视觉随机性
- 4 套配色方案，每次启动随机选择
- 粒子大小、速度、形状全随机
- 运动轨迹实时生成

### 4. 抽象文字碎片
- 随机生成中文单字、双字词、符号
- 文字与粒子混合显示
- 平滑渐入渐出动画

### 5. 附加功能
- 背景音乐播放控制
- 震动反馈（触摸/长按/按钮）
- 分享海报生成
- 一键重置画布

## 核心实现逻辑

### 粒子系统 (pages/index/index.js: 60-150)

```javascript
createParticle(x, y, options) {
  return {
    x, y,           // 位置
    vx, vy,         // 速度
    size,           // 大小
    color,          // 颜色
    shape,          // 形状: circle/triangle/square
    rotation,       // 旋转角度
    life,           // 生命值（用于渐隐）
    trail: []       // 运动轨迹
  };
}
```

### 动画循环 (pages/index/index.js: 230-250)

```javascript
startAnimation() {
  const animate = () => {
    this.updateParticles();   // 更新粒子状态
    this.drawParticles();     // 绘制粒子
    this.updateTextParticles(); // 更新文字
    requestAnimationFrame(animate);
  };
  animate();
}
```

### 交互事件绑定 (pages/index/index.js: 340-380)

```javascript
onTouchStart(e)  → splitParticles()  // 粒子分裂
onTouchMove(e)   → 修改粒子速度向量  // 方向控制
onLongPress(e)   → canvasToTempFilePath() // 保存图片
```

## 文件结构

```
interst/
├── app.js              # 小程序入口
├── app.json            # 全局配置
├── app.wxss            # 全局样式
├── sitemap.json        # 索引配置
├── project.config.json # 项目配置
└── pages/
    └── index/
        ├── index.js    # 核心逻辑（粒子系统、动画、交互）
        ├── index.json  # 页面配置
        ├── index.wxml  # 页面结构
        └── index.wxss  # 页面样式
```

## 部署说明

1. 打开微信开发者工具
2. 导入项目，选择 `interst` 目录
3. 修改 `project.config.json` 中的 `appid` 为你的小程序 AppID
4. 点击"预览"或"上传"进行部署

## 扩展建议

- 添加重力感应控制（需获取设备权限）
- 支持更多粒子形状和特效
- 增加自定义配色方案
- 添加粒子间的引力/斥力物理效果
