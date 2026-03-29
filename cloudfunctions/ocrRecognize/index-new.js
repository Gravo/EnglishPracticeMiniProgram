// 云函数：ocrRecognize - 腾讯云OCR识别（简化版，无SDK依赖）
const cloud = require('wx-server-sdk');
cloud.init();

// 使用HTTPS直接调用API
const https = require('https');
const crypto = require('crypto');

// 签名算法
function signRequest(secretId, secretKey, service, host, payload, timestamp, date) {
  const httpRequestMethod = 'POST';
  const canonicalUri = '/';
  const canonicalQueryString = '';
  const contentType = 'application/json';
  
  const canonicalHeaders = 
    'content-type:' + contentType + '\n' +
    'host:' + host + '\n' +
    'x-tc-action:GeneralBasicOCR\n' +
    'x-tc-region:ap-beijing\n' +
    'x-tc-timestamp:' + timestamp + '\n' +
    'x-tc-version:2018-11-19\n';
  
  const signedHeaders = 'content-type;host;x-tc-action;x-tc-region;x-tc-timestamp;x-tc-version';
  const hashedRequestPayload = crypto.createHash('sha256').update(payload).digest('hex');
  
  const canonicalRequest = 
    httpRequestMethod + '\n' +
    canonicalUri + '\n' +
    canonicalQueryString + '\n' +
    canonicalHeaders + '\n' +
    signedHeaders + '\n' +
    hashedRequestPayload;
  
  const algorithm = 'TC3-HMAC-SHA256';
  const credentialScope = date + '/' + service + '/tc3_request';
  const hashedCanonicalRequest = crypto.createHash('sha256').update(canonicalRequest).digest('hex');
  
  const stringToSign = 
    algorithm + '\n' +
    timestamp + '\n' +
    credentialScope + '\n' +
    hashedCanonicalRequest;
  
  const secretDate = crypto.createHmac('sha256', 'TC3' + secretKey).update(date).digest();
  const secretService = crypto.createHmac('sha256', secretDate).update(service).digest();
  const secretSigning = crypto.createHmac('sha256', secretService).update('tc3_request').digest();
  const signature = crypto.createHmac('sha256', secretSigning).update(stringToSign).digest('hex');
  
  const authorization = 
    algorithm + ' ' +
    'Credential=' + secretId + '/' + credentialScope + ', ' +
    'SignedHeaders=' + signedHeaders + ', ' +
    'Signature=' + signature;
  
  return authorization;
}

exports.main = async (event, context) => {
  const { imageBase64 } = event;
  
  if (!imageBase64) {
    return {
      success: false,
      error: '缺少图片数据'
    };
  }

  const secretId = process.env.TENCENT_SECRET_ID;
  const secretKey = process.env.TENCENT_SECRET_KEY;
  
  if (!secretId || !secretKey) {
    return {
      success: false,
      error: '未配置腾讯云API密钥，请在云开发控制台设置环境变量 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY'
    };
  }

  const host = 'ocr.tencentcloudapi.com';
  const service = 'ocr';
  const timestamp = Math.floor(Date.now() / 1000);
  const date = new Date(timestamp * 1000).toISOString().split('T')[0];
  
  const payload = JSON.stringify({
    ImageBase64: imageBase64,
    LanguageType: 'auto'
  });
  
  const authorization = signRequest(secretId, secretKey, service, host, payload, timestamp, date);
  
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
        try {
          const result = JSON.parse(data);
          
          if (result.Response && result.Response.TextDetections) {
            const text = result.Response.TextDetections
              .map(item => item.DetectedText)
              .join(' ');
            
            resolve({
              success: true,
              text: text,
              confidence: result.Response.TextDetections[0].Confidence
            });
          } else if (result.Response && result.Response.Error) {
            resolve({
              success: false,
              error: result.Response.Error.Message || 'OCR识别失败'
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
      resolve({
        success: false,
        error: '请求失败: ' + error.message
      });
    });
    
    req.write(payload);
    req.end();
  });
};
