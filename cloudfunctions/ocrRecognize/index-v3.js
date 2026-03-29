// 云函数：ocrRecognize - 腾讯云OCR识别
// 使用云开发的 HTTP 访问服务调用腾讯云API

const cloud = require('wx-server-sdk');
cloud.init();

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
  
  console.log('SecretId:', secretId ? '已配置' : '未配置');
  console.log('SecretKey:', secretKey ? '已配置' : '未配置');
  
  if (!secretId || !secretKey) {
    return {
      success: false,
      error: '未配置腾讯云API密钥，请在云开发控制台设置环境变量 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY'
    };
  }

  try {
    // 使用云开发的 request 能力
    const result = await recognizeText(imageBase64, secretId, secretKey);
    return result;
  } catch (error) {
    console.error('OCR调用失败:', error);
    return {
      success: false,
      error: error.message || 'OCR服务调用失败'
    };
  }
};

// 文字识别函数
async function recognizeText(imageBase64, secretId, secretKey) {
  // 使用腾讯云API的签名V3版本
  const timestamp = Math.floor(Date.now() / 1000);
  const date = new Date(timestamp * 1000).toISOString().split('T')[0];
  
  const payload = {
    ImageBase64: imageBase64,
    LanguageType: 'auto'
  };
  
  const payloadStr = JSON.stringify(payload);
  
  // 构建签名
  const auth = signRequest({
    secretId,
    secretKey,
    service: 'ocr',
    host: 'ocr.tencentcloudapi.com',
    region: 'ap-beijing',
    action: 'GeneralBasicOCR',
    version: '2018-11-19',
    timestamp,
    date,
    payload: payloadStr
  });
  
  // 发送请求
  return new Promise((resolve, reject) => {
    const https = require('https');
    
    const options = {
      hostname: 'ocr.tencentcloudapi.com',
      port: 443,
      path: '/',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'ocr.tencentcloudapi.com',
        'Authorization': auth,
        'X-TC-Action': 'GeneralBasicOCR',
        'X-TC-Version': '2018-11-19',
        'X-TC-Timestamp': timestamp.toString(),
        'X-TC-Region': 'ap-beijing'
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        console.log('API响应:', data);
        try {
          const result = JSON.parse(data);
          
          if (result.Response && result.Response.Error) {
            resolve({
              success: false,
              error: result.Response.Error.Message
            });
          } else if (result.Response && result.Response.TextDetections) {
            const text = result.Response.TextDetections
              .map(item => item.DetectedText)
              .join(' ');
            resolve({
              success: true,
              text: text
            });
          } else {
            resolve({
              success: false,
              error: '识别失败'
            });
          }
        } catch (e) {
          reject(new Error('解析失败: ' + e.message));
        }
      });
    });
    
    req.on('error', (e) => {
      reject(new Error('请求失败: ' + e.message));
    });
    
    req.write(payloadStr);
    req.end();
  });
}

// TC3-HMAC-SHA256 签名
function signRequest({ secretId, secretKey, service, host, region, action, version, timestamp, date, payload }) {
  const crypto = require('crypto');
  
  // 1. 构建规范请求
  const httpRequestMethod = 'POST';
  const canonicalUri = '/';
  const canonicalQueryString = '';
  const contentType = 'application/json';
  
  const canonicalHeaders = `content-type:${contentType}\nhost:${host}\nx-tc-action:${action.toLowerCase()}\nx-tc-region:${region}\nx-tc-timestamp:${timestamp}\nx-tc-version:${version}\n`;
  
  const signedHeaders = 'content-type;host;x-tc-action;x-tc-region;x-tc-timestamp;x-tc-version';
  const hashedPayload = crypto.createHash('sha256').update(payload).digest('hex');
  
  const canonicalRequest = `${httpRequestMethod}\n${canonicalUri}\n${canonicalQueryString}\n${canonicalHeaders}\n${signedHeaders}\n${hashedPayload}`;
  
  // 2. 构建待签名字符串
  const algorithm = 'TC3-HMAC-SHA256';
  const credentialScope = `${date}/${service}/tc3_request`;
  const hashedCanonicalRequest = crypto.createHash('sha256').update(canonicalRequest).digest('hex');
  
  const stringToSign = `${algorithm}\n${timestamp}\n${credentialScope}\n${hashedCanonicalRequest}`;
  
  // 3. 计算签名
  const kDate = crypto.createHmac('sha256', `TC3${secretKey}`).update(date).digest();
  const kService = crypto.createHmac('sha256', kDate).update(service).digest();
  const kSigning = crypto.createHmac('sha256', kService).update('tc3_request').digest();
  const signature = crypto.createHmac('sha256', kSigning).update(stringToSign).digest('hex');
  
  // 4. 构建Authorization
  return `${algorithm} Credential=${secretId}/${credentialScope}, SignedHeaders=${signedHeaders}, Signature=${signature}`;
}
