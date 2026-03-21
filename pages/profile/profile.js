// pages/profile/profile.js
const app = getApp();

Page({
  data: {
    userInfo: {},
    isLoggedIn: false,
    userLevel: 1,
    totalStats: {
      words: 0,
      listening: 0,
      reading: 0,
      days: 0
    }
  },

  onShow() {
    this.checkLoginStatus();
    this.loadStats();
  },

  // 检查登录状态
  checkLoginStatus() {
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.setData({
        userInfo: userInfo,
        isLoggedIn: true
      });
    }
  },

  // 加载统计数据
  loadStats() {
    try {
      const allStats = wx.getStorageSync('all_stats') || {};
      this.setData({ totalStats: allStats });
    } catch (e) {
      console.error('加载统计数据失败', e);
    }
  },

  // 登录
  login() {
    // 实际项目中调用 wx.login 获取用户信息
    wx.showLoading({ title: '登录中...' });
    
    setTimeout(() => {
      const mockUserInfo = {
        nickName: '英语学习者',
        avatarUrl: ''
      };
      
      wx.setStorageSync('userInfo', mockUserInfo);
      
      this.setData({
        userInfo: mockUserInfo,
        isLoggedIn: true
      });
      
      wx.hideLoading();
      wx.showToast({ title: '登录成功', icon: 'success' });
    }, 1000);
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('userInfo');
          this.setData({
            userInfo: {},
            isLoggedIn: false
          });
          wx.showToast({ title: '已退出登录' });
        }
      }
    });
  },

  // 跳转设置
  goToSettings() {
    wx.navigateTo({ url: '/pages/settings/settings' });
  },

  // 跳转学习记录
  goToRecords() {
    wx.navigateTo({ url: '/pages/records/records' });
  },

  // 跳转收藏夹
  goToFavorites() {
    wx.navigateTo({ url: '/pages/favorites/favorites' });
  },

  // 跳转关于
  goToAbout() {
    wx.navigateTo({ url: '/pages/about/about' });
  }
});
