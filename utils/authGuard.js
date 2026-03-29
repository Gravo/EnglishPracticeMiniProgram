// utils/authGuard.js
// ============================================
// 页面守卫 - 确保用户已登录和激活
// ============================================

const authManager = require('./authManager.js');

// 页面守卫配置
const GUARD_CONFIG = {
  // 需要登录的页面
  loginRequired: [
    '/pages/index/index',
    '/pages/player/player',
    '/pages/scan/scan',
    '/pages/compare/compare',
    '/pages/profile/profile'
  ],
  
  // 需要激活的页面
  activationRequired: [
    '/pages/player/player',
    '/pages/scan/scan',
    '/pages/compare/compare'
  ],
  
  // 公开页面（无需登录）
  publicPages: [
    '/pages/login/login',
    '/pages/index/index' // 首页部分内容公开
  ]
};

// 检查页面是否需要登录
function isLoginRequired(path) {
  return GUARD_CONFIG.loginRequired.some(p => path.startsWith(p));
}

// 检查页面是否需要激活
function isActivationRequired(path) {
  return GUARD_CONFIG.activationRequired.some(p => path.startsWith(p));
}

// 主守卫函数
function authGuard(path) {
  const status = authManager.checkAuthStatus();
  
  // 如果未登录，跳转到登录页
  if (!status.isLoggedIn) {
    return {
      allowed: false,
      redirect: '/pages/login/login',
      reason: 'need_login'
    };
  }
  
  // 如果未激活，跳转到登录页（激活页面）
  if (!status.isLicenseValid && isActivationRequired(path)) {
    return {
      allowed: false,
      redirect: '/pages/login/login?from=' + encodeURIComponent(path),
      reason: 'need_activate'
    };
  }
  
  return {
    allowed: true
  };
}

// 小程序全局守卫（App.js 中使用）
function onAppAuthGuard() {
  // 不拦截任何路由，让用户自由访问
  // 页面级别的守卫在各自的 onLoad 中调用 checkAuth
}

// 页面守卫 Hook（在需要保护的页面的 onLoad 中调用）
function checkPageAuth(options = {}) {
  const { 
    requiredLogin = true,
    requiredActivation = true,
    redirectToLogin = true
  } = options;
  
  const status = authManager.checkAuthStatus();
  
  // 检查登录
  if (requiredLogin && !status.isLoggedIn) {
    if (redirectToLogin) {
      wx.showModal({
        title: '请先登录',
        content: '登录后即可使用全部功能',
        confirmText: '去登录',
        cancelText: '返回',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/login/login'
            });
          }
        }
      });
    }
    return { allowed: false, reason: 'need_login' };
  }
  
  // 检查激活
  if (requiredActivation && !status.isLicenseValid) {
    if (redirectToLogin) {
      wx.showModal({
        title: '请先激活',
        content: '输入激活码解锁全部功能',
        confirmText: '去激活',
        cancelText: '试用',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/login/login?mode=activate'
            });
          }
        }
      });
    }
    return { allowed: false, reason: 'need_activate' };
  }
  
  return { 
    allowed: true,
    status,
    user: status.wxUser,
    license: status.license
  };
}

// 简化版守卫（用于装饰页面）
function withAuth(options = {}) {
  return function(target, key, descriptor) {
    const originalOnLoad = descriptor.value;
    
    descriptor.value = function(...args) {
      const auth = checkPageAuth(options);
      if (!auth.allowed) {
        // 如果不允许访问，不执行后续逻辑
        return;
      }
      // 执行原来的 onLoad
      return originalOnLoad.apply(this, args);
    };
    
    return descriptor;
  };
}

// 生成授权状态信息
function getAuthDisplayInfo() {
  const status = authManager.checkAuthStatus();
  
  if (status.isLicenseValid) {
    const expiresIn = Math.ceil((status.license.expires - Date.now()) / (24 * 60 * 60 * 1000));
    return {
      isValid: true,
      user: status.wxUser?.nickName || '用户',
      expiresText: expiresIn > 30 ? '永久' : `剩余 ${expiresIn} 天`,
      level: calculateUserLevel()
    };
  }
  
  return {
    isValid: false,
    user: status.wxUser?.nickName || '未登录',
    expiresText: '未激活'
  };
}

// 计算用户等级
function calculateUserLevel() {
  const progress = wx.getStorageSync('levels_progress') || [];
  let totalScore = 0;
  progress.forEach(p => {
    totalScore += p.bestScore || 0;
  });
  return Math.floor(totalScore / 500) + 1;
}

module.exports = {
  authGuard,
  checkPageAuth,
  withAuth,
  getAuthDisplayInfo,
  isLoginRequired,
  isActivationRequired,
  GUARD_CONFIG
};
