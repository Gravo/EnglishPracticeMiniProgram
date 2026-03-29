// pages/index/index.js
// ============================================
// 首页 - 整合授权系统 + 本地文件访问
// ============================================
const app = getApp();
const authGuard = require('../../utils/authGuard.js');
const authManager = require('../../utils/authManager.js');

Page({
  data: {
    // 用户信息
    userInfo: null,
    isLoggedIn: false,
    isActivated: false,
    
    // 关卡数据
    levels: [],
    currentLevelId: null,
    
    // 统计数据
    userLevel: 1,
    totalPoints: 0,
    streakDays: 1,
    completedLevels: 0,
    totalLevels: 7,
    
    // 弹窗
    showLocalFileDialog: false,
    localAudioPath: '',
    localTextContent: '',
    
    // 显示登录提示
    showLoginTip: false
  },

  onLoad(options) {
    // 检查授权状态
    this.checkAuth(options);
  },

  onShow() {
    // 每次显示都检查授权
    this.checkAuth();
    this.loadData();
  },

  // 检查授权状态
  checkAuth(options) {
    const status = authManager.checkAuthStatus();
    
    this.setData({
      isLoggedIn: status.isLoggedIn,
      isActivated: status.isLicenseValid,
      userInfo: status.wxUser,
      showLoginTip: !status.isLoggedIn
    });
    
    // 如果需要激活但不在登录页面
    if (!status.isLicenseValid && status.isLoggedIn && !options?.from) {
      // 自动显示激活提示
      setTimeout(() => {
        wx.showModal({
          title: '🎁 激活解锁全部功能',
          content: '输入激活码解锁全部关卡，或使用演示模式体验',
          confirmText: '去激活',
          cancelText: '稍后',
          success: (res) => {
            if (res.confirm) {
              wx.navigateTo({
                url: '/pages/login/login'
              });
            }
          }
        });
      }, 1000);
    }
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

    // 计算用户等级
    const userLevel = Math.floor(totalPoints / 500) + 1;

    this.setData({
      levels,
      userLevel,
      totalPoints,
      completedLevels,
      totalLevels: levels.length
    });
  },

  // 点击关卡
  onLevelTap(e) {
    const levelId = e.currentTarget.dataset.id;
    const level = this.data.levels.find(l => l.id === levelId);
    
    if (!level) {
      wx.showToast({ title: '关卡不存在', icon: 'none' });
      return;
    }
    
    if (level.status === 'locked') {
      wx.showToast({ title: '请先完成上一关', icon: 'none' });
      return;
    }

    this.setData({ currentLevelId: levelId });
    this.startLevel();
  },

  // 开始挑战
  startLevel() {
    if (!this.data.currentLevelId) {
      wx.showToast({ title: '请先选择关卡', icon: 'none' });
      return;
    }

    wx.navigateTo({
      url: `/pages/player/player?levelId=${this.data.currentLevelId}`
    });
  },

  // ============================================
  // 本地文件访问功能
  // ============================================

  // 显示本地文件选择弹窗
  onShowLocalFiles() {
    // 检查授权
    const auth = authGuard.checkPageAuth({ requiredLogin: true, requiredActivation: false });
    if (!auth.allowed) return;

    this.setData({ showLocalFileDialog: true });
  },

  // 关闭弹窗
  onCloseLocalDialog() {
    this.setData({
      showLocalFileDialog: false,
      localAudioPath: '',
      localTextContent: ''
    });
  },

  // 选择本地音频文件
  onChooseAudio() {
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['mp3', 'wav', 'm4a', 'ogg'],
      success: (res) => {
        const file = res.tempFiles[0];
        this.setData({
          localAudioPath: file.name,
          localAudioTempPath: file.path
        });
        wx.showToast({
          title: '已选择: ' + file.name,
          icon: 'none',
          duration: 2000
        });
      },
      fail: (err) => {
        console.error('选择音频失败:', err);
        wx.showToast({ title: '选择失败', icon: 'none' });
      }
    });
  },

  // 选择本地文本文件
  onChooseText() {
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['txt', 'srt', 'lrc', 'json'],
      success: (res) => {
        const file = res.tempFiles[0];
        
        // 读取文件内容
        wx.getFileSystemManager().readFile({
          filePath: file.path,
          encoding: 'utf-8',
          success: (content) => {
            this.setData({
              localTextContent: content.data.substring(0, 500), // 预览前500字
              localTextPath: file.name
            });
            wx.showToast({
              title: '已选择: ' + file.name,
              icon: 'none',
              duration: 2000
            });
          },
          fail: () => {
            wx.showToast({ title: '读取失败', icon: 'none' });
          }
        });
      },
      fail: (err) => {
        console.error('选择文本失败:', err);
        wx.showToast({ title: '选择失败', icon: 'none' });
      }
    });
  },

  // 开始使用本地文件学习
  onStartLocalLearn() {
    if (!this.data.localAudioPath) {
      wx.showToast({ title: '请先选择音频文件', icon: 'none' });
      return;
    }

    // 跳转到播放器，使用本地文件
    wx.navigateTo({
      url: `/pages/player/player?mode=local&audio=${encodeURIComponent(this.data.localAudioPath)}&text=${encodeURIComponent(this.data.localTextContent || '')}`
    });

    this.onCloseLocalDialog();
  },

  // ============================================
  // 跳转到登录
  // ============================================

  onGoToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.checkAuth();
    this.loadData();
    wx.stopPullDownRefresh();
  }
});
