# Breaking Bad 智能音频提取策略

## 问题分析

当前策略的问题：
1. **时间戳固定**：从固定时间点（120s, 300s等）提取，不对应实际对话
2. **内容不匹配**：提取的音频与关卡主题（问路、餐厅等）无关
3. **字幕是示例**：transcripts/ 下的文件是编写的示例，不是真实字幕

## 改进策略：基于语义的关键片段提取

### 第一步：关键词匹配

从真实SRT字幕中搜索主题相关关键词：

```
问路场景关键词：
- where, direction, way to, how do I get, turn left/right
- straight, corner, block, street, address, lost

餐厅场景关键词：
- order, menu, food, eat, restaurant, bill, check
- steak, chicken, drink, waiter, delicious

医院场景关键词：
- doctor, hospital, sick, pain, medicine, prescription
- cancer, appointment, nurse, treatment

家庭场景关键词：
- family, son, wife, home, love, school
- Walter Jr, Skyler, dinner, birthday

谈判场景关键词：
- deal, money, business, price, agreement
- product, delivery, partner, trust
```

### 第二步：片段评分算法

```javascript
function scoreSegment(segment, keywords) {
  let score = 0;
  
  // 关键词匹配得分
  keywords.forEach(keyword => {
    if (segment.text.toLowerCase().includes(keyword)) {
      score += 10;
    }
  });
  
  // 对话长度得分（太短或太长都不好）
  const duration = segment.endTime - segment.startTime;
  if (duration >= 3 && duration <= 15) {
    score += 5; // 理想长度 3-15秒
  }
  
  // 对话完整性得分（有问有答）
  if (segment.text.includes('?') && segment.text.includes('.')) {
    score += 3; // 可能是完整对话
  }
  
  // 人物对话得分（排除旁白/独白）
  if (segment.speakers && segment.speakers.length >= 2) {
    score += 5; // 多人对话
  }
  
  return score;
}
```

### 第三步：智能片段组合

```javascript
function combineSegments(segments, targetDuration = 600) {
  // 按时间排序
  segments.sort((a, b) => a.startTime - b.startTime);
  
  // 选择高分片段，确保不重叠
  const selected = [];
  let currentDuration = 0;
  
  for (const seg of segments) {
    // 检查是否与已选片段重叠
    const overlap = selected.some(s => 
      (seg.startTime >= s.startTime && seg.startTime <= s.endTime) ||
      (seg.endTime >= s.startTime && seg.endTime <= s.endTime)
    );
    
    if (!overlap && seg.score > 20) { // 只选高分片段
      selected.push(seg);
      currentDuration += (seg.endTime - seg.startTime);
      
      // 添加过渡静音（0.5秒）
      currentDuration += 0.5;
    }
    
    if (currentDuration >= targetDuration) break;
  }
  
  return selected;
}
```

### 第四步：音频处理流程

```bash
# 1. 提取多个片段
ffmpeg -i input.mkv -ss 120 -t 8 -vn -b:a 64k fragment1.mp3
ffmpeg -i input.mkv -ss 450 -t 12 -vn -b:a 64k fragment2.mp3
ffmpeg -i input.mkv -ss 890 -t 6 -vn -b:a 64k fragment3.mp3

# 2. 创建片段列表文件
echo "file 'fragment1.mp3'" > list.txt
echo "file 'fragment2.mp3'" >> list.txt
echo "file 'fragment3.mp3'" >> list.txt

# 3. 合并片段
ffmpeg -f concat -i list.txt -c copy combined.mp3
```

## 具体实施步骤

### 1. 字幕解析脚本

```python
# parse_srt.py
import re
from datetime import timedelta

def parse_srt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析字幕块
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n((?:.|\n)+?)(?=\n\n|\Z)'
    matches = re.findall(pattern, content)
    
    subtitles = []
    for match in matches:
        index, start, end, text = match
        subtitles.append({
            'index': int(index),
            'start': time_to_seconds(start),
            'end': time_to_seconds(end),
            'text': text.strip().replace('\n', ' ')
        })
    
    return subtitles

def time_to_seconds(time_str):
    # 00:01:23,456 -> 83.456
    h, m, s = time_str.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
```

### 2. 场景分类配置

