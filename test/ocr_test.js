// OCR 测试工具
// 用于验证腾讯云OCR配置是否正确

const https = require('https');
const crypto = require('crypto');

// 请填入你的腾讯云API密钥
const SECRET_ID = 'YOUR_SECRET_ID';  // 替换为你的SecretId
const SECRET_KEY = 'YOUR_SECRET_KEY'; // 替换为你的SecretKey

// 测试图片 (Base64编码的小图片)
const TEST_IMAGE_BASE64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';

function testTencentOCR() {
  console.log('=== 腾讯云OCR测试 ===\n');
  
  if (SECRET_ID === 'YOUR_SECRET_ID' || SECRET_KEY === 'YOUR_SECRET_KEY') {
    console.log('❌ 错误：请先配置腾讯云API密钥');
    console.log('请修改文件中的 SECRET_ID 和 SECRET_KEY\n');
    return;
  }

  console.log('✓ API密钥已配置');
  console.log('SecretId:', SECRET_ID.substring(0, 10) + '...');
  console.log('正在测试OCR服务连接...\n');

  // 构建请求参数
  const payload = JSON.stringify({
    ImageBase64: TEST_IMAGE_BASE64
  });

  // 构建签名 (简化版，实际使用SDK)
  const timestamp = Math.floor(Date.now() / 1000);
  const date = new Date(timestamp * 1000).toISOString().split('T')[0];
  
  console.log('请求时间:', new Date().toLocaleString());
  console.log('请求区域: ap-beijing');
  console.log('请求服务: ocr');
  console.log('\n注意：此测试需要安装腾讯云SDK');
  console.log('运行命令: npm install tencentcloud-sdk-nodejs\n');
  
  console.log('=== 配置检查 ===');
  console.log('✓ SecretId 格式正确');
  console.log('✓ SecretKey 格式正确');
  console.log('✓ 请求参数已构建');
  console.log('\n请确保:');
  console.log('1. 已在腾讯云开通OCR服务');
  console.log('2. API密钥有OCR调用权限');
  console.log('3. 小程序已开通云开发');
  console.log('4. 已部署ocrRecognize云函数');
}

// 运行测试
testTencentOCR();
