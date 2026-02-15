// pages/gallery/gallery.js
const storage = require('../../utils/storage.js')

Page({
  data: {
    photos: [],
    loading: false,
    uniqueUploaders: 0
  },

  onLoad() {
    this.loadPhotos()
  },

  onShow() {
    // 页面显示时重新加载
    this.loadPhotos()
  },

  loadPhotos() {
    this.setData({ loading: true })

    try {
      const photos = storage.getPhotos()

      // 处理数据
      const processedPhotos = photos.map(photo => ({
        ...photo,
        avatar: photo.uploaderName ? photo.uploaderName.charAt(0).toUpperCase() : '匿',
        timeAgo: storage.formatTime(photo.createdAt)
      }))

      // 计算唯一上传者数量
      const uniqueNames = new Set(photos.map(p => p.uploaderName))

      this.setData({
        photos: processedPhotos,
        uniqueUploaders: uniqueNames.size,
        loading: false
      })
    } catch (error) {
      console.error('加载失败:', error)
      this.setData({ loading: false })
    }
  },

  previewPhoto(e) {
    const photo = e.currentTarget.dataset.photo
    const urls = this.data.photos.map(p => p.imageUrl)
    const current = photo.imageUrl

    wx.previewImage({
      urls: urls,
      current: current
    })
  },

  onPullDownRefresh() {
    this.loadPhotos()
    wx.stopPullDownRefresh()
  }
})
