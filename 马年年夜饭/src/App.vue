<template>
  <div class="app">
    <!-- 超级喜庆背景装饰 -->
    <div class="background-decorations">
      <!-- 大灯笼 -->
      <div class="lantern-decoration">
        <span class="lantern">🏮</span>
        <span class="lantern">🏮</span>
        <span class="lantern">🏮</span>
      </div>

      <!-- 祥云 -->
      <div class="cloud-decoration">☁️</div>
      <div class="cloud-decoration">☁️</div>
      <div class="cloud-decoration">☁️</div>

      <!-- 纸屑雨（增加数量） -->
      <div class="confetti" style="left: 5%; animation-delay: 0s;"></div>
      <div class="confetti" style="left: 15%; animation-delay: 0.5s;"></div>
      <div class="confetti" style="left: 25%; animation-delay: 1s;"></div>
      <div class="confetti" style="left: 35%; animation-delay: 1.5s;"></div>
      <div class="confetti" style="left: 45%; animation-delay: 2s;"></div>
      <div class="confetti" style="left: 55%; animation-delay: 2.5s;"></div>
      <div class="confetti" style="left: 65%; animation-delay: 3s;"></div>
      <div class="confetti" style="left: 75%; animation-delay: 3.5s;"></div>
      <div class="confetti" style="left: 85%; animation-delay: 4s;"></div>
      <div class="confetti" style="left: 95%; animation-delay: 4.5s;"></div>

      <!-- 奔马 -->
      <div class="horse-decoration">🐎</div>
      <div class="horse-decoration">🐎</div>
      <div class="horse-decoration">🐎</div>

      <!-- 金币雨 -->
      <div class="coin" style="left: 10%; animation-delay: 0s;"></div>
      <div class="coin" style="left: 30%; animation-delay: 3s;"></div>
      <div class="coin" style="left: 50%; animation-delay: 6s;"></div>
      <div class="coin" style="left: 70%; animation-delay: 9s;"></div>
      <div class="coin" style="left: 90%; animation-delay: 12s;"></div>
    </div>

    <!-- 春联 -->
    <div class="spring-couple-left">龙马精神</div>
    <div class="spring-couple-right">马到成功</div>

    <!-- 导航栏 -->
    <nav class="navbar" v-if="showNav">
      <div class="container nav-container">
        <router-link to="/" class="nav-logo">
          <span class="logo-icon">🐴</span>
          <span class="logo-text">马年新春</span>
          <span class="logo-decorations">
            <span class="logo-decor">🧧</span>
            <span class="logo-decor">🎊</span>
            <span class="logo-decor">🏮</span>
          </span>
        </router-link>

        <div class="nav-menu" :class="{ active: menuOpen }">
          <router-link to="/" class="nav-link" @click="closeMenu">
            <span class="nav-icon">🏠</span>
            <span>首页</span>
            <span class="nav-horse">🐴</span>
          </router-link>
          <router-link to="/greeting" class="nav-link" @click="closeMenu">
            <span class="nav-icon">🧧</span>
            <span>发祝福</span>
            <span class="nav-horse">🐎</span>
          </router-link>
          <router-link to="/upload" class="nav-link" @click="closeMenu">
            <span class="nav-icon">📸</span>
            <span>上传年夜饭</span>
            <span class="nav-horse">🐴</span>
          </router-link>
          <router-link to="/gallery" class="nav-link" @click="closeMenu">
            <span class="nav-icon">🖼️</span>
            <span>年夜饭墙</span>
            <span class="nav-horse">🐎</span>
          </router-link>
        </div>

        <button class="nav-toggle" @click="toggleMenu" v-if="isMobile">
          <span :class="{ active: menuOpen }"></span>
          <span :class="{ active: menuOpen }"></span>
          <span :class="{ active: menuOpen }"></span>
        </button>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <main class="main-content" :class="{ 'with-nav': showNav }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 页脚 -->
    <footer class="footer" v-if="showNav">
      <div class="footer-content">
        <p class="footer-main">🎊 2026 马年新春祝福平台 🎊</p>
        <p class="footer-sub">
          <span>🐴</span>
          <span>愿您龙马精神，马到成功！</span>
          <span>🐴</span>
        </p>
        <p class="footer-luck">💰 恭喜发财，大吉大利 💰</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const menuOpen = ref(false)
