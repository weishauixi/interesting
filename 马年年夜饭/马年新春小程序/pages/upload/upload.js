// pages/upload/upload.js
const storage = require('../../utils/storage.js')

Page({
  data: {
    previewImages: [],
    selectedFiles: [],
    submitting: false,
    form: {
      uploaderName: '',
      message: '',
      isPublic: true
    }
  },

  onLoad() {
    // 页面加载
  },

  chooseImage() {
    const maxCount = 3 - this.data.previewImages.length
    if (maxCount <= 0) {
      wx.showToast({
        title: '最多只能上传3张图片',
        icon: 'none'
      })
      return
    }

    wx.chooseImage({
      count: maxCount,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePaths = res.tempFilePaths

        // 检查文件大小
        tempFilePaths.forEach(filePath => {
          wx.getFileInfo({
            filePath: filePath,
            success: (fileInfo) => {
              if (fileInfo.size > 5 * 1024 * 1024) {
                wx.showToast({
                  title: '图片大小不能超过5MB',
                  icon: 'none'
                })
                return
              }

              // 添加到预览列表
              this.data.previewImages.push(filePath)
              this.setData({
                previewImages: this.data.previewImages
              })
            }
          })
        })
      }
    })
  },

  removeImage(e) {
    const index = e.currentTarget.dataset.index
    this.data.previewImages.splice(index, 1)
    this.setData({
      previewImages: this.data.previewImages
    })
  },

  onUploaderNameInput(e) {
    this.setData({
      'form.uploaderName': e.detail.value
    })
  },

  onMessageInput(e) {
    this.setData({
      'form.message': e.detail.value
    })
  },

  togglePublic() {
    this.setData({
      'form.isPublic': !this.data.form.isPublic
    })
  },

  handleSubmit() {
    if (this.data.previewImages.length === 0) {
      wx.showToast({
        title: '请至少上传一张图片',
        icon: 'none'
      })
      return
    }

    if (!this.data.form.uploaderName.trim()) {
      wx.showToast({
        title: '请输入您的昵称',
        icon: 'none'
      })
      return
    }

    this.setData({ submitting: true })

    // 保存第一张图片到本地存储
    // 注意：实际项目中应该上传到服务器
    const firstImage = this.data.previewImages[0]

    const result = storage.savePhoto({
      imageUrl: firstImage, // 使用临时路径
      uploaderName: this.data.form.uploaderName,
      message: this.data.form.message,
      isPublic: this.data.form.isPublic
    })

    if (result.success) {
      wx.showToast({
        title: '✅ 上传成功！',
        icon: 'success',
        duration: 2000
      })

      setTimeout(() => {
        wx.switchTab({
          url: '/pages/gallery/gallery'
        })
      }, 1500)
    } else {
      wx.showToast({
        title: '上传失败，请重试',
        icon: 'none'
      })
      this.setData({ submitting: false })
    }
  }
})
