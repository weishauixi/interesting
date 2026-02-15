<template>
  <div class="gallery-page">
    <div class="container">
      <h1 class="title">🖼️ 年夜饭照片墙 🖼️</h1>
      <p class="subtitle">🎊 看看大家都在吃什么 🎊</p>

      <!-- 统计信息 -->
      <div class="stats-bar">
        <div class="stat-item">
          <span class="stat-value">{{ photos.length }}</span>
          <span class="stat-label">张照片</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">{{ uniqueUploaders }}</span>
          <span class="stat-label">位朋友参与</span>
        </div>
      </div>

      <!-- 筛选和上传 -->
      <div class="action-bar">
        <div class="filter-bar">
          <button
            class="filter-btn"
            :class="{ active: filter === 'all' }"
            @click="setFilter('all')"
          >
            全部
          </button>
          <button
            class="filter-btn"
            :class="{ active: filter === 'latest' }"
            @click="setFilter('latest')"
          >
            最新
          </button>
        </div>

        <button @click="showUploadForm = !showUploadForm" class="btn btn-primary upload-toggle-btn">
          <span v-if="!showUploadForm">📸 上传我的年夜饭</span>
          <span v-else>✕ 收起上传</span>
        </button>
      </div>

      <!-- 快速上传表单 -->
      <div v-if="showUploadForm" class="quick-upload-card slide-in">
        <h3 class="upload-title">📸 快速上传年夜饭照片</h3>

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
            <p class="upload-limit">支持 JPG、PNG 格式，最多3张</p>
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

        <div class="upload-form-fields">
          <div class="form-group">
            <label class="form-label">您的昵称</label>
            <input
              v-model="uploadForm.uploaderName"
              type="text"
              class="form-input"
              placeholder="请输入您的昵称"
            >
          </div>

          <div class="form-group">
            <label class="form-label">新年寄语</label>
            <textarea
              v-model="uploadForm.message"
              class="form-textarea"
              placeholder="说点什么吧..."
              rows="2"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="uploadForm.isPublic" type="checkbox">
              <span>公开显示在照片墙</span>
            </label>
          </div>

          <button @click="handleQuickUpload" class="btn btn-primary btn-block" :disabled="uploading || previewImages.length === 0">
            <span v-if="!uploading">🎉 立即上传</span>
            <span v-else>上传中...</span>
          </button>
        </div>
      </div>

      <!-- 上传成功提示 -->
      <div v-if="showUploadSuccess" class="success-message fade-in">
        <div class="success-content">
          <div class="success-icon">🎊</div>
          <h3>上传成功！</h3>
          <p>您的年夜饭照片已添加到照片墙</p>
          <button @click="resetUploadForm" class="btn btn-outline">
            继续上传
          </button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        加载中...
      </div>

      <!-- 照片墙 -->
      <div v-else-if="photos.length > 0" class="gallery masonry">
        <div
          v-for="photo in filteredPhotos"
          :key="photo.id"
          class="photo-card masonry-item"
        >
          <div class="photo-image" @click="openPhoto(photo)">
            <img :src="photo.image_url" :alt="photo.uploader_name + ' 的年夜饭'">
          </div>

          <div class="photo-info">
            <div class="photo-uploader">
              <span class="uploader-avatar">{{ getAvatar(photo.uploader_name) }}</span>
              <span class="uploader-name">{{ photo.uploader_name }}</span>
            </div>

            <div v-if="photo.message" class="photo-message">
              {{ photo.message }}
            </div>

            <div class="photo-footer">
              <span class="photo-time">{{ formatTime(photo.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <p>还没有人上传年夜饭照片</p>
        <p class="empty-hint">快来上传第一张吧！</p>
        <router-link to="/upload" class="btn btn-primary">
          上传年夜饭
        </router-link>
      </div>

      <!-- 加载更多 -->
      <div v-if="!loading && hasMore" class="load-more">
        <button @click="loadMore" class="btn btn-outline">
          加载更多
        </button>
      </div>
    </div>

    <!-- 图片预览弹窗 -->
    <div v-if="selectedPhoto" class="photo-modal" @click="closePhoto">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closePhoto">✕</button>

        <div class="modal-image">
          <img :src="selectedPhoto.image_url" :alt="selectedPhoto.uploader_name + ' 的年夜饭'">
        </div>

        <div class="modal-info">
          <div class="modal-uploader">
            <span class="uploader-avatar">{{ getAvatar(selectedPhoto.uploader_name) }}</span>
            <span class="uploader-name">{{ selectedPhoto.uploader_name }}</span>
          </div>

          <div v-if="selectedPhoto.message" class="modal-message">
            {{ selectedPhoto.message }}
          </div>

          <div class="modal-time">
            {{ formatTime(selectedPhoto.created_at) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getPhotos, uploadPhoto } from '@/services'

const photos = ref([])
const loading = ref(false)
const hasMore = ref(false)
const filter = ref('latest')
const selectedPhoto = ref(null)

// 上传相关
const showUploadForm = ref(false)
const showUploadSuccess = ref(false)
const uploading = ref(false)
const fileInput = ref(null)
const previewImages = ref([])
const selectedFiles = ref([])
const dragging = ref(false)

const uploadForm = ref({
  uploaderName: '',
  message: '',
  isPublic: true
})

const filteredPhotos = computed(() => {
  if (filter.value === 'latest') {
    return [...photos.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  }
  return photos.value
})

const uniqueUploaders = computed(() => {
  const uniqueNames = new Set(photos.value.map(p => p.uploader_name))
  return uniqueNames.size
})

async function loadPhotos() {
  loading.value = true
  try {
    const result = await getPhotos(50)
    if (result.success) {
      photos.value = result.data
      hasMore.value = result.data.length >= 50
    } else {
      alert('加载失败：' + result.error)
    }
  } catch (error) {
    console.error('加载失败:', error)
  } finally {
    loading.value = false
  }
}

function loadMore() {
  // 简化版本，实际应该实现分页
  alert('加载更多功能开发中')
}

function setFilter(newFilter) {
  filter.value = newFilter
}

function openPhoto(photo) {
  selectedPhoto.value = photo
  document.body.style.overflow = 'hidden'
}

function closePhoto() {
  selectedPhoto.value = null
  document.body.style.overflow = ''
}

function getAvatar(name) {
  return name ? name.charAt(0).toUpperCase() : '匿'
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

// ===== 上传相关函数 =====

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
    if (file.size > 5 * 1024 * 1024) {
      alert(`图片 ${file.name} 超过5MB，请选择小一点的图片`)
      return
    }

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

async function handleQuickUpload() {
  if (previewImages.value.length === 0) {
    alert('请至少上传一张图片')
    return
  }

  if (!uploadForm.value.uploaderName.trim()) {
    alert('请输入您的昵称')
    return
  }

  uploading.value = true

  try {
    // 逐个上传图片
    for (const file of selectedFiles.value) {
      const result = await uploadPhoto({
        file,
        uploaderName: uploadForm.value.uploaderName,
        message: uploadForm.value.message,
        isPublic: uploadForm.value.isPublic
      })

      if (!result.success) {
        throw new Error(result.error)
      }
    }

    showUploadSuccess.value = true
    showUploadForm.value = false

    // 重新加载照片列表
    await loadPhotos()
  } catch (error) {
    console.error('上传失败:', error)
    alert('上传失败：' + error.message)
  } finally {
    uploading.value = false
  }
}

function resetUploadForm() {
  previewImages.value = []
  selectedFiles.value = []
  uploadForm.value = {
    uploaderName: '',
    message: '',
    isPublic: true
  }
  showUploadSuccess.value = false
}

onMounted(() => {
  loadPhotos()
})
</script>

<style scoped>
.gallery-page {
  padding: 20px 0;
}

/* 统计栏 */
.stats-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 245, 245, 0.98) 100%);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.1);
  border: 2px solid #d32f2f;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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

/* 操作栏 */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.filter-bar {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.filter-btn {
  padding: 8px 24px;
  border: 2px solid #d32f2f;
  background: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #d32f2f;
}

.filter-btn:hover {
  border-color: #ffd700;
  color: #ff6f00;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.2);
}

.filter-btn.active {
  background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 100%);
  border-color: #ffd700;
  color: white;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
}

/* 快速上传卡片 */
.quick-upload-card {
  background: linear-gradient(135deg, #ffffff 0%, #fff5f5 50%, #ffebee 100%);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 32px;
  border: 3px solid #ffd700;
  box-shadow: 0 8px 24px rgba(211, 47, 47, 0.15);
  position: relative;
  overflow: hidden;
}

.quick-upload-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: repeating-linear-gradient(
    90deg,
    #c0392b 0px,
    #c0392b 30px,
    #ffd700 30px,
    #ffd700 60px
  );
}

.upload-title {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 24px;
  color: #c0392b;
  position: relative;
}

.upload-title::before {
  content: '📸';
  margin-right: 8px;
}

/* 上传区域 */
.upload-area {
  border: 3px dashed #c0392b;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
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
  animation: bounce 2s ease-in-out infinite;
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
  border: 2px solid #ffd700;
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
  background: rgba(211, 47, 47, 0.9);
  color: white;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: #ffd700;
  transform: scale(1.1);
}

.preview-add {
  aspect-ratio: 1;
  border: 2px dashed #c0392b;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fff;
}

.preview-add:hover {
  border-color: #ffd700;
  background: linear-gradient(135deg, #fff5f5 0%, #ffebee 100%);
}

.add-icon {
  font-size: 32px;
  color: #c0392b;
}

.add-text {
  font-size: 14px;
  color: #c0392b;
  margin-top: 8px;
  font-weight: 600;
}

/* 上传表单字段 */
.upload-form-fields {
  max-width: 600px;
  margin: 0 auto;
}

.upload-form-fields .form-group {
  margin-bottom: 20px;
}

.upload-form-fields .form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 700;
  font-size: 15px;
  color: #c0392b;
}

.upload-form-fields .form-input,
.upload-form-fields .form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 15px;
  font-family: inherit;
}

.upload-form-fields .form-input:focus,
.upload-form-fields .form-textarea:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

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

/* 成功消息 */
.success-message {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 3px solid #c3e6cb;
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 32px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.success-content {
  position: relative;
}

.success-icon {
  font-size: 64px;
  margin-bottom: 16px;
  animation: bounce 2s ease-in-out infinite;
}

.success-content h3 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #155724;
}

.success-content p {
  color: #155724;
  margin-bottom: 24px;
  font-size: 16px;
}

/* 照片卡片 */
.photo-card {
  background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 20px;
  border: 2px solid transparent;
}

.photo-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 8px 24px rgba(211, 47, 47, 0.2);
  border-color: #ffd700;
}

.photo-image {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.photo-image::after {
  content: '';
  display: block;
  padding-bottom: 75%; /* 4:3 比例 */
}

.photo-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.photo-card:hover .photo-image img {
  transform: scale(1.05);
}

.photo-info {
  padding: 16px;
}

.photo-uploader {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.uploader-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
  border: 2px solid #ffd700;
}

.uploader-name {
  font-weight: 600;
  color: #d32f2f;
}

.photo-message {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.photo-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.photo-time {
  font-size: 12px;
  color: #999;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-hint {
  color: #999;
  margin-bottom: 24px;
}

/* 加载更多 */
.load-more {
  text-align: center;
  margin-top: 40px;
}

/* 预览弹窗 */
.photo-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  position: relative;
  max-width: 900px;
  width: 100%;
  background: transparent;
  border-radius: 16px;
  overflow: hidden;
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

.modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.modal-image {
  width: 100%;
  background: black;
  border-radius: 12px;
  overflow: hidden;
}

.modal-image img {
  width: 100%;
  height: auto;
  display: block;
}

.modal-info {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-top: 16px;
}

.modal-uploader {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.modal-uploader .uploader-avatar {
  width: 40px;
  height: 40px;
  font-size: 18px;
}

.modal-uploader .uploader-name {
  font-size: 18px;
  font-weight: 600;
}

.modal-message {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.modal-time {
  font-size: 14px;
  color: #999;
}

/* 响应式 */
@media (max-width: 768px) {
  /* 标题和副标题 */
  .title {
    font-size: 28px !important;
  }

  .subtitle {
    font-size: 15px !important;
  }

  /* 统计栏 */
  .stats-bar {
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }

  .stat-value {
    font-size: 28px;
  }

  .stat-label {
    font-size: 13px;
  }

  .stat-divider {
    width: 40px;
    height: 2px;
  }

  /* 操作栏 */
  .action-bar {
    flex-direction: column;
    gap: 16px;
  }

  .filter-bar {
    width: 100%;
    justify-content: center;
  }

  .filter-btn {
    flex: 1;
    padding: 10px 16px;
    font-size: 14px;
  }

  .upload-toggle-btn {
    width: 100%;
    justify-content: center;
    padding: 12px 20px;
  }

  /* 快速上传卡片 */
  .quick-upload-card {
    padding: 20px;
    border-width: 2px;
  }

  .upload-title {
    font-size: 20px;
    margin-bottom: 20px;
  }

  /* 上传区域 */
  .upload-area {
    padding: 20px;
    min-height: 160px;
  }

  .upload-icon {
    font-size: 48px;
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
    gap: 12px;
  }

  .remove-btn {
    width: 24px;
    height: 24px;
    font-size: 14px;
  }

  .add-icon {
    font-size: 24px;
  }

  .add-text {
    font-size: 12px;
  }

  /* 表单字段 */
  .upload-form-fields {
    max-width: 100%;
  }

  .upload-form-fields .form-group {
    margin-bottom: 16px;
  }

  .upload-form-fields .form-label {
    font-size: 14px;
  }

  .upload-form-fields .form-input,
  .upload-form-fields .form-textarea {
    padding: 10px 14px;
    font-size: 14px;
  }

  /* 成功消息 */
  .success-message {
    padding: 24px;
  }

  .success-icon {
    font-size: 48px;
  }

  .success-content h3 {
    font-size: 20px;
  }

  .success-content p {
    font-size: 14px;
  }

  /* 照片墙 */
  .gallery {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .photo-card {
    margin-bottom: 16px;
  }

  .photo-info {
    padding: 12px;
  }

  .uploader-avatar {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .uploader-name {
    font-size: 14px;
  }

  .photo-message {
    font-size: 13px;
  }

  /* 空状态 */
  .empty-state {
    padding: 40px 20px;
  }

  /* 预览弹窗 */
  .photo-modal {
    padding: 10px;
  }

  .modal-content {
    max-width: 100%;
  }

  .modal-close {
    top: -36px;
    right: 10px;
    width: 32px;
    height: 32px;
    font-size: 20px;
  }

  .modal-info {
    padding: 16px;
  }

  .modal-uploader .uploader-avatar {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }

  .modal-uploader .uploader-name {
    font-size: 16px;
  }

  .modal-message {
    font-size: 14px;
  }
}

/* 小屏手机 */
@media (max-width: 480px) {
  .title {
    font-size: 24px !important;
  }

  .subtitle {
    font-size: 14px !important;
  }

  /* 统计栏 */
  .stats-bar {
    padding: 12px;
    margin-bottom: 20px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-label {
    font-size: 12px;
  }

  /* 快速上传卡片 */
  .quick-upload-card {
    padding: 16px;
    border-radius: 16px;
  }

  .upload-title {
    font-size: 18px;
  }

  /* 上传区域 */
  .upload-area {
    padding: 16px;
    min-height: 140px;
    border-width: 2px;
  }

  .upload-icon {
    font-size: 40px;
  }

  /* 预览列表 */
  .preview-list {
    gap: 8px;
  }

  .preview-item {
    border-radius: 8px;
  }

  /* 照片信息 */
  .photo-info {
    padding: 10px;
  }

  .photo-message {
    font-size: 12px;
    margin-bottom: 8px;
  }

  /* 按钮优化 */
  .btn {
    min-height: 44px;
  }
}
</style>
