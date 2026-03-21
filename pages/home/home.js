// pages/home/home.js
const app = getApp();

Page({
  data: {
    todayStats: {
      words: 0,
      listening: 0,
      reading: 0,
      streak: 0
    },
    dailySentence: {
      en: "The only way to do great work is to love what you do.",
      cn: "成就伟大事业的唯一途径是热爱自己所做的事。"
    }
  },

  onLoad() {
    this.loadTodayStats();
  },

  onShow() {
    // 每次显示页面时刷新数据
    this.loadTodayStats();
  },

  // 加载今日学习数据
  loadTodayStats() {
    try {
      const stats = wx.getStorageSync('today_stats') || {};
      this.setData({
        todayStats: stats
      });
    } catch (e) {
      console.error('加载统计数据失败', e);
    }
  },

  // 跳转背单词
  goToVocabulary() {
    wx.switchTab({
      url: '/pages/vocabulary/vocabulary'
    });
  },

  // 跳转听力练习
  goToListening() {
    wx.switchTab({
      url: '/pages/listening/listening'
    });
  },

  // 跳转阅读
  goToReading() {
    wx.switchTab({
      url: '/pages/reading/reading'
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadTodayStats();
    wx.stopPullDownRefresh();
  }
});
