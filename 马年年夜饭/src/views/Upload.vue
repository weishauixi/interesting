<template>
  <div class="upload-page">
    <div class="container">
      <h1 class="title">📸 上传年夜饭照片 📸</h1>
      <p class="subtitle">🎊 分享您的年夜饭，与大家共度佳节 🎊</p>

      <div class="upload-container">
        <!-- 上传表单 -->
        <div class="upload-form card">
          <h2 class="form-title">上传照片</h2>

          <form @submit.prevent="handleSubmit">
            <!-- 图片上传区域 -->
            <div class="form-group">
              <label class="form-label">选择照片（最多3张）</label>

              <div class="upload-area" :class="{ dragging }" @drop.prevent="handleDrop" @dragover.prevent @dragenter.prevent="dragging = true" @dragleave.prevent="dragging = false">
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/*"
                  multiple
                  @change="handleFileSelect"
                  style="display: none"
                >

                <div v-if="previewImages.length === 0" class="upload-placeholder">
                  <div class="upload-icon">📷</div>
                  <p>拖拽图片到这里</p>
                  <p class="upload-hint">或</p>
                  <button type="button" class="btn btn-secondary" @click="triggerFileInput">
                    选择图片
                  </button>
                  <p class="upload-limit">支持 JPG、PNG 格式，单张不超过 5MB</p>
                </div>

                <div v-else class="preview-list">
                  <div v-for="(image, index) in previewImages" :key="index" class="preview-item">
                    <img :src="image.url" :alt="`预览 ${index + 1}`">
                    <button type="button" class="remove-btn" @click="removeImage(index)">✕</button>
                  </div>

                  <div v-if="previewImages.length < 3" class="preview-add" @click="triggerFileInput">
                    <span class="add-icon">+</span>
                    <span class="add-text">添加图片</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 昵称 -->
            <div class="form-group">
              <label class="form-label">您的昵称</label>
              <input
                v-model="form.uploaderName"
                type="text"
                class="form-input"
                placeholder="请输入您的昵称"
              >
            </div>

            <!-- 新年寄语 -->
            <div class="form-group">
              <label class="form-label">新年寄语</label>
              <textarea
                v-model="form.message"
                class="form-textarea"
                placeholder="说点什么吧..."
                rows="3"
              ></textarea>
            </div>

            <!-- 隐私设置 -->
            <div class="form-group">
              <label class="checkbox-label">
                <input v-model="form.isPublic" type="checkbox">
                <span>公开显示在年夜饭照片墙</span>
              </label>
            </div>

            <!-- 提交按钮 -->
            <div class="form-actions">
              <button type="submit" class="btn btn-primary btn-block" :disabled="submitting || previewImages.length === 0">
                <span v-if="!submitting">🎉 上传照片</span>
                <span v-else>上传中...</span>
              </button>
            </div>
          </form>
        </div>

        <!-- 上传说明 -->
        <div class="upload-tips card">
          <h3 class="tips-title">💡 上传说明</h3>

          <ul class="tips-list">
            <li>📷 支持 1-3 张照片上传</li>
            <li>🖼️ 图片格式：JPG、PNG</li>
            <li>📏 单张图片大小不超过 5MB</li>
            <li>👀 公开的照片将展示在年夜饭照片墙</li>
            <li>🎊 上传后即可在照片墙看到您的年夜饭</li>
          </ul>

          <div class="quick-link">
            <router-link to="/gallery" class="btn btn-outline">
              查看年夜饭照片墙 →
            </router-link>
          </div>
        </div>
      </div>

      <!-- 成功提示 -->
      <div v-if="showSuccess" class="success-modal fade-in" @click="closeSuccess">
        <div class="success-content" @click.stop>
          <div class="success-icon">🎊</div>
          <h3>上传成功！</h3>
          <p>您的年夜饭照片已上传</p>
          <div class="success-actions">
            <router-link to="/gallery" class="btn btn-primary">
              查看照片墙
            </router-link>
            <button @click="resetForm" class="btn btn-outline">
              继续上传
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadPhoto } from '@/services'

const fileInput = ref(null)
const previewImages = ref([])
const selectedFiles = ref([])
const dragging = ref(false)
const submitting = ref(false)
const showSuccess = ref(false)

const form = ref({
  uploaderName: '',
  message: '',
  isPublic: true
})

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(event) {
  const files = Array.from(event.target.files || [])
  addFiles(files)
}

function handleDrop(event) {
  dragging.value = false
  const files = Array.from(event.dataTransfer?.files || [])
  addFiles(files)
}

function addFiles(files) {
  const imageFiles = files.filter(file => file.type.startsWith('image/'))

  if (imageFiles.length === 0) {
    alert('请选择图片文件')
    return
  }

  const remainingSlots = 3 - previewImages.value.length
  const filesToAdd = imageFiles.slice(0, remainingSlots)

  if (filesToAdd.length < imageFiles.length) {
    alert('最多只能上传3张图片')
  }

  filesToAdd.forEach(file => {
    // 检查文件大小
    if (file.size > 5 * 1024 * 1024) {
      alert(`图片 ${file.name} 超过5MB，请选择 smaller 图片`)
      return
    }

    // 创建预览
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImages.value.push({
        url: e.target.result,
        file
      })
      selectedFiles.value.push(file)
    }
    reader.readAsDataURL(file)
  })
}

function removeImage(index) {
  previewImages.value.splice(index, 1)
  selectedFiles.value.splice(index, 1)
}

async function handleSubmit() {
  if (previewImages.value.length === 0) {
    alert('请至少上传一张图片')
    return
  }

  if (!form.value.uploaderName.trim()) {
    alert('请输入您的昵称')
    return
  }

  submitting.value = true

  try {
    // 逐个上传图片
    for (const file of selectedFiles.value) {
      const result = await uploadPhoto({
        file,
        uploaderName: form.value.uploaderName,
        message: form.value.message,
        isPublic: form.value.isPublic
      })

      if (!result.success) {
        throw new Error(result.error)
      }
    }

    showSuccess.value = true
  } catch (error) {
    console.error('上传失败:', error)
    alert('上传失败：' + error.message)
  } finally {
    submitting.value = false
  }
}

function closeSuccess() {
  showSuccess.value = false
}

function resetForm() {
  previewImages.value = []
  selectedFiles.value = []
  form.value = {
    uploaderName: '',
    message: '',
    isPublic: true
  }
  showSuccess.value = false
}
</script>

<style scoped>
.upload-page {
  padding: 20px 0;
}

.upload-container {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 32px;
  align-items: start;
}

.form-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #2c3e50;
}

/* 上传区域 */
.upload-area {
  border: 3px dashed #d32f2f;
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area.dragging {
  border-color: #ffd700;
  background: linear-gradient(135deg, #fff5f5 0%, #ffebee 100%);
  box-shadow: 0 8px 24px rgba(211, 47, 47, 0.2);
}

.upload-placeholder {
  width: 100%;
}

.upload-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.upload-placeholder p {
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
}

.upload-hint {
  color: #999;
  margin: 16px 0;
}

.upload-limit {
  font-size: 14px;
  color: #999;
  margin-top: 16px;
}

/* 预览列表 */
.preview-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  width: 100%;
}

.preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: rgba(231, 76, 60, 0.9);
  transform: scale(1.1);
}