const windowWidth = ref(window.innerWidth)

const isMobile = computed(() => windowWidth.value < 768)

const showNav = computed(() => {
  // 在所有页面都显示导航栏
  return true
})

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function closeMenu() {
  menuOpen.value = false
}

function handleResize() {
  windowWidth.value = window.innerWidth
  if (windowWidth.value >= 768) {
    menuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* 背景装饰 */
.background-decorations {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
}

/* 导航栏 */
.navbar {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 3px solid #d32f2f;
}

.navbar::before {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  right: 0;
  height: 3px;
  background: repeating-linear-gradient(
    90deg,
    #d32f2f 0px,
    #d32f2f 20px,
    #ff6f00 20px,
    #ff6f00 40px
  );
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  position: relative;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.logo-icon {
  font-size: 32px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.logo-decoration {
  font-size: 20px;
  margin-left: 4px;
  animation: wiggle 1s ease-in-out infinite;
}

@keyframes wiggle {
  0%, 100% {
    transform: rotate(-5deg);
  }
  50% {
    transform: rotate(5deg);
  }
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #d32f2f 0%, #ff6f00 100%);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-link:hover::before {
  width: 80%;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
}

.nav-icon {
  font-size: 20px;
}

.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
  background: none;
  border: none;
  cursor: pointer;
}

.nav-toggle span {
  width: 24px;
  height: 2px;
  background: #2c3e50;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.nav-toggle span.active:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.nav-toggle span.active:nth-child(2) {
  opacity: 0;
}

.nav-toggle span.active:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .nav-toggle {
    display: flex;
  }

  .nav-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    padding: 16px;
    gap: 4px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transform: translateY(-100%);
    opacity: 0;
    transition: all 0.3s ease;
  }

  .nav-menu.active {
    transform: translateY(0);
    opacity: 1;
  }

  .nav-link {
    width: 100%;
    justify-content: center;
    padding: 12px;
  }
}

/* 主内容 */
.main-content {
  flex: 1;
  padding: 40px 20px;
  position: relative;
  z-index: 1;
}

.main-content.with-nav {
  padding-top: 40px;
}

/* 页脚 */
.footer {
  background: linear-gradient(135deg, rgba(211, 47, 47, 0.95) 0%, rgba(255, 111, 0, 0.95) 100%);
  backdrop-filter: blur(10px);
  padding: 24px 20px;
  text-align: center;
  color: white;
  border-top: none;
  position: relative;
  overflow: hidden;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: repeating-linear-gradient(
    90deg,
    #ffd700 0px,
    #ffd700 30px,
    #ffed4e 30px,
    #ffed4e 60px
  );
}

.footer-content p {
  margin: 4px 0;
  font-weight: 500;
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  /* 导航栏优化 */
  .navbar {
    padding: 8px 0;
  }

  .nav-container {
    padding: 10px 16px;
  }

  .nav-logo {
    font-size: 18px;
  }

  .logo-icon {
    font-size: 28px;
  }

  .logo-decorations {
    display: none; /* 移动端隐藏装饰 */
  }

  /* 导航菜单优化 */
  .nav-menu {
    top: 55px;
    padding: 12px;
    gap: 4px;
  }

  .nav-link {
    width: 100%;
    justify-content: center;
    padding: 14px;
    font-size: 16px;
  }

  .nav-horse {
    display: none; /* 移动端隐藏马图标 */
  }

  /* 汉堡按钮 */
  .nav-toggle {
    padding: 6px;
    border-radius: 6px;
  }

  .nav-toggle span {
    width: 22px;
    height: 2px;
  }

  /* 主内容 */
  .main-content {
    padding: 24px 16px;
  }

  .main-content.with-nav {
    padding-top: 24px;
  }

  /* 页脚优化 */
  .footer-content p {
    font-size: 14px;
  }
}

/* 超小屏优化 */
@media (max-width: 480px) {
  .nav-logo {
    font-size: 16px;
  }

  .logo-icon {
    font-size: 24px;
  }

  .main-content {
    padding: 20px 12px;
  }

  .footer-content p {
    font-size: 13px;
  }
}
</style>
