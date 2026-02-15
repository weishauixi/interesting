<template>
  <div class="greeting-page">
    <div class="container">
      <h1 class="title">🧧 发送马年祝福 🧧</h1>
      <p class="subtitle">✨ 选择精美模板，定制专属祝福 ✨</p>

      <div class="greeting-container">
        <!-- 左侧：表单区域 -->
        <div class="form-section">
          <div class="card">
            <h2 class="section-title">1️⃣ 选择祝福模板</h2>

            <div class="templates-grid">
              <div
                v-for="template in templates"
                :key="template.id"
                class="template-card"
                :class="{ active: selectedTemplate === template.id }"
                @click="selectTemplate(template.id)"
              >
                <div class="template-preview" :style="{ background: template.gradient }">
                  <span class="template-emoji">{{ template.emoji }}</span>
                </div>
                <div class="template-name">{{ template.name }}</div>
              </div>
            </div>

            <h2 class="section-title" style="margin-top: 32px;">2️⃣ 填写祝福信息</h2>

            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label class="form-label">您的昵称</label>
                <input
                  v-model="form.senderName"
                  type="text"
                  class="form-input"
                  placeholder="请输入您的昵称（可选）"
                >
              </div>

              <div class="form-group">
                <label class="form-label">祝福对象</label>
                <input
                  v-model="form.recipientName"
                  type="text"
                  class="form-input"
                  placeholder="如：所有人、爸爸妈妈、亲爱的朋友们..."
                >
              </div>

              <div class="form-group">
                <label class="form-label">祝福语</label>
                <textarea
                  v-model="form.message"
                  class="form-textarea"
                  placeholder="输入您的祝福语..."
                  rows="4"
                ></textarea>
              </div>

              <div class="form-actions">
                <button type="submit" class="btn btn-primary" :disabled="submitting">
                  <span v-if="!submitting">🎉 生成祝福卡片</span>
                  <span v-else>生成中...</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- 右侧：预览区域 -->
        <div class="preview-section">
          <div class="card preview-card">
            <h2 class="section-title">👁️ 卡片预览</h2>

            <div class="greeting-card-preview" :style="{ background: selectedTemplateGradient }">
              <div class="preview-decoration">{{ selectedTemplateEmoji }}</div>

              <div class="preview-content">
                <div class="preview-header">
                  <span class="preview-badge">马年新春</span>
                </div>

                <div class="preview-message">
                  {{ displayMessage }}
                </div>

                <div class="preview-footer">
                  <div class="preview-from">
                    <span class="label">来自：</span>
                    <span class="value">{{ form.senderName || '匿名' }}</span>
                  </div>
                  <div class="preview-to">
                    <span class="label">致：</span>
                    <span class="value">{{ form.recipientName || '所有人' }}</span>
                  </div>
                </div>

                <div class="preview-date">
                  {{ new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' }) }}
                </div>
              </div>
            </div>

            <div class="preview-actions" v-if="generated">
              <button @click="copyLink" class="btn btn-secondary">
                <span>🔗</span>
                复制链接分享
              </button>
              <button @click="downloadCard" class="btn btn-outline">
                <span>💾</span>
                保存为图片
              </button>
            </div>
          </div>

          <!-- 成功提示 -->
          <div v-if="showSuccess" class="success-message fade-in">
            <span class="success-icon">✅</span>
            <p>祝福卡片生成成功！</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { saveGreeting } from '@/services'

// 祝福模板
const templates = [
  {
    id: 1,
    name: '龙马精神',
    emoji: '🐴',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: 2,
    name: '红红火火',
    emoji: '🧧',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    id: 3,
    name: '金玉满堂',
    emoji: '💰',
    gradient: 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)'
  },
  {
    id: 4,
    name: '春风得意',
    emoji: '🌸',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
  },
  {
    id: 5,
    name: '国潮风',
    emoji: '🏮',
    gradient: 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'
  },
  {
    id: 6,
    name: '水墨丹青',
    emoji: '🖌️',
    gradient: 'linear-gradient(135deg, #434343 0%, #000000 100%)'
  }
]

// 表单数据
const form = ref({
  senderName: '',
  recipientName: '所有人',
  message: ''
})

const selectedTemplate = ref(1)
const submitting = ref(false)
const generated = ref(false)
const showSuccess = ref(false)
const greetingId = ref('')

// 选中的模板信息
const selectedTemplateGradient = computed(() => {
  const template = templates.find(t => t.id === selectedTemplate.value)
  return template?.gradient || templates[0].gradient
})

const selectedTemplateEmoji = computed(() => {
  const template = templates.find(t => t.id === selectedTemplate.value)
  return template?.emoji || '🐴'
})

// 显示的祝福语
const displayMessage = computed(() => {
  if (form.value.message) {
    return form.value.message
  }
  return '龙马精神迎新春，马到成功行大运！愿您在新的一年里身体健康，万事如意，阖家幸福！'
})

function selectTemplate(id) {
  selectedTemplate.value = id
}

async function handleSubmit() {
  if (!form.value.message.trim()) {
    alert('请输入祝福语')
    return
  }

  submitting.value = true

  try {
    const result = await saveGreeting({
      templateId: selectedTemplate.value,
      message: form.value.message,
      senderName: form.value.senderName || '匿名',
      recipientName: form.value.recipientName || '所有人',
      backgroundStyle: 'gradient'
    })

    if (result.success) {
      greetingId.value = result.id
      generated.value = true
      showSuccess.value = true

      setTimeout(() => {
        showSuccess.value = false
      }, 3000)
    } else {
      alert('生成失败：' + result.error)
    }
  } catch (error) {
    console.error('提交失败:', error)
    alert('生成失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

function copyLink() {
  const url = `${window.location.origin}/greeting/${greetingId.value}`
  navigator.clipboard.writeText(url).then(() => {
    alert('链接已复制到剪贴板！')
  }).catch(() => {
    alert('复制失败，请手动复制地址栏链接')
  })
}

function downloadCard() {
  alert('图片保存功能开发中，您可以截图保存当前预览')
}

onMounted(() => {
  // 设置默认祝福语
  form.value.message = '龙马精神迎新春，马到成功行大运！愿您在新的一年里身体健康，万事如意，阖家幸福！'
})
</script>

<style scoped>
.greeting-page {
  padding: 20px 0;
}

.greeting-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: start;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #d32f2f;
  position: relative;
  padding-left: 16px;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #d32f2f 0%, #ffd700 100%);
  border-radius: 2px;
}

/* 模板网格 */
.templates-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.template-card {
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 3px solid transparent;
}

.template-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(211, 47, 47, 0.2);
}

.template-card.active {
  border-color: #d32f2f;
  box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.3);
}

.template-preview {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.template-emoji {
  font-size: 32px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.template-name {
  padding: 8px;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  background: white;
  color: #d32f2f;
}

/* 表单操作 */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

/* 预览卡片 */
.preview-card {
  position: sticky;
  top: 100px;
}

.greeting-card-preview {
  border-radius: 16px;
  padding: 32px;
  color: white;
  position: relative;
  overflow: hidden;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-decoration {
  position: absolute;
  font-size: 120px;
  opacity: 0.2;
  top: 20px;
  right: 20px;
}

.preview-content {
  position: relative;
  z-index: 1;
  width: 100%;
}

.preview-header {
  text-align: center;
  margin-bottom: 24px;
}

.preview-badge {
  display: inline-block;
  padding: 8px 24px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.preview-message {
  font-size: 18px;
  line-height: 1.8;
  text-align: center;
  margin-bottom: 32px;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.preview-footer {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 14px;
}

.preview-from,
.preview-to {
  display: flex;
  gap: 8px;
  align-items: center;
}

.label {
  opacity: 0.8;
}

.value {
  font-weight: 600;
}

.preview-date {
  text-align: center;
  font-size: 12px;
  opacity: 0.7;
}

.preview-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.preview-actions .btn {
  flex: 1;
}

/* 成功提示 */
.success-message {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 12px;
  padding: 16px 20px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #155724;
}

.success-icon {
  font-size: 24px;
}

/* 响应式 */
@media (max-width: 1024px) {
  .greeting-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .preview-card {
    position: static;
  }

  .templates-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  /* 标题和副标题 */
  .title {
    font-size: 28px !important;
  }

  .subtitle {
    font-size: 15px !important;
  }

  /* 章节标题 */
  .section-title {
    font-size: 18px;
    margin-bottom: 16px;
  }

  /* 模板网格 */
  .templates-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 20px;
  }

  .template-preview {
    height: 70px;
  }

  .template-emoji {
    font-size: 28px;
  }

  .template-name {
    font-size: 13px;
    padding: 6px;
  }

  /* 表单操作 */
  .form-actions {
    flex-direction: column;
    gap: 12px;
  }

  .form-actions .btn {
    width: 100%;
    justify-content: center;
  }

  /* 预览卡片 */
  .greeting-card-preview {
    min-height: 350px;
    padding: 24px;
  }

  .preview-decoration {
    font-size: 80px;
    top: 10px;
    right: 10px;
  }

  .preview-badge {
    padding: 6px 20px;
    font-size: 13px;
  }

  .preview-message {
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 24px;
    min-height: 80px;
  }

  .preview-footer {
    font-size: 13px;
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }

  .preview-date {
    font-size: 11px;
  }

  /* 预览操作按钮 */
  .preview-actions {
    flex-direction: column;
    gap: 10px;
    margin-top: 16px;
  }

  .preview-actions .btn {
    width: 100%;
  }

  /* 成功提示 */
  .success-message {
    padding: 12px 16px;
    font-size: 14px;
  }

  .success-icon {
    font-size: 20px;
  }
}

/* 小屏手机 */
@media (max-width: 480px) {
  .greeting-page {
    padding: 16px 0;
  }

  .title {
    font-size: 24px !important;
  }

  .subtitle {
    font-size: 14px !important;
  }

  /* 模板网格 */
  .templates-grid {
    gap: 8px;
  }

  .template-preview {
    height: 60px;
  }

  .template-emoji {
    font-size: 24px;
  }

  .template-name {
    font-size: 12px;
    padding: 4px;
  }

  /* 预览卡片 */
  .greeting-card-preview {
    min-height: 300px;
    padding: 20px;
    border-radius: 12px;
  }

  .preview-decoration {
    font-size: 60px;
  }

  .preview-badge {
    padding: 4px 16px;
    font-size: 12px;
  }

  .preview-message {
    font-size: 14px;
    line-height: 1.5;
    min-height: 70px;
  }

  .preview-footer {
    font-size: 12px;
  }

  .label,
  .value {
    font-size: 12px;
  }

  .preview-date {
    font-size: 10px;
  }

  /* 成功提示 */
  .success-message {
    padding: 10px 14px;
    font-size: 13px;
    border-radius: 10px;
  }

  .success-icon {
    font-size: 18px;
  }
}
</style>
