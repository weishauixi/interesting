// pages/home/home.js
const storage = require('../../utils/storage.js')

Page({
  data: {
    greetings: [],
    stats: null,
    loading: false
  },

  onLoad() {
    this.loadData()
  },

  onShow() {
    // 页面显示时重新加载数据
    this.loadData()
  },

  loadData() {
    this.setData({ loading: true })

    try {
      // 加载祝福和统计数据
      const greetings = storage.getGreetings().slice(0, 6)
      const stats = storage.getStats()

      // 格式化时间
      const greetingsWithTime = greetings.map(g => ({
        ...g,
        timeAgo: storage.formatTime(g.createdAt)
      }))

      this.setData({
        greetings: greetingsWithTime,
        stats: stats,
        loading: false
      })
    } catch (error) {
      console.error('加载数据失败:', error)
      this.setData({ loading: false })
    }
  },

  goToGreeting() {
    wx.navigateTo({
      url: '/pages/greeting/greeting'
    })
  },

  goToGallery() {
    wx.switchTab({
      url: '/pages/gallery/gallery'
    })
  },

  goToUpload() {
    wx.switchTab({
      url: '/pages/upload/upload'
    })
  }
})
