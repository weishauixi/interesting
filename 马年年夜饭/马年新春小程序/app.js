// app.js
App({
  onLaunch() {
    // 初始化云开发环境（如果需要）
    console.log('马年新春祝福小程序启动')

    // 检查本地存储
    this.initStorage()
  },

  onShow() {
    // 小程序显示时的逻辑
  },

  initStorage() {
    // 初始化示例数据
    const greetings = wx.getStorageSync('greetings')
    const photos = wx.getStorageSync('photos')

    if (!greetings) {
      // 示例祝福数据
      const sampleGreetings = [
        {
          id: 1,
          templateId: 1,
          message: '龙马精神迎新春，马到成功行大运！愿您在新的一年里身体健康，万事如意！',
          senderName: '小明',
          recipientName: '所有人',
          createdAt: new Date().toISOString()
        },
        {
          id: 2,
          templateId: 2,
          message: '马年大吉！祝您新年快乐，阖家幸福，财源滚滚！',
          senderName: '小红',
          recipientName: '亲朋好友',
          createdAt: new Date(Date.now() - 3600000).toISOString()
        }
      ]
      wx.setStorageSync('greetings', sampleGreetings)
    }

    if (!photos) {
      // 示例照片数据
      const samplePhotos = [
        {
          id: 1,
          imageUrl: 'https://picsum.photos/400/300?random=1',
          uploaderName: '美食家',
          message: '今年年夜饭真丰盛！',
          isPublic: true,
          createdAt: new Date().toISOString()
        }
      ]
      wx.setStorageSync('photos', samplePhotos)
    }
  },

  globalData: {
    userInfo: null
  }
})
