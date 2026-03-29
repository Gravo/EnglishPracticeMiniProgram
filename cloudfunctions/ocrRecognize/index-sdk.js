// 云函数：ocrRecognize - 使用腾讯云官方SDK
const cloud = require('wx-server-sdk');
cloud.init();

// 使用腾讯云SDK
const tencentcloud = require("tencentcloud-sdk-nodejs");
const OcrClient = tencentcloud.ocr.v20181119.Client;

exports.main = async (event, context) => {
  const { imageBase64 } = event;
  
  if (!imageBase64 || imageBase64 === 'test') {
    return {
      success: false,
      error: '缺少图片数据'
    };
  }

  // 从环境变量读取密钥
  const secretId = process.env.TENCENT_SECRET_ID;
  const secretKey = process.env.TENCENT_SECRET_KEY;
  
  console.log('环境变量检查:');
  console.log('- TENCENT_SECRET_ID:', secretId ? '已设置 (长度:' + secretId.length + ')' : '未设置');
  console.log('- TENCENT_SECRET_KEY:', secretKey ? '已设置 (长度:' + secretKey.length + ')' : '未设置');
  
  if (!secretId || !secretKey) {
    return {
      success: false,
      error: '未配置腾讯云API密钥。请在云开发控制台 → 云函数 → ocrRecognize → 配置 → 环境变量 中设置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY'
    };
  }

  try {
    // 创建OCR客户端
    const client = new OcrClient({
      credential: {
        secretId: secretId,
        secretKey: secretKey,
      },
      region: "ap-beijing",
      profile: {
        signMethod: "TC3-HMAC-SHA256",
        httpProfile: {
          reqMethod: "POST",
          reqTimeout: 30,
        },
      },
    });

    // 调用通用印刷体识别
    const params = {
      ImageBase64: imageBase64,
      LanguageType: "auto",
    };

    console.log('正在调用OCR API...');
    const result = await client.GeneralBasicOCR(params);
    console.log('OCR API返回:', JSON.stringify(result, null, 2));

    if (result.TextDetections && result.TextDetections.length > 0) {
      const text = result.TextDetections
        .map(item => item.DetectedText)
        .join(' ');
      
      return {
        success: true,
        text: text,
        confidence: result.TextDetections[0].Confidence
      };
    } else {
      return {
        success: false,
        error: '未能识别出文字'
      };
    }
  } catch (error) {
    console.error('OCR调用失败:', error);
    return {
      success: false,
      error: error.message || 'OCR服务调用失败'
    };
  }
};
