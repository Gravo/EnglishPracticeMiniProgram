# 腾讯混元大模型资源包申请指南

## 资源包内容
- 1亿 Token 资源包
- 1万张生图资源包
- 有效期：6个月
- 适用范围：微信小程序 + 云开发

---

## 申请步骤

### 1. 登录腾讯云
访问 https://cloud.tencent.com/
用微信扫码登录

### 2. 进入混元大模型控制台
1. 搜索"混元大模型"或访问 https://cloud.tencent.com/product/hunyuan
2. 点击"立即使用"
3. 进入控制台

### 3. 领取免费资源包
1. 在控制台找到"资源包"或"免费额度"
2. 点击"领取免费资源包"
3. 确认领取 1亿 Token + 1万张生图

### 4. 获取 API Key
1. 进入"API密钥管理"
2. 点击"新建密钥"
3. 记录 SecretId 和 SecretKey

---

## 在小程序中使用混元

### 云函数调用方式（推荐）

```javascript
// 云函数：hunyuanChat
const cloud = require('wx-server-sdk');
cloud.init();

const { HunyuanClient } = require("@tencentcloud/hunyuan-sdk-nodejs");

exports.main = async (event, context) => {
  const { message } = event;
  
  const client = new HunyuanClient({
    credential: {
      secretId: process.env.HUNYUAN_SECRET_ID,
      secretKey: process.env.HUNYUAN_SECRET_KEY,
    },
    region: "ap-guangzhou",
  });
  
  try {
    const result = await client.ChatCompletions({
      Model: "hunyuan-lite", // 或 hunyuan-standard
      Messages: [
        { Role: "user", Content: message }
      ]
    });
    
    return {
      success: true,
      reply: result.Choices[0].Message.Content
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

## 应用场景

### 1. AI 作文批改
```javascript
// 批改用户听写作文
const prompt = `请批改以下英语作文，指出语法错误并给出修改建议：
${userText}

原文参考：
${originalText}`;
```

### 2. 智能提示
```javascript
// 当用户听写困难时给出提示
const prompt = `用户正在听写关于"${topic}"的内容，请给出3个关键词提示，不要直接给出答案。`;
```

### 3. 生图功能
```javascript
// 根据听写内容生成配图
const prompt = `根据以下英文内容生成一张教育插图：
${text}`;
```

---

## 费用说明

免费额度：
- Token: 1亿个（约可调用 50万次对话）
- 生图: 1万张

超出后：
- hunyuan-lite: 免费（限流）
- hunyuan-standard: 按Token计费
- 生图: 按张计费

---

## 申请链接

直接访问：
https://cloud.tencent.com/act/pro/hunyuan-free

或搜索：腾讯云混元大模型免费额度
