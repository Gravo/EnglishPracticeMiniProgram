// config.js - OCR配置
// 请将你的腾讯云API密钥填入此处

const OCR_CONFIG = {
  // 腾讯云OCR配置
  tencent: {
    secretId: '', // 填写你的SecretId
    secretKey: '', // 填写你的SecretKey
    region: 'ap-beijing'
  },
  
  // 当前使用的OCR方案: 'mock' | 'tencent' | 'baidu' | 'wechat'
  currentProvider: 'mock'
};

// 切换OCR方案的函数
function switchOCRProvider(provider) {
  const validProviders = ['mock', 'tencent', 'baidu', 'wechat'];
  if (validProviders.includes(provider)) {
    OCR_CONFIG.currentProvider = provider;
    console.log(`OCR方案已切换为: ${provider}`);
  } else {
    console.error('无效的OCR方案');
  }
}

module.exports = {
  OCR_CONFIG,
  switchOCRProvider
};
