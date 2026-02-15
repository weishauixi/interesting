<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero">
      <div class="container hero-content">
        <div class="hero-decoration">🐴</div>
        <div class="hero-title-container">
          <h1 class="hero-title">🎊 马年新春祝福 🎊</h1>
          <div class="title-gold-decoration">✨</div>
        </div>
        <p class="hero-subtitle">🧧 龙马精神迎新春，马到成功行大运 🧧</p>
        <div class="festive-divider">
          <span class="divider-icon">💰</span>
          <span class="divider-line"></span>
          <span class="divider-text">新年快乐</span>
          <span class="divider-line"></span>
          <span class="divider-icon">💰</span>
        </div>

        <!-- 统计数据 -->
        <div class="stats" v-if="stats">
          <div class="stat-item">
            <div class="stat-number">{{ stats.greetingsCount }}</div>
            <div class="stat-label">已发送祝福</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.photosCount }}</div>
            <div class="stat-label">年夜饭照片</div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="hero-actions">
          <router-link to="/greeting" class="btn btn-primary btn-lg">
            <span>🧧</span>
            发送新春祝福
          </router-link>
          <router-link to="/upload" class="btn btn-secondary btn-lg">
            <span>📸</span>
            上传年夜饭
          </router-link>
        </div>
      </div>
    </section>

    <!-- 特色功能介绍 -->
    <section class="features">
      <div class="container">
        <h2 class="section-title">✨ 马年特色功能</h2>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <h3 class="feature-title">精美祝福卡片</h3>
            <p class="feature-desc">选择马年主题模板，生成专属祝福卡片，分享给亲友</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🖼️</div>
            <h3 class="feature-title">年夜饭照片墙</h3>
            <p class="feature-desc">上传年夜饭照片，与大家分享节日美食与团圆时刻</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3 class="feature-title">温馨祝福墙</h3>
            <p class="feature-desc">浏览所有祝福，感受节日的温暖与喜庆</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 祝福预览 -->
    <section class="preview-greetings">
      <div class="container">
        <h2 class="section-title">💝 最新祝福</h2>

        <div v-if="loading" class="loading">加载中...</div>

        <div v-else-if="greetings.length > 0" class="greetings-list">
          <div
            v-for="greeting in greetings"
            :key="greeting.objectId"
            class="greeting-card"
          >
            <div class="greeting-header">
              <span class="greeting-sender">{{ greeting.senderName }}</span>
              <span class="greeting-time">{{ formatTime(greeting.createdAt) }}</span>
            </div>
            <div class="greeting-message">{{ greeting.message }}</div>
            <div class="greeting-footer">
              <span class="greeting-recipient">致 {{ greeting.recipientName }}</span>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>还没有祝福，快来发送第一条吧！</p>
        </div>

        <div class="section-action" v-if="greetings.length > 0">
          <router-link to="/gallery" class="btn btn-outline">
            查看更多祝福 →
          </router-link>
        </div>
      </div>
    </section>

    <!-- 装饰元素 -->
    <div class="floating-lanterns">
      <span class="lantern">🏮</span>
      <span class="lantern">🏮</span>
      <span class="lantern">🏮</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getGreetings, getStats } from '@/services'

