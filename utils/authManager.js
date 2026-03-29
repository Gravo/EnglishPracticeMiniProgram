// utils/authManager.js
// ============================================
// 授权管理系统 - 支持微信登录 + 本地激活码
// ============================================

const AUTH_CONFIG = {
  // 激活码有效期（毫秒） 30天
  LICENSE_VALIDITY: 30 * 24 * 60 * 60 * 1000,
  
  // 激活码盐值（生产环境应放在服务端）
  SALT: 'BB_License_2024',
  
  // 演示激活码（仅用于测试）
  DEMO_CODES: [
    'BBDEMO-2024-FREE',
    'BBTEST-12345678'
  ]
};

// 激活码格式验证
function validateCodeFormat(code) {
  if (!code || typeof code !== 'string') return false;
  
  // 格式: XXXX-XXXX-XXXX-XXXX 或纯数字
  const patterns = [
    /^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/,
    /^[A-Z0-9]{8,32}$/,
    /^\d{8,16}$/
  ];
  
  return patterns.some(p => p.test(code.toUpperCase()));
}

// 生成激活码校验和
function generateChecksum(code) {
  let sum = 0;
  const salt = AUTH_CONFIG.SALT;
  for (let i = 0; i < code.length; i++) {
    sum += code.charCodeAt(i) * (i + 1);
    sum += salt.charCodeAt(i % salt.length);
  }
  return (sum % 97 + 1).toString().padStart(2, '0');
}

// 验证激活码（本地验证 + 服务器验证）
async function verifyLicenseCode(code, wxUserInfo) {
  if (!validateCodeFormat(code)) {
    return { valid: false, error: '激活码格式不正确' };
  }
  
  // 1. 先检查演示激活码
  if (AUTH_CONFIG.DEMO_CODES.includes(code.toUpperCase())) {
    return {
      valid: true,
      type: 'demo',
      expires: Date.now() + AUTH_CONFIG.LICENSE_VALIDITY,
      user: '演示用户'
    };
  }
  
  // 2. 本地校验（格式 + 校验和）
  const codeUpper = code.toUpperCase();
  const stored = wx.getStorageSync('license_info') || {};
  
  // 如果是已激活的码
  if (stored.code === codeUpper && stored.checksum) {
    const expectedChecksum = generateChecksum(codeUpper + stored.salt);
    if (stored.checksum === expectedChecksum) {
      if (stored.expires > Date.now()) {
        return {
          valid: true,
          type: stored.type || 'local',
          expires: stored.expires,
          user: wxUserInfo?.nickName || '本地用户'
        };
      } else {
        return { valid: false, error: '激活码已过期' };
      }
    }
  }
  
  // 3. 尝试验证新码（模拟服务器验证）
  // 实际应该调用服务器 API 验证
  try {
    const result = await callServerVerifyAPI(codeUpper, wxUserInfo);
    if (result.valid) {
      // 保存激活信息
      const licenseInfo = {
        code: codeUpper,
        checksum: generateChecksum(codeUpper + result.salt),
        salt: result.salt,
        type: result.type,
        expires: result.expires,
        user: wxUserInfo?.nickName,
        activatedAt: Date.now()
      };
      wx.setStorageSync('license_info', licenseInfo);
    }
    return result;
  } catch (e) {
    console.error('激活码验证失败:', e);
    return { valid: false, error: '验证失败，请稍后重试' };
  }
}

// 模拟服务器验证（实际应调用云函数）
async function callServerVerifyAPI(code, wxUserInfo) {
  // 这里应该调用你的后端 API 验证激活码
  // 示例：
  // const res = await wx.cloud.callFunction({
  //   name: 'verifyLicense',
  //   data: { code, wxUserInfo }
  // });
  
  // 演示：如果是特定码，直接通过
  if (code.startsWith('BB')) {
    return {
      valid: true,
      type: 'premium',
      salt: Date.now().toString(36),
      expires: Date.now() + AUTH_CONFIG.LICENSE_VALIDITY
    };
  }
  
  return { valid: false, error: '激活码无效' };
}

// 检查授权状态
function checkAuthStatus() {
  const license = wx.getStorageSync('license_info') || {};
  const wxLogin = wx.getStorageSync('wx_user_info') || null;
  
  const isLicenseValid = license.expires > Date.now();
  const isLoggedIn = !!wxLogin;
  
  return {
    isLoggedIn,
    isLicenseValid,
    license,
    wxUser: wxLogin,
    canUse: isLoggedIn && isLicenseValid,
    status: isLicenseValid ? 'active' : (isLoggedIn ? 'need_activate' : 'need_login')
  };
}

// 获取微信登录凭证
function getWxLoginCode() {
  return new Promise((resolve, reject) => {
    wx.login({
      success: (res) => {
        if (res.code) {
          resolve(res.code);
        } else {
          reject(new Error('获取登录凭证失败'));
        }
      },
      fail: reject
    });
  });
}

// 微信登录并获取用户信息
async function wxLoginAndGetUserInfo() {
  try {
    // 1. 获取登录凭证
    const code = await getWxLoginCode();
    
    // 2. 获取用户信息（需要用户授权）
    const userInfo = await getUserProfile();
    
    // 3. 保存登录信息
    wx.setStorageSync('wx_user_info', userInfo);
    wx.setStorageSync('wx_login_code', code);
    wx.setStorageSync('wx_login_time', Date.now());
    
    return {
      success: true,
      userInfo,
      code
    };
  } catch (e) {
    console.error('微信登录失败:', e);
    return {
      success: false,
      error: e.message || '登录失败'
    };
  }
}

// 获取用户信息（新版 API）
function getUserProfile() {
  return new Promise((resolve, reject) => {
    wx.getUserProfile({
      desc: '用于提供个性化学习服务',
      success: (res) => {
        resolve({
          nickName: res.userInfo.nickName,
          avatarUrl: res.userInfo.avatarUrl,
          gender: res.userInfo.gender,
          country: res.userInfo.country,
          province: res.userInfo.province,
          city: res.userInfo.city,
          language: res.userInfo.language
        });
      },
      fail: (e) => {
        // 如果用户拒绝授权，返回基本信息
        resolve({
          nickName: '微信用户',
          avatarUrl: '',
          gender: 0,
          country: '',
          province: '',
          city: ''
        });
      }
    });
  });
}

// 清除登录状态
function logout() {
  wx.removeStorageSync('wx_user_info');
  wx.removeStorageSync('wx_login_code');
  wx.removeStorageSync('wx_login_time');
  // 保留 license_info，不清除激活码
}

// 清除所有数据
function clearAllData() {
  wx.clearStorageSync();
}

module.exports = {
  verifyLicenseCode,
  checkAuthStatus,
  wxLoginAndGetUserInfo,
  getWxLoginCode,
  validateCodeFormat,
  generateChecksum,
  logout,
  clearAllData,
  AUTH_CONFIG
};
