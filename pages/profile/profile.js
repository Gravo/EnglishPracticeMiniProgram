// pages/profile/profile.js
const app = getApp();

Page({
  data: {
    userInfo: null,
    userLevel: 1,
    totalPoints: 0,
    streakDays: 1,
    completedLevels: 0,
    totalPlayCount: 0,
    avgScore: 0,
    studyDays: 1,
    recentRecords: []
  },

  onLoad() {
    this.loadUserData();
  },

  onShow() {
    this.loadUserData();
  },

  // 加载用户数据
  loadUserData() {
    const levels = app.globalData.levels || [];
    const userInfo = wx.getStorageSync('user_info') || {};
    const records = wx.getStorageSync('score_records') || [];

    // 计算统计数据
    let completedLevels = 0;
    let totalPlayCount = 0;
    let totalScore = 0;
    let scoreCount = 0;

    levels.forEach(level => {
      totalPlayCount += level.playCount || 0;
      if (level.status === 'completed') {
        completedLevels++;
      }
      if (level.bestScore > 0) {
        totalScore += level.bestScore;
        scoreCount++;
      }
    });

    // 计算平均分
    const avgScore = scoreCount > 0 ? Math.round(totalScore / scoreCount) : 0;

    // 计算用户等级
    const totalPoints = userInfo.totalPoints || 0;
    const userLevel = Math.floor(totalPoints / 500) + 1;

    // 格式化最近记录
    const recentRecords = records.slice(-5).reverse().map(record => {
      const level = levels.find(l => l.id === record.levelId) || {};
      return {
        ...record,
        levelTitle: level.title || '关卡 ' + record.levelId,
        date: new Date(record.date).toLocaleDateString()
      };
    });

    this.setData({
      userInfo,
      userLevel,
      totalPoints,
      streakDays: userInfo.streakDays || 1,
      completedLevels,
      totalPlayCount,
      avgScore,
      studyDays: userInfo.studyDays || 1,
      recentRecords
    });
  },

  // 查看全部记录
  viewAllRecords() {
    wx.showToast({ title: '功能开发中', icon: 'none' });
  },

  // 设置
  goToSettings() {
    wx.showToast({ title: '功能开发中', icon: 'none' });
  },

  // 清除数据
  clearData() {
    wx.showModal({
      title: '提示',
      content: '确定要清除所有数据吗？这将重置你的进度和成绩。',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync();
          app.globalData.levels.forEach(level => {
            level.bestScore = 0;
            level.playCount = 0;
            level.status = level.id === 1 ? 'unlocked' : 'locked';
          });
          wx.showToast({ title: '数据已清除', icon: 'success' });
          this.loadUserData();
        }
      }
    });
  },

  // 关于
  about() {
    wx.showModal({
      title: '英语听写练习',
      content: '版本: 1.0.0\n\n基于尚雯婕英语学习法，帮你提升英语听力水平。',
      showCancel: false
    });
  }
});
