// app.js - 小程序入口文件
App({
  onLaunch() {
    // 获取系统信息
    wx.getSystemInfo({
      success: (res) => {
        this.globalData.systemInfo = res;
      }
    });
  },

  globalData: {
    systemInfo: null
  }
});
