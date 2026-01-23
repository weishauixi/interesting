// index.js - 主页面核心逻辑
// 实现粒子系统、动画循环、交互事件绑定

const app = getApp();

Page({
  data: {
    textParticles: [],           // 文字粒子数组
    isPlayingMusic: false,       // 背景音乐状态
  },

  // ==================== 粒子类定义 ====================
  particles: [],                 // 图形粒子数组
  canvas: null,
  ctx: null,
  width: 0,
  height: 0,
  animationId: null,

  // 抽象文字素材库
  textSources: [
    '梦', '雾', '光', '影', '尘', '风', '雨', '雪',
    '流逝', '碎片', '褶皱', '飘浮', '沉没', '绽放',
    '⌘', '⎔', '⎊', '∞', '◇', '○', '△', '□',
    '霎那', '永恒', '虚无', '存在', '混沌',
    '像风一样', '时光倒流', '星云破碎', '寂静回响'
  ],

  // 配色方案
  colorPalettes: [
    ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],  // 温暖
    ['#A8E6CF', '#DCEDC1', '#FFD3B6', '#FFAAA5'],  // 柔和
    ['#667eea', '#764ba2', '#f093fb', '#4facfe'],  // 梦幻
    ['#00d2ff', '#3a7bd5', '#00b4db', '#1e3c72'],  // 冷调
  ],

  // 当前配色
  colors: [],

  onLoad() {
    this.initCanvas();
    this.initColors();
    this.initParticles();
    this.startAnimation();
    this.spawnTextParticles();
  },

  onUnload() {
    this.stopAnimation();
  },

  // ==================== Canvas初始化 ====================
  initCanvas() {
    const query = wx.createSelectorQuery();
    query.select('#particleCanvas')
      .fields({ node: true, size: true })
      .exec((res) => {
        if (!res[0]) return;

        const canvas = res[0].node;
        const ctx = canvas.getContext('2d');

        // 设置画布尺寸
        const dpr = wx.getSystemInfoSync().pixelRatio;
        canvas.width = res[0].width * dpr;
        canvas.height = res[0].height * dpr;
        ctx.scale(dpr, dpr);

        this.canvas = canvas;
        this.ctx = ctx;
        this.width = res[0].width;
        this.height = res[0].height;
      });
  },

  // ==================== 颜色初始化 ====================
  initColors() {
    const palette = this.colorPalettes[Math.floor(Math.random() * this.colorPalettes.length)];
    this.colors = [...palette];
  },

  // ==================== 粒子系统核心 ====================
  /**
   * 粒子类 - 包含位置、速度、颜色、形状属性
   */
  createParticle(x, y, options = {}) {
    const shape = options.shape || ['circle', 'triangle', 'square'][Math.floor(Math.random() * 3)];
    const size = options.size || Math.random() * 20 + 5;
    const color = options.color || this.colors[Math.floor(Math.random() * this.colors.length)];

    return {
      x: x || Math.random() * this.width,
      y: y || Math.random() * this.height,
      vx: (Math.random() - 0.5) * 3,           // X轴速度
      vy: (Math.random() - 0.5) * 3,           // Y轴速度
      size: size,
      targetSize: size,
      currentSize: 0,
      color: color,
      shape: shape,
      rotation: Math.random() * Math.PI * 2,   // 旋转角度
      rotationSpeed: (Math.random() - 0.5) * 0.1,
      life: 1,                                  // 生命值
      decay: Math.random() * 0.002 + 0.0005,   // 衰减速度
      alpha: Math.random() * 0.5 + 0.3,        // 透明度
      trail: [],                                // 轨迹
    };
  },

  /**
   * 初始化粒子 - 创建初始粒子群
   */
  initParticles() {
    const count = 50; // 初始粒子数量
    for (let i = 0; i < count; i++) {
      this.particles.push(this.createParticle());
    }
  },

  /**
   * 更新粒子 - 计算位置、速度、生命周期
   */
  updateParticles() {
    this.particles = this.particles.filter(p => {
      // 更新位置
      p.x += p.vx;
      p.y += p.vy;

      // 边界反弹
      if (p.x < 0 || p.x > this.width) p.vx *= -0.8;
      if (p.y < 0 || p.y > this.height) p.vy *= -0.8;

      // 旋转更新
      p.rotation += p.rotationSpeed;

      // 渐入效果
      if (p.currentSize < p.targetSize) {
        p.currentSize += 0.5;
      }

      // 记录轨迹
      p.trail.push({ x: p.x, y: p.y });
      if (p.trail.length > 20) p.trail.shift();

      // 生命衰减
      p.life -= p.decay;

      return p.life > 0;
    });

    // 维持最小粒子数
    while (this.particles.length < 30) {
      this.particles.push(this.createParticle());
    }
  },

  /**
   * 绘制粒子 - 根据形状绘制
   */
  drawParticles() {
    const ctx = this.ctx;

    // 半透明背景实现拖尾效果
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, this.width, this.height);

    this.particles.forEach(p => {
      ctx.save();
      ctx.globalAlpha = p.alpha * p.life;
      ctx.fillStyle = p.color;

      // 绘制轨迹
      if (p.trail.length > 1) {
        ctx.beginPath();
        ctx.moveTo(p.trail[0].x, p.trail[0].y);
        p.trail.forEach((point, i) => {
          ctx.lineTo(point.x, point.y);
        });
        ctx.strokeStyle = p.color;
        ctx.lineWidth = p.size * 0.3;
        ctx.globalAlpha = p.alpha * p.life * 0.3;
        ctx.stroke();
      }

      // 绘制粒子
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation);
      ctx.globalAlpha = p.alpha * p.life;

      switch (p.shape) {
        case 'circle':
          ctx.beginPath();
          ctx.arc(0, 0, p.currentSize, 0, Math.PI * 2);
          ctx.fill();
          break;

        case 'triangle':
          ctx.beginPath();
          ctx.moveTo(0, -p.currentSize);
          ctx.lineTo(p.currentSize * 0.866, p.currentSize * 0.5);
          ctx.lineTo(-p.currentSize * 0.866, p.currentSize * 0.5);
          ctx.closePath();
          ctx.fill();
          break;

        case 'square':
          ctx.fillRect(-p.currentSize / 2, -p.currentSize / 2, p.currentSize, p.currentSize);
          break;
      }

      ctx.restore();
    });
  },

  /**
   * 粒子分裂 - 触摸时触发
   */
  splitParticles(x, y) {
    const splitCount = 8;
    for (let i = 0; i < splitCount; i++) {
      const angle = (Math.PI * 2 / splitCount) * i;
      const speed = Math.random() * 4 + 2;
      const particle = this.createParticle(x, y, {
        size: Math.random() * 15 + 5,
        color: this.colors[Math.floor(Math.random() * this.colors.length)]
      });
      particle.vx = Math.cos(angle) * speed;
      particle.vy = Math.sin(angle) * speed;
      particle.decay = 0.01; // 更快衰减
      this.particles.push(particle);
    }

    // 震动反馈
    wx.vibrateShort({ type: 'light' });
  },

  // ==================== 动画循环 ====================
  /**
   * 主动画循环 - 使用requestAnimationFrame
   */
  startAnimation() {
    const animate = () => {
      if (!this.ctx) return;

      this.updateParticles();
      this.drawParticles();
      this.updateTextParticles();

      this.animationId = requestAnimationFrame(animate);
    };
    animate();
  },

  stopAnimation() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
  },

  // ==================== 文字粒子系统 ====================
  textParticleId: 0,

  spawnTextParticles() {
    // 定时生成文字粒子
    setInterval(() => {
      if (this.data.textParticles.length < 8) {
        const text = this.textSources[Math.floor(Math.random() * this.textSources.length)];
        const color = this.colors[Math.floor(Math.random() * this.colors.length)];

        const textParticle = {
          id: this.textParticleId++,
          text: text,
          x: Math.random() * (this.width - 100) + 50,
          y: Math.random() * (this.height - 100) + 50,
          vx: (Math.random() - 0.5) * 1,
          vy: (Math.random() - 0.5) * 1,
          color: color,
          size: Math.random() * 20 + 14,
          opacity: 0,
          targetOpacity: Math.random() * 0.6 + 0.4,
        };

        const textParticles = [...this.data.textParticles, textParticle];
        this.setData({ textParticles });
      }
    }, 3000);
  },

  updateTextParticles() {
    const textParticles = this.data.textParticles.map(p => {
      let newX = p.x + p.vx;
      let newY = p.y + p.vy;

      // 边界检测
      if (newX < 0 || newX > this.width) p.vx *= -1;
      if (newY < 0 || newY > this.height) p.vy *= -1;

      // 渐入效果
      let newOpacity = p.opacity;
      if (newOpacity < p.targetOpacity) {
        newOpacity = Math.min(p.opacity + 0.02, p.targetOpacity);
      }

      return {
        ...p,
        x: newX,
        y: newY,
        opacity: newOpacity
      };
    });

    this.setData({ textParticles });
  },

  // ==================== 触摸交互 ====================
  lastTouchPos: { x: 0, y: 0 },
  touchStartTime: 0,
  longPressTimer: null,

  /**
   * 触摸开始 - 粒子分裂
   */
  onTouchStart(e) {
    const touch = e.touches[0];
    this.lastTouchPos = { x: touch.x, y: touch.y };
    this.touchStartTime = Date.now();

    // 触摸处生成新粒子
    this.splitParticles(touch.x, touch.y);

    // 长按检测
    this.longPressTimer = setTimeout(() => {
      this.onLongPress(e);
    }, 800);
  },

  /**
   * 触摸移动 - 改变附近粒子运动方向
   */
  onTouchMove(e) {
    const touch = e.touches[0];
    const dx = touch.x - this.lastTouchPos.x;
    const dy = touch.y - this.lastTouchPos.y;

    // 影响附近粒子
    this.particles.forEach(p => {
      const dist = Math.hypot(p.x - touch.x, p.y - touch.y);
      if (dist < 150) {
        p.vx += dx * 0.02;
        p.vy += dy * 0.02;
      }
    });

    this.lastTouchPos = { x: touch.x, y: touch.y };
  },

  /**
   * 触摸结束
   */
  onTouchEnd() {
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }
  },

  /**
   * 长按 - 保存图片
   */
  onLongPress(e) {
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }

    wx.vibrateShort({ type: 'heavy' });

    // 导出画布为图片
    wx.canvasToTempFilePath({
      canvas: this.canvas,
      success: (res) => {
        wx.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success: () => {
            wx.showToast({
              title: '已保存到相册',
              icon: 'success'
            });
          }
        });
      }
    });
  },

  // ==================== 控制功能 ====================
  /**
   * 切换背景音乐
   */
  toggleMusic() {
    const innerAudioContext = this.innerAudioContext;

    if (!innerAudioContext) {
      // 创建音频上下文（使用在线白噪音资源）
      this.innerAudioContext = wx.createInnerAudioContext();
      this.innerAudioContext.src = 'https://assets.mixkit.co/music/preview/mixkit-sleepy-cat-135.mp3';
      this.innerAudioContext.loop = true;
      this.innerAudioContext.volume = 0.3;

      this.innerAudioContext.onPlay(() => {
        this.setData({ isPlayingMusic: true });
      });

      this.innerAudioContext.onPause(() => {
        this.setData({ isPlayingMusic: false });
      });

      this.innerAudioContext.play();
    } else {
      if (this.data.isPlayingMusic) {
        innerAudioContext.pause();
      } else {
        innerAudioContext.play();
      }
    }

    wx.vibrateShort({ type: 'light' });
  },

  /**
   * 生成分享海报
   */
  sharePoster() {
    wx.vibrateShort({ type: 'light' });

    wx.canvasToTempFilePath({
      canvas: this.canvas,
      success: (res) => {
        wx.showShareImageMenu({
          path: res.tempFilePath,
          success: () => {
            wx.showToast({
              title: '可分享给好友',
              icon: 'success'
            });
          }
        });
      }
    });
  },

  /**
   * 重置画布
   */
  resetCanvas() {
    wx.vibrateShort({ type: 'medium' });

    // 清除粒子
    this.particles = [];
    this.setData({ textParticles: [] });

    // 重新初始化
    this.initColors();
    this.initParticles();

    // 清空画布
    if (this.ctx) {
      this.ctx.fillStyle = '#000';
      this.ctx.fillRect(0, 0, this.width, this.height);
    }

    wx.showToast({
      title: '已重置',
      icon: 'success',
      duration: 1000
    });
  },

  /**
   * 分享配置
   */
  onShareAppMessage() {
    return {
      title: '情绪星云 - 触碰抽象之美',
      path: '/pages/index/index',
      imageUrl: ''
    };
  }
});
