// OCR 测试脚本
// 在微信开发者工具控制台运行测试

async function testOCR() {
  console.log('=== OCR 云函数测试 ===\n');
  
  // 测试1: 检查云函数是否存在
  console.log('1. 检查云函数...');
  try {
    const functions = await wx.cloud.callFunction({
      name: 'ocrRecognize',
      data: { test: true }
    });
    console.log('✓ 云函数可调用');
  } catch(e) {
    console.log('✗ 云函数调用失败:', e.message);
    return;
  }
  
  // 测试2: 测试空数据
  console.log('\n2. 测试空数据...');
  try {
    const result = await wx.cloud.callFunction({
      name: 'ocrRecognize',
      data: {}
    });
    console.log('结果:', result.result);
    if (result.result.error && result.result.error.includes('缺少图片数据')) {
      console.log('✓ 空数据检测正常');
    }
  } catch(e) {
    console.log('✗ 测试失败:', e.message);
  }
  
  // 测试3: 测试环境变量
  console.log('\n3. 测试环境变量...');
  try {
    const result = await wx.cloud.callFunction({
      name: 'ocrRecognize',
      data: { imageBase64: 'test' }
    });
    console.log('结果:', result.result);
    if (result.result.error && result.result.error.includes('未配置')) {
      console.log('⚠ 环境变量未配置，请在云开发控制台设置');
    } else if (result.result.success) {
      console.log('✓ 环境变量已配置');
    }
  } catch(e) {
    console.log('✗ 测试失败:', e.message);
  }
  
  console.log('\n=== 测试完成 ===');
}

// 运行测试
testOCR();
