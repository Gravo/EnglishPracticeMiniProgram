// pages/login/login.js
// 登录页面
const authManager = require('../../utils/authManager.js');

Page({
  data: {
    // 登录状态
    hasLogin: false,
    userInfo: null,
    
    // 授权状态
    authStatus: 'need_login', // need_login | need_activate | active | expired
    licenseInfo: null,
    
    // 激活码相关
    licenseCode: '',
    showActivateDialog: false,
    isActivating: false,
    activateError: '',
    
    // 用户协议
    agreedToTerms: false,
    showTerms: false
  },

  onLoad() {
    this.checkStatus();
  },

  onShow() {
    this.checkStatus();
  },

  // 检查登录和授权状态
  checkStatus() {
    const status = authManager.checkAuthStatus();
    this.setData({
      hasLogin: status.isLoggedIn,
      userInfo: status.wxUser,
      authStatus: status.isLicenseValid ? 'active' : (status.isLoggedIn ? 'need_activate' : 'need_login'),
      licenseInfo: status.license
    });
  },

  // 微信一键登录
  async onWxLogin() {
    if (!this.data.agreedToTerms) {
      wx.showModal({
        title: '请先同意用户协议',
        content: '登录即表示您同意我们的用户协议和隐私政策',
        confirmText: '同意',
        cancelText: '查看协议',
        success: (res) => {
          if (res.confirm) {
            this.setData({ agreedToTerms: true });
            this.doWxLogin();
          } else {
            this.onShowTerms();
          }
        }
      });
      return;
    }

    await this.doWxLogin();
  },

  // 执行微信登录
  async doWxLogin() {
    wx.showLoading({ title: '登录中...' });

    const result = await authManager.wxLoginAndGetUserInfo();

    wx.hideLoading();

    if (result.success) {
      this.setData({
        hasLogin: true,
        userInfo: result.userInfo,
        authStatus: 'need_activate' // 需要激活
      });

      wx.showToast({
        title: '登录成功',
        icon: 'success'
      });

      // 检查是否有已激活的码
      const status = authManager.checkAuthStatus();
      if (status.isLicenseValid) {
        wx.switchTab({ url: '/pages/index/index' });
      }
    } else {
      wx.showModal({
        title: '登录失败',
        content: result.error || '请稍后重试',
        showCancel: false
      });
    }
  },

  // 显示激活码弹窗
  onShowActivate() {
    this.setData({
      showActivateDialog: true,
      licenseCode: '',
      activateError: ''
    });
  },

  // 关闭激活码弹窗
  onCloseActivate() {
    this.setData({ showActivateDialog: false });
  },

  // 输入激活码
  onLicenseInput(e) {
    this.setData({
      licenseCode: e.detail.value.toUpperCase()
    });
  },

  // 提交激活码
  async onSubmitLicense() {
    const code = this.data.licenseCode.trim();
    
    if (!code) {
      this.setData({ activateError: '请输入激活码' });
      return;
    }

    this.setData({
      isActivating: true,
      activateError: ''
    });

    wx.showLoading({ title: '验证中...' });

    const result = await authManager.verifyLicenseCode(code, this.data.userInfo);

    wx.hideLoading();
    this.setData({ isActivating: false });

    if (result.valid) {
      this.setData({
        showActivateDialog: false,
        authStatus: 'active',
        licenseInfo: result
      });

      wx.showModal({
        title: '激活成功',
        content: `欢迎使用！\n用户: ${result.user}\n有效期至: ${new Date(result.expires).toLocaleDateString()}`,
        showCancel: false,
        success: () => {
          wx.switchTab({ url: '/pages/index/index' });
        }
      });
    } else {
      this.setData({ activateError: result.error || '激活失败' });
    }
  },

  // 跳过激活（演示模式）
  onSkipActivate() {
    // 使用演示码自动激活
    authManager.verifyLicenseCode('BBDEMO-2024-FREE', this.data.userInfo).then(result => {
      if (result.valid) {
        this.setData({
          showActivateDialog: false,
          authStatus: 'active',
          licenseInfo: result
        });
        wx.switchTab({ url: '/pages/index/index' });
      }
    });
  },

  // 切换用户协议勾选
  onAgreeTerms(e) {
    this.setData({
      agreedToTerms: e.detail.value.length > 0
    });
  },

  // 显示用户协议
  onShowTerms() {
    this.setData({ showTerms: true });
  },

  // 关闭用户协议
  onCloseTerms() {
    this.setData({ showTerms: false });
  },

  // 退出登录
  onLogout() {
    wx.showModal({
      title: '确认退出',
      content: '退出后将清除本地登录信息，但保留激活码',
      success: (res) => {
        if (res.confirm) {
          authManager.logout();
          this.setData({
            hasLogin: false,
            userInfo: null,
            authStatus: 'need_login'
          });
        }
      }
    });
  }
});
