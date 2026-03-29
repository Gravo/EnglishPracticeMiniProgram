# OCR 配置指南

## 方案一：腾讯云 OCR（推荐）

### 1. 注册腾讯云账号
访问 https://cloud.tencent.com/ 注册账号

### 2. 开通 OCR 服务
1. 登录腾讯云控制台
2. 搜索"文字识别"进入 OCR 控制台
3. 点击"立即使用"开通服务
4. 选择"通用印刷体识别"或"英文识别"

### 3. 获取 API 密钥
1. 进入"访问管理" → "API密钥管理"
2. 点击"新建密钥"
3. 记录 SecretId 和 SecretKey

### 4. 小程序端配置
在 `pages/scan/scan.js` 中替换以下代码：

```javascript
// 腾讯云 OCR 配置
const tencentOCR = {
  secretId: 'YOUR_SECRET_ID',
  secretKey: 'YOUR_SECRET_KEY',
  region: 'ap-beijing', // 根据你的地区选择
  service: 'ocr'
};

// 调用腾讯云 OCR
async function recognizeWithTencentCloud(imageBase64) {
  const timestamp = Math.floor(Date.now() / 1000);
  
  // 构建请求参数
  const params = {
    ImageBase64: imageBase64,
    LanguageType: 'auto' // 自动识别语言
  };
  
  // 发送请求到腾讯云 OCR API
  // 注意：实际调用需要通过云函数或后端转发，避免暴露密钥
  
  return new Promise((resolve, reject) => {
    wx.cloud.callFunction({
      name: 'ocrRecognize',
      data: {
        imageBase64: imageBase64
      },
      success: res => resolve(res.result),
      fail: err => reject(err)
    });
  });
}
```

### 5. 创建云函数
在微信开发者工具中：
1. 右键点击 `cloudfunctions` 文件夹
2. 选择"新建 Node.js 云函数"
3. 命名为 `ocrRecognize`

云函数代码 (`index.js`)：
```javascript
const cloud = require('wx-server-sdk');
const tencentcloud = require('tencentcloud-sdk-nodejs');

cloud.init();

const OcrClient = tencentcloud.ocr.v20181119.Client;

exports.main = async (event, context) => {
  const { imageBase64 } = event;
  
  const clientConfig = {
    credential: {
      secretId: process.env.TENCENT_SECRET_ID,
      secretKey: process.env.TENCENT_SECRET_KEY,
    },
    region: 'ap-beijing',
    profile: {
      signMethod: 'TC3-HMAC-SHA256',
      httpProfile: {
        reqMethod: 'POST',
        reqTimeout: 30,
      },
    },
  };
  
  const client = new OcrClient(clientConfig);
  
  try {
    const params = {
      ImageBase64: imageBase64,
    };
    
    const result = await client.GeneralBasicOCR(params);
    
    // 提取识别出的文字
    const text = result.TextDetections.map(item => item.DetectedText).join(' ');
    
    return {
      success: true,
      text: text
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
};
```

---

## 方案二：百度 AI OCR

### 1. 注册百度 AI 账号
访问 https://ai.baidu.com/ 注册

### 2. 创建应用
1. 进入"文字识别"控制台
2. 点击"创建应用"
3. 记录 API Key 和 Secret Key

### 3. 小程序端配置
```javascript
// 百度 OCR 配置
const baiduOCR = {
  apiKey: 'YOUR_API_KEY',
  secretKey: 'YOUR_SECRET_KEY'
};

// 获取 Access Token
async function getBaiduAccessToken() {
  const url = `https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${baiduOCR.apiKey}&client_secret=${baiduOCR.secretKey}`;
  
  return new Promise((resolve, reject) => {
    wx.request({
      url: url,
      method: 'POST',
      success: res => resolve(res.data.access_token),
      fail: reject
    });
  });
}

// 调用百度 OCR
async function recognizeWithBaidu(imageBase64) {
  const accessToken = await getBaiduAccessToken();
  const url = `https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=${accessToken}`;
  
  return new Promise((resolve, reject) => {
    wx.request({
      url: url,
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: {
        image: imageBase64,
        language_type: 'ENG' // 英文识别
      },
      success: res => {
        if (res.data.words_result) {
          const text = res.data.words_result.map(item => item.words).join(' ');
          resolve(text);
        } else {
          reject(new Error('识别失败'));
        }
      },
      fail: reject
    });
  });
}
```

---

## 方案三：微信 OCR 插件（最简单）

### 1. 申请插件
1. 登录微信小程序后台
2. 进入"设置" → "第三方设置" → "插件管理"
3. 点击"添加插件"
4. 搜索 "微信OCR" 或 "OCR识别"
5. 申请使用

### 2. 配置 app.json
```json
{
  "plugins": {
    "ocr-plugin": {
      "version": "1.0.0",
      "provider": "wx4418c1d031224693"
    }
  }
}
```

### 3. 使用插件
```javascript
// 在 scan.js 中
const plugin = requirePlugin('ocr-plugin');

plugin.ocr({
  imgPath: this.data.imageSrc,
  success: (res) => {
    console.log('识别结果:', res.text);
    this.setData({ recognizedText: res.text });
  },
  fail: (err) => {
    console.error('识别失败:', err);
  }
});
```

---

## 推荐方案

| 方案 | 优点 | 缺点 | 适用场景 |
|-----|------|------|---------|
| 腾讯云 OCR | 准确率高，支持英文 | 需要云函数 | 生产环境 |
| 百度 OCR | 免费额度多 | 需要后端转发 | 生产环境 |
| 微信插件 | 最简单，无需配置 | 准确率一般 | 快速测试 |

**建议**：先用微信插件快速测试，再用腾讯云/百度 OCR 上线生产环境。