.preview-add {
  aspect-ratio: 1;
  border: 2px dashed #ddd;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
}

.preview-add:hover {
  border-color: #e74c3c;
  background: #fff5f5;
}

.add-icon {
  font-size: 32px;
  color: #999;
}

.add-text {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

/* 复选框样式 */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* 提交按钮 */
.form-actions {
  margin-top: 24px;
}

.btn-block {
  width: 100%;
  padding: 16px;
  font-size: 18px;
}

/* 上传说明 */
.tips-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #2c3e50;
}

.tips-list {
  list-style: none;
  padding: 0;
}

.tips-list li {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 15px;
  line-height: 1.6;
}

.tips-list li:last-child {
  border-bottom: none;
}

.quick-link {
  margin-top: 24px;
}

.quick-link .btn {
  width: 100%;
}

/* 成功提示 */
.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.success-content {
  background: white;
  border-radius: 24px;
  padding: 40px;
  text-align: center;
  max-width: 400px;
  width: 90%;
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.success-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.success-content h3 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #2c3e50;
}

.success-content p {
  color: #666;
  margin-bottom: 24px;
}

.success-actions {
  display: flex;
  gap: 12px;
  flex-direction: column;
}

.success-actions .btn {
  width: 100%;
}

/* 响应式 */
@media (max-width: 1024px) {
  .upload-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .upload-tips {
    order: -1;
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

  /* 表单标题 */
  .form-title {
    font-size: 20px;
    margin-bottom: 20px;
  }

  /* 上传区域 */
  .upload-area {
    padding: 32px;
    min-height: 260px;
    border-width: 2px;
  }

  .upload-icon {
    font-size: 48px;
    margin-bottom: 12px;
  }

  .upload-placeholder p {
    font-size: 15px;
  }

  .upload-hint {
    margin: 12px 0;
  }

  .upload-limit {
    font-size: 13px;
    margin-top: 12px;
  }

  /* 预览列表 */
  .preview-list {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .remove-btn {
    width: 26px;
    height: 26px;
    font-size: 16px;
  }

  .add-icon {
    font-size: 28px;
  }

  .add-text {
    font-size: 13px;
  }

  /* 提交按钮 */
  .btn-block {
    padding: 14px;
    font-size: 16px;
  }

  /* 上传说明 */
  .tips-title {
    font-size: 18px;
    margin-bottom: 16px;
  }

  .tips-list li {
    font-size: 14px;
    padding: 10px 0;
  }

  /* 成功提示 */
  .success-content {
    padding: 32px 24px;
    max-width: 90%;
  }

  .success-icon {
    font-size: 56px;
    margin-bottom: 12px;
  }

  .success-content h3 {
    font-size: 22px;
  }

  .success-content p {
    font-size: 15px;
    margin-bottom: 20px;
  }

  .success-actions {
    gap: 10px;
  }
}

/* 小屏手机 */
@media (max-width: 480px) {
  .upload-page {
    padding: 16px 0;
  }

  .title {
    font-size: 24px !important;
  }

  .subtitle {
    font-size: 14px !important;
  }

  /* 表单标题 */
  .form-title {
    font-size: 18px;
    margin-bottom: 16px;
  }

  /* 上传区域 */
  .upload-area {
    padding: 24px;
    min-height: 220px;
    border-radius: 12px;
  }

  .upload-icon {
    font-size: 40px;
  }

  .upload-placeholder p {
    font-size: 14px;
  }

  .upload-limit {
    font-size: 12px;
  }

  /* 预览列表 */
  .preview-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .preview-item {
    border-radius: 10px;
  }

  .remove-btn {
    width: 24px;
    height: 24px;
    font-size: 14px;
    top: 6px;
    right: 6px;
  }

  .preview-add {
    border-radius: 10px;
  }

  .add-icon {
    font-size: 24px;
  }

  .add-text {
    font-size: 12px;
  }

  /* 按钮优化 */
  .btn-block {
    padding: 12px;
    font-size: 15px;
    min-height: 48px;
  }

  /* 上传说明 */
  .tips-title {
    font-size: 16px;
    margin-bottom: 12px;
  }

  .tips-list li {
    font-size: 13px;
    padding: 8px 0;
  }

  /* 成功提示 */
  .success-content {
    padding: 24px 20px;
    border-radius: 20px;
    width: 95%;
  }

  .success-icon {
    font-size: 48px;
  }

  .success-content h3 {
    font-size: 20px;
    margin-bottom: 6px;
  }

  .success-content p {
    font-size: 14px;
    margin-bottom: 16px;
  }

  .success-actions {
    gap: 8px;
  }

  .success-actions .btn {
    padding: 12px;
    font-size: 14px;
  }
}
</style>
