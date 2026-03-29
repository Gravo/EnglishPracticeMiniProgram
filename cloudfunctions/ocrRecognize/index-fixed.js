// 云函数：ocrRecognize - 腾讯云OCR识别
const cloud = require('wx-server-sdk');
cloud.init();

exports.main = async (event, context) => {
  const { imageBase64 } = event;
  
  if (!imageBase64) {
    return {
      success: false,
      error: '缺少图片数据'
    };
  }

  // 从环境变量读取密钥
  const secretId = process.env.TENCENT_SECRET_ID;
  const secretKey = process.env.TENCENT_SECRET_KEY;
  
  if (!secretId || !secretKey) {
    return {
      success: false,
      error: '未配置腾讯云API密钥，请在云开发控制台设置环境变量 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY'
    };
  }

  try {
    // 使用云开发的 HTTP 请求能力调用腾讯云API
    const result = await callTencentOCR(imageBase64, secretId, secretKey);
    return result;
  } catch (error) {
    console.error('OCR调用失败:', error);
    return {
      success: false,
      error: error.message || 'OCR服务调用失败'
    };
  }
};

// 调用腾讯云OCR API
async function callTencentOCR(imageBase64, secretId, secretKey) {
  const https = require('https');
  const crypto = require('crypto');
  
  const host = 'ocr.tencentcloudapi.com';
  const service = 'ocr';
  const region = 'ap-beijing';
  const action = 'GeneralBasicOCR';
  const version = '2018-11-19';
  const timestamp = Math.floor(Date.now() / 1000);
  const date = new Date(timestamp * 1000).toISOString().split('T')[0];
  
  const payload = JSON.stringify({
    ImageBase64: imageBase64,
    LanguageType: 'auto'
  });
  
  // TC3-HMAC-SHA256 签名
  const authorization = getAuthorization({
    secretId,
    secretKey,
    host,
    service,
    region,
    action,
    version,
    timestamp,
    date,
    payload
  });
  
  return new Promise((resolve, reject) => {
    const options = {
      hostname: host,
      port: 443,
      path: '/',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': host,
        'Authorization': authorization,
        'X-TC-Action': action,
        'X-TC-Version': version,
        'X-TC-Timestamp': timestamp.toString(),
        'X-TC-Region': region
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          console.log('OCR API响应:', JSON.stringify(result, null, 2));
          
          if (result.Response && result.Response.Error) {
            resolve({
              success: false,
              error: result.Response.Error.Message || 'OCR识别失败'
            });
          } else if (result.Response && result.Response.TextDetections) {
            const text = result.Response.TextDetections
              .map(item => item.DetectedText)
              .join(' ');
            
            resolve({
              success: true,
              text: text,
              confidence: result.Response.TextDetections[0].Confidence
            });
          } else {
            resolve({
              success: false,
              error: '未能识别出文字'
            });
          }
        } catch(e) {
          resolve({
            success: false,
            error: '解析响应失败: ' + e.message
          });
        }
      });
    });
    
    req.on('error', (error) => {
      reject(new Error('请求失败: ' + error.message));
    });
    
    req.write(payload);
    req.end();
  });
}

// TC3-HMAC-SHA256 签名算法
function getAuthorization({ secretId, secretKey, host, service, region, action, version, timestamp, date, payload }) {
  const algorithm = 'TC3-HMAC-SHA256';
  
  // 步骤1：拼接规范请求串
  const httpRequestMethod = 'POST';
  const canonicalUri = '/';
  const canonicalQueryString = '';
  const contentType = 'application/json';
  
  const canonicalHeaders = [
    `content-type:${contentType}`,
    `host:${host}`,
    `x-tc-action:${action.toLowerCase()}`,
    `x-tc-region:${region}`,
    `x-tc-timestamp:${timestamp}`,
    `x-tc-version:${version}`,
    ''
  ].join('\n');
  
  const signedHeaders = 'content-type;host;x-tc-action;x-tc-region;x-tc-timestamp;x-tc-version';
  const hashedRequestPayload = sha256(payload);
  
  const canonicalRequest = [
    httpRequestMethod,
    canonicalUri,
    canonicalQueryString,
    canonicalHeaders,
    signedHeaders,
    hashedRequestPayload
  ].join('\n');
  
  // 步骤2：拼接待签名字符串
  const credentialScope = `${date}/${service}/tc3_request`;
  const hashedCanonicalRequest = sha256(canonicalRequest);
  
  const stringToSign = [
    algorithm,
    timestamp,
    credentialScope,
    hashedCanonicalRequest
  ].join('\n');
  
  // 步骤3：计算签名
  const secretDate = hmacSha256(`TC3${secretKey}`, date);
  const secretService = hmacSha256(secretDate, service);
  const secretSigning = hmacSha256(secretService, 'tc3_request');
  const signature = hmacSha256(secretSigning, stringToSign, 'hex');
  
  // 步骤4：拼接Authorization
  const authorization = `${algorithm} Credential=${secretId}/${credentialScope}, SignedHeaders=${signedHeaders}, Signature=${signature}`;
  
  return authorization;
}

function sha256(message) {
  const crypto = require('crypto');
  return crypto.createHash('sha256').update(message).digest('hex');
}

function hmacSha256(key, message, outputFormat = 'buffer') {
  const crypto = require('crypto');
  const hmac = crypto.createHmac('sha256', key).update(message);
  if (outputFormat === 'hex') {
    return hmac.digest('hex');
  }
  return hmac.digest();
}