```javascript
// scene_keywords.js
const sceneKeywords = {
  asking_directions: {
    keywords: ['where', 'direction', 'way to', 'how do i get', 'turn left', 
               'turn right', 'go straight', 'corner', 'block', 'street', 
               'address', 'lost', 'find', 'looking for'],
    minScore: 15,
    targetDuration: 600
  },
  restaurant: {
    keywords: ['order', 'menu', 'food', 'eat', 'restaurant', 'bill', 'check',
               'steak', 'chicken', 'drink', 'waiter', 'waitress', 'delicious',
               'table', 'reservation', 'special'],
    minScore: 15,
    targetDuration: 600
  },
  hospital: {
    keywords: ['doctor', 'hospital', 'sick', 'pain', 'medicine', 'prescription',
               'cancer', 'appointment', 'nurse', 'treatment', 'symptom',
               'diagnosis', 'examination', 'emergency'],
    minScore: 15,
    targetDuration: 600
  },
  family: {
    keywords: ['family', 'son', 'wife', 'home', 'love', 'school', 'dinner',
               'birthday', 'honey', 'dear', 'kids', 'children', 'parent'],
    minScore: 15,
    targetDuration: 600
  },
  negotiation: {
    keywords: ['deal', 'money', 'business', 'price', 'agreement', 'product',
               'delivery', 'partner', 'trust', 'offer', 'contract', 'pay'],
    minScore: 15,
    targetDuration: 600
  },
  chemistry: {
    keywords: ['chemistry', 'science', 'meth', 'cook', 'formula', 'lab',
               'chemical', 'reaction', 'purity', 'crystal', 'equipment'],
    minScore: 15,
    targetDuration: 600
  }
};
```

### 3. 完整提取流程

```javascript
// extract_by_scene.js
const fs = require('fs');
const { execSync } = require('child_process');

function extractScene(sceneName, videoFile, srtFile, outputFile) {
  // 1. 解析字幕
  const subtitles = parseSRT(srtFile);
  
  // 2. 获取场景关键词配置
  const config = sceneKeywords[sceneName];
  
  // 3. 评分并排序
  const scored = subtitles.map(sub => ({
    ...sub,
    score: scoreSegment(sub, config.keywords)
  })).filter(sub => sub.score >= config.minScore)
    .sort((a, b) => b.score - a.score);
  
  // 4. 选择不重叠的片段
  const selected = combineSegments(scored, config.targetDuration);
  
  // 5. 提取音频片段
  const fragments = [];
  selected.forEach((seg, i) => {
    const fragFile = `temp_${sceneName}_${i}.mp3`;
    const cmd = `ffmpeg -i "${videoFile}" -ss ${seg.start} -t ${seg.end - seg.start} -vn -b:a 64k -ac 1 -y "${fragFile}"`;
    execSync(cmd);
    fragments.push(fragFile);
  });
  
  // 6. 合并片段
  const listFile = `temp_${sceneName}_list.txt`;
  fs.writeFileSync(listFile, fragments.map(f => `file '${f}'`).join('\n'));
  const mergeCmd = `ffmpeg -f concat -i "${listFile}" -c copy "${outputFile}"`;
  execSync(mergeCmd);
  
  // 7. 清理临时文件
  fragments.forEach(f => fs.unlinkSync(f));
  fs.unlinkSync(listFile);
  
  // 8. 生成新的字幕文件
  generateNewSRT(selected, outputFile.replace('.mp3', '.txt'));
  
  console.log(`✓ ${sceneName}: 提取完成`);
  console.log(`  片段数: ${selected.length}`);
  console.log(`  总时长: ${selected.reduce((sum, s) => sum + (s.end - s.start), 0)}秒`);
}
```

## 优势对比

| 方面 | 原策略 | 新策略 |
|------|--------|--------|
| **内容匹配** | ❌ 随机提取 | ✅ 语义匹配 |
| **主题一致性** | ❌ 不保证 | ✅ 关键词驱动 |
| **学习价值** | ❌ 可能包含无关内容 | ✅ 聚焦场景对话 |
| **字幕同步** | ❌ 时间不匹配 | ✅ 精确对应 |
| **来源标记** | ❌ 无 | ✅ 记录原始时间戳 |

## 下一步

需要我：
1. 编写完整的字幕解析和提取脚本？
2. 先分析S01E01-S01E07的真实字幕内容？
3. 为每个场景找出最佳片段？
