// utils/storage.js - 数据存储工具

/**
 * 获取所有祝福
 */
function getGreetings() {
  try {
    const greetings = wx.getStorageSync('greetings') || []
    return greetings.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
  } catch (e) {
    console.error('获取祝福失败', e)
    return []
  }
}

/**
 * 保存祝福
 */
function saveGreeting(greeting) {
  try {
    const greetings = getGreetings()
    const newGreeting = {
      id: Date.now(),
      createdAt: new Date().toISOString(),
      ...greeting
    }
    greetings.unshift(newGreeting)
    wx.setStorageSync('greetings', greetings)
    return { success: true, id: newGreeting.id }
  } catch (e) {
    console.error('保存祝福失败', e)
    return { success: false, error: e.message }
  }
}

/**
 * 获取所有照片
 */
function getPhotos() {
  try {
    const photos = wx.getStorageSync('photos') || []
    return photos
      .filter(photo => photo.isPublic !== false)
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
  } catch (e) {
    console.error('获取照片失败', e)
    return []
  }
}

/**
 * 保存照片
 */
function savePhoto(photo) {
  try {
    const photos = getPhotos()
    const newPhoto = {
      id: Date.now(),
      createdAt: new Date().toISOString(),
      ...photo
    }
    photos.unshift(newPhoto)
    wx.setStorageSync('photos', photos)
    return { success: true, id: newPhoto.id }
  } catch (e) {
    console.error('保存照片失败', e)
    return { success: false, error: e.message }
  }
}

/**
 * 获取统计数据
 */
function getStats() {
  try {
    const greetings = wx.getStorageSync('greetings') || []
    const photos = wx.getStorageSync('photos') || []
    return {
      greetingsCount: greetings.length,
      photosCount: photos.length
    }
  } catch (e) {
    console.error('获取统计失败', e)
    return { greetingsCount: 0, photosCount: 0 }
  }
}

/**
 * 格式化时间
 */
function formatTime(timestamp) {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date

  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour

  if (diff < minute) return '刚刚'
  if (diff < hour) return Math.floor(diff / minute) + '分钟前'
  if (diff < day) return Math.floor(diff / hour) + '小时前'
  if (diff < 7 * day) return Math.floor(diff / day) + '天前'

  return date.toLocaleDateString('zh-CN')
}

module.exports = {
  getGreetings,
  saveGreeting,
  getPhotos,
  savePhoto,
  getStats,
  formatTime
}
