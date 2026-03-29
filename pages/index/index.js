// pages/index/index.js
const app = getApp();

Page({
  data: {
    userInfo: null,
    userLevel: 1,
    totalPoints: 0,
    streakDays: 1,
    completedLevels: 0,
    totalLevels: 7,
    currentLevelId: null,
    levels: []
  },

  onLoad() {
    this.loadData();
  },

  onShow() {
    this.loadData();
  },

  // 加载数据
  loadData() {
    const appData = app.globalData;
    const levels = appData.levels || [];
    
    // 计算统计数据
    let completedLevels = 0;
    let totalPoints = 0;
    
    levels.forEach(level => {
      if (level.bestScore > 0) {
        completedLevels++;
        totalPoints += level.bestScore;
      }
    });

    // 计算用户等级 (每500积分升一级)
    const userLevel = Math.floor(totalPoints / 500) + 1;

    // 加载用户信息
    const userInfo = appData.userInfo || {};

    this.setData({
      userInfo,
      userLevel,
      totalPoints,
      completedLevels,
      totalLevels: levels.length,
      levels
    });
  },

  // 点击关卡
  onLevelTap(e) {
    const levelId = e.currentTarget.dataset.id;
    const level = this.data.levels.find(l => l.id === levelId);
    
    if (!level) {
      wx.showToast({
        title: '关卡不存在',
        icon: 'none'
      });
      return;
    }
    
    if (level.status === 'locked') {
      wx.showToast({
        title: '请先完成上一关',
        icon: 'none'
      });
      return;
    }

    this.setData({
      currentLevelId: levelId
    });

    // 直接开始
    this.startLevel();
  },

  // 开始挑战
  startLevel() {
    if (!this.data.currentLevelId) {
      wx.showToast({
        title: '请先选择关卡',
        icon: 'none'
      });
      return;
    }

    wx.navigateTo({
      url: `/pages/player/player?levelId=${this.data.currentLevelId}`
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadData();
    wx.stopPullDownRefresh();
  }
});
