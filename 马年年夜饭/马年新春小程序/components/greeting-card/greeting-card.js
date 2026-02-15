// components/greeting-card/greeting-card.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    senderName: {
      type: String,
      value: '匿名'
    },
    recipientName: {
      type: String,
      value: '所有人'
    },
    message: {
      type: String,
      value: ''
    },
    timeAgo: {
      type: String,
      value: '刚刚'
    },
    templateGradient: {
      type: String,
      value: 'linear-gradient(135deg, #d32f2f 0%, #ff6f00 100%)'
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    displayMessage: ''
  },

  /**
   * 组件生命周期
   */
  lifetimes: {
    attached() {
      // 组件加载时设置默认消息
      if (!this.data.message) {
        this.setData({
          displayMessage: '龙马精神迎新春，马到成功行大运！'
        })
      } else {
        this.setData({
          displayMessage: this.data.message
        })
      }
    }
  },

  /**
   * 组件的方法列表
   */
  methods: {
    // 点击卡片触发事件
    onCardTap() {
      this.triggerEvent('tap', {
        senderName: this.data.senderName,
        message: this.data.message
      })
    }
  }
})