const greetings = ref([])
const stats = ref(null)
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    // 并行加载祝福和统计数据
    const [greetingsResult, statsResult] = await Promise.all([
      getGreetings(6),
      getStats()
    ])

    if (greetingsResult.success) {
      greetings.value = greetingsResult.data
    }

    if (statsResult.success) {
      stats.value = statsResult.data
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

function formatTime(timestamp) {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`

  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.home {
  position: relative;
}

/* 英雄区域 */
.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 245, 245, 0.98) 50%, rgba(255, 235, 238, 0.98) 100%);
  border-radius: 24px;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
  border: 3px solid #d32f2f;
  box-shadow: 0 8px 32px rgba(211, 47, 47, 0.2);
}

.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 3s ease-in-out infinite;
}

.hero::after {
  content: '';
  position: absolute;
  bottom: -50%;
  left: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(211, 47, 47, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 3s ease-in-out infinite 1.5s;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-decoration {
  font-size: 80px;
  margin-bottom: 16px;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.hero-title-container {
  position: relative;
  margin-bottom: 16px;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 0;
  background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 50%, #ffd700 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  z-index: 1;
}

.title-gold-decoration {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 60px;
  opacity: 0.3;
  z-index: 0;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

.hero-subtitle {
  font-size: 20px;
  color: #d32f2f;
  margin-bottom: 24px;
  font-weight: 600;
}

/* 喜庆分隔线 */
.festive-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 32px;
}

.divider-icon {
  font-size: 32px;
  animation: bounce 2s ease-in-out infinite;
}

.divider-icon:nth-child(5) {
  animation-delay: 1s;
}

.divider-line {
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, #ffd700 50%, transparent 100%);
}

.divider-text {
  font-size: 18px;
  font-weight: 700;
  color: #d32f2f;
  padding: 8px 24px;
  background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
  border-radius: 20px;
  border: 2px solid #ffd700;
}

/* 统计数据 */
.stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-bottom: 40px;
  padding: 24px;
  background: linear-gradient(135deg, rgba(211, 47, 47, 0.1) 0%, rgba(255, 215, 0, 0.1) 100%);
  border-radius: 16px;
  border: 2px solid rgba(211, 47, 47, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(211, 47, 47, 0.2);
}

.stat-label {
  font-size: 14px;
  color: #d32f2f;
  margin-top: 4px;
  font-weight: 600;
}

.stat-divider {
  width: 2px;
  height: 40px;
  background: linear-gradient(180deg, transparent 0%, #ffd700 50%, transparent 100%);
}

/* 操作按钮 */
.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 16px 40px;
  font-size: 18px;
  position: relative;
  overflow: hidden;
}

.btn-lg::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.3) 50%, transparent 100%);
  transition: left 0.5s;
}

.btn-lg:hover::before {
  left: 100%;
}

/* 特色功能 */
.features {
  margin-bottom: 60px;
}

.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 40px;
  color: #d32f2f;
  position: relative;
  padding-bottom: 16px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, transparent 0%, #ffd700 50%, transparent 100%);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.feature-card {
  background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.1);
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #d32f2f 0%, #ffd700 50%, #ff6f00 100%);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(211, 47, 47, 0.2);
  border-color: #ffd700;
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: inline-block;
  animation: wiggle 3s ease-in-out infinite;
}

.feature-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #d32f2f;
}

.feature-desc {
  color: #666;
  line-height: 1.6;
}

/* 祝福预览 */
.preview-greetings {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 245, 245, 0.98) 100%);
  border-radius: 24px;
  padding: 40px 20px;
  border: 3px solid #d32f2f;
  box-shadow: 0 8px 32px rgba(211, 47, 47, 0.15);
}

.greetings-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.greeting-card {
  background: linear-gradient(135deg, #fff 0%, #fff5f5 50%, #ffebee 100%);
  border-radius: 12px;
  padding: 20px;
  border: 2px solid #d32f2f;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.greeting-card::before {
  content: '🧧';
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 20px;
  opacity: 0.3;
}

.greeting-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 24px rgba(211, 47, 47, 0.25);
  border-color: #ffd700;
}

.greeting-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 2px solid rgba(211, 47, 47, 0.1);
}

.greeting-sender {
  font-weight: 600;
  color: #d32f2f;
}

.greeting-time {
  font-size: 12px;
  color: #ff6f00;
  font-weight: 500;
}

.greeting-message {
  font-size: 16px;
  line-height: 1.6;
  color: #2c3e50;
  margin-bottom: 12px;
  min-height: 48px;
}

.greeting-footer {
  display: flex;
  justify-content: flex-end;
}

.greeting-recipient {
  font-size: 14px;
  color: #d32f2f;
  font-weight: 500;
}

.section-action {
  text-align: center;
}

/* 浮动灯笼装饰 */
.floating-lanterns {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  pointer-events: none;
  z-index: -1;
}

.lantern {
  position: absolute;
  font-size: 40px;
  opacity: 0.6;
  animation: float 4s ease-in-out infinite;
}

.lantern:nth-child(1) {
  left: 5%;
  animation-delay: 0s;
}

.lantern:nth-child(2) {
  left: 50%;
  animation-delay: 1s;
}

.lantern:nth-child(3) {
  right: 5%;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .hero {
    padding: 40px 16px;
    margin-bottom: 24px;
  }

  .hero-decoration {
    font-size: 50px;
  }

  .hero-title-container {
    margin-bottom: 16px;
  }

  .hero-title {
    font-size: 28px;
    line-height: 1.2;
  }

  .title-gold-decoration {
    font-size: 40px;
  }

  .hero-subtitle {
    font-size: 15px;
    margin-bottom: 24px;
  }

  /* 统计数据 */
  .stats {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    margin-bottom: 24px;
  }

  .stat-value {
    font-size: 28px;
  }

  .stat-label {
    font-size: 13px;
  }

  .stat-divider {
    width: 30px;
    height: 2px;
  }

  /* 分隔线 */
  .festive-divider {
    flex-direction: column;
    gap: 12px;
    margin: 24px 0;
  }

  .festive-divider .divider-icon {
    font-size: 30px;
  }

  .festive-divider .divider-line {
    width: 80px;
  }

  .festive-divider .divider-text {
    font-size: 18px;
    padding: 10px 24px;
  }

  /* 操作按钮 */
  .hero-actions {
    flex-direction: column;
    align-items: center;
    gap: 12px;
    width: 100%;
  }

  .btn-lg {
    width: 100%;
    max-width: 280px;
  }

  /* 特色功能 */
  .features-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .feature-card {
    padding: 24px;
  }

  .feature-icon {
    font-size: 40px;
  }

  .feature-title {
    font-size: 18px;
  }

  /* 祝福卡片 */
  .greetings-list {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .greeting-card {
    padding: 16px;
  }

  .section-action {
    display: flex;
    justify-content: center;
  }

  .section-action .btn {
    width: 100%;
    max-width: 280px;
  }

  /* 浮动元素 */
  .lantern {
    font-size: 40px !important;
  }
}

/* 小屏手机 */
@media (max-width: 480px) {
  .hero-title {
    font-size: 24px;
  }

  .hero-decoration {
    font-size: 40px;
  }

  .title-gold-decoration {
    font-size: 30px;
  }

  .stats {
    padding: 12px;
  }

  .stat-value {
    font-size: 24px;
  }

  .btn-lg {
    padding: 14px 28px;
    font-size: 15px;
  }

  .feature-card {
    padding: 20px;
  }
}
</style>
