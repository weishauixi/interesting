// pages/greeting/greeting.js
const storage = require('../../utils/storage.js')

Page({
  data: {
    templates: [
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
    ],
    selectedTemplate: 1,
    selectedTemplateGradient: '',
    selectedTemplateEmoji: '',
    form: {
      senderName: '',
      recipientName: '所有人',
      message: '龙马精神迎新春，马到成功行大运！愿您在新的一年里身体健康，万事如意，阖家幸福！'
    },
    displayMessage: '',
    submitting: false,
    currentDate: ''
  },

  onLoad() {
    // 设置当前日期
    const now = new Date()
    const dateStr = now.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })

    // 初始化选中的模板信息
    this.updateTemplateInfo()

    this.setData({
      currentDate: dateStr
    })
  },

  // 更新模板信息
  updateTemplateInfo() {
    const template = this.data.templates.find(t => t.id === this.data.selectedTemplate)
    const gradient = template ? template.gradient : this.data.templates[0].gradient
    const emoji = template ? template.emoji : '🐴'

    this.setData({
      selectedTemplateGradient: gradient,
      selectedTemplateEmoji: emoji,
      displayMessage: this.data.form.message || '龙马精神迎新春，马到成功行大运！愿您在新的一年里身体健康，万事如意，阖家幸福！'
    })
  },

  selectTemplate(e) {
    const id = e.currentTarget.dataset.id
    this.setData({
      selectedTemplate: id
    }, () => {
      this.updateTemplateInfo()
    })
  },

  onSenderNameInput(e) {
    this.setData({
      'form.senderName': e.detail.value
    })
  },

  onRecipientNameInput(e) {
    this.setData({
      'form.recipientName': e.detail.value
    })
  },

  onMessageInput(e) {
    this.setData({
      'form.message': e.detail.value,
      displayMessage: e.detail.value || '龙马精神迎新春，马到成功行大运！愿您在新的一年里身体健康，万事如意，阖家幸福！'
    })
  },

  handleSubmit() {
    if (!this.data.form.message.trim()) {
      wx.showToast({
        title: '请输入祝福语',
        icon: 'none'
      })
      return
    }

    this.setData({ submitting: true })

    const result = storage.saveGreeting({
      templateId: this.data.selectedTemplate,
      message: this.data.form.message,
      senderName: this.data.form.senderName || '匿名',
      recipientName: this.data.form.recipientName || '所有人',
      backgroundStyle: 'gradient'
    })

    if (result.success) {
      wx.showToast({
        title: '祝福发送成功！',
        icon: 'success',
        duration: 2000
      })

      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    } else {
      wx.showToast({
        title: '发送失败，请重试',
        icon: 'none'
      })
      this.setData({ submitting: false })
    }
  }
})
