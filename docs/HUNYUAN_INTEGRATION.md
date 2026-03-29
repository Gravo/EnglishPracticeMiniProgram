# 混元大模型接入方案

## 接入点一：智能批改助手

### 功能描述
用户完成听写后，AI不仅指出错误，还能解释语法问题和改进建议。

### Prompt模板
```
你是一位专业的英语教师。请对以下学生的听写进行批改：

【原文】
{original_text}

【学生听写】
{student_text}

【错误位置】
{error_positions}

请提供：
1. 总体评价（鼓励性）
2. 每个错误的详细解释（语法/拼写/听力）
3. 改进建议
4. 相关知识点讲解

输出格式为JSON：
{
  "overall": "总体评价",
  "errors": [
    {
      "position": "错误位置",
      "type": "错误类型",
      "explanation": "详细解释",
      "suggestion": "改进建议"
    }
  ],
  "tips": "学习建议"
}
```

### 预估Token消耗
- 单次调用: ~500 tokens
- 月活1000用户: 50万 tokens

---

## 接入点二：AI听力材料生成

### 功能描述
根据用户水平和兴趣，自动生成定制化听力材料。

### Prompt模板
```
请生成一段英语听力材料：

【难度等级】{level} (1-5)
【主题偏好】{topic}
【时长要求】{duration}秒
【词汇范围】{vocabulary_level}

要求：
1. 内容有趣且符合主题
2. 语速适中，适合听写
3. 包含{word_count}个单词
4. 句子结构清晰

请输出：
1. 英文原文
2. 中文翻译
3. 关键词汇表（含音标）
4. 句子分割（每句一行）
5. TTS朗读提示（重音、停顿标记）
```

### 预估Token消耗
- 单次生成: ~1000 tokens
- 月生成100篇: 10万 tokens

---

## 接入点三：AI对话练习

### 功能描述
基于听力材料，生成对话场景进行口语练习。

### Prompt模板
```
基于以下听力材料，创建一个对话练习场景：

【听力材料】
{listening_material}

【场景设定】
{scenario_description}

请生成：
1. 对话背景介绍
2. 5轮对话内容（中英文对照）
3. 关键句型讲解
4. 角色扮演提示

要求对话自然，符合听力材料主题。
```

### 预估Token消耗
- 单次对话: ~800 tokens
- 月活500用户: 40万 tokens

---

## 接入点四：个性化学习报告

### 功能描述
分析用户学习数据，生成个性化学习建议。

### Prompt模板
```
请分析以下学生的学习数据，生成个性化建议：

【学习数据】
- 总练习次数: {total_practice}
- 平均准确率: {avg_accuracy}%
- 常见错误类型: {error_types}
- 学习时长: {study_time}
- 薄弱知识点: {weak_points}

请生成：
1. 学习总结（鼓励性）
2. 薄弱环节分析
3. 针对性练习建议
4. 下周学习计划
5. 预计达到目标时间

输出格式为Markdown，适合展示在小程序中。
```

### 预估Token消耗
- 单次报告: ~600 tokens
- 周活1000用户: 24万 tokens/周

---

## Token使用汇总

| 功能 | 单次Token | 月调用量 | 月Token消耗 |
|------|----------|---------|------------|
| 智能批改 | 500 | 1000 | 50万 |
| 材料生成 | 1000 | 100 | 10万 |
| 对话练习 | 800 | 500 | 40万 |
| 学习报告 | 600 | 4000 | 240万 |
| **总计** | - | - | **340万** |

---

## 混元生图使用场景

### 1. 关卡封面图
```
生成一张关于{主题}的教育插画，风格简洁现代，适合作为小程序关卡封面。
主题：{中国古代四大发明/古希腊文明/美国独立宣言/联合国/冷战}
尺寸：750x400像素
风格：扁平化插画，蓝色主色调
```

### 2. 成就徽章
```
生成一个{成就名称}的徽章图标，
风格：游戏化徽章，金色边框，
元素：{星星/奖杯/书本/耳机等}，
背景：透明或纯色
```

### 3. 分享卡片
```
生成一张学习成果分享图，
包含：分数{display_score}，等级{display_level}，
风格：激励性，社交媒体友好，
尺寸：适合微信朋友圈分享
```

---

## 技术接入代码示例

### 调用混元API
```javascript
// 调用混元大模型
async function callHunyuan(prompt) {
  const result = await wx.cloud.callFunction({
    name: 'hunyuanChat',
    data: {
      messages: [
        { role: 'user', content: prompt }
      ]
    }
  });
  
  return result.data.response;
}

// 智能批改示例
async function aiCorrect(original, student) {
  const prompt = `你是一位专业的英语教师...`;
  const result = await callHunyuan(prompt);
  return JSON.parse(result);
}
```

### 云函数示例
```javascript
// cloudfunctions/hunyuanChat/index.js
const cloud = require('wx-server-sdk');
cloud.init();

exports.main = async (event) => {
  const { messages } = event;
  
  // 调用混元API
  const response = await callHunyuanAPI(messages);
  
  return {
    response: response
  };
};
```
