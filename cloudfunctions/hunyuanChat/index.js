// 云函数：hunyuanChat - 腾讯混元大模型对话
const cloud = require('wx-server-sdk');
cloud.init();

// 注意：需要先安装混元SDK
// npm install @tencentcloud/hunyuan-sdk-nodejs

exports.main = async (event, context) => {
  const { 
    message,           // 用户消息
    model = 'hunyuan-lite',  // 模型版本：hunyuan-lite / hunyuan-standard
    temperature = 0.7,  // 温度参数
    maxTokens = 1024   // 最大Token数
  } = event;

  // 从环境变量读取密钥
  const secretId = process.env.HUNYUAN_SECRET_ID || process.env.TENCENT_SECRET_ID;
  const secretKey = process.env.HUNYUAN_SECRET_KEY || process.env.TENCENT_SECRET_KEY;

  if (!secretId || !secretKey) {
    return {
      success: false,
      error: '未配置混元API密钥'
    };
  }

  try {
    // 动态引入SDK（如果没有安装会报错）
    const { HunyuanClient } = require("@tencentcloud/hunyuan-sdk-nodejs");
    
    const client = new HunyuanClient({
      credential: {
        secretId: secretId,
        secretKey: secretKey,
      },
      region: "ap-guangzhou",
    });

    const result = await client.ChatCompletions({
      Model: model,
      Messages: [
        { 
          Role: "system", 
          Content: "你是一个专业的英语教师，擅长批改英语作文和提供学习建议。"
        },
        { 
          Role: "user", 
          Content: message 
        }
      ],
      Temperature: temperature,
      MaxTokens: maxTokens
    });

    return {
      success: true,
      reply: result.Choices[0].Message.Content,
      usage: result.Usage
    };

  } catch (error) {
    console.error('混元调用失败:', error);
    
    // 如果SDK未安装，返回友好提示
    if (error.code === 'MODULE_NOT_FOUND') {
      return {
        success: false,
        error: '请先安装混元SDK: npm install @tencentcloud/hunyuan-sdk-nodejs'
      };
    }
    
    return {
      success: false,
      error: error.message
    };
  }
};
