# 技术设计文档 (TDD)

**项目**: 英语听写练习小程序  
**版本**: v1.0  
**日期**: 2026-03-21

---

## 1. 系统架构

```
┌─────────────────────────────────────────┐
│           微信小程序前端                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │关卡列表 │ │音频播放 │ │扫描识别 │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│  ┌─────────┐ ┌─────────┐               │
│  │对照批改 │ │个人中心 │               │
│  └─────────┘ └─────────┘               │
└─────────────────────────────────────────┘
                   │
┌─────────────────────────────────────────┐
│           微信小程序API                  │
│  - 音频播放 (InnerAudioContext)         │
│  - 相机/相册 (wx.chooseMedia)           │
│  - OCR识别 (wx.serviceMarket)           │
│  - 本地存储 (wx.getStorage)             │
│  - 云开发 (wx.cloud)                    │
└─────────────────────────────────────────┘
                   │
┌─────────────────────────────────────────┐
│           后端服务                       │
│  - 微信云开发 (数据库 + 存储)            │
│  - OCR服务 (腾讯云/百度)                │
│  - 音频文件存储 (云存储)                │
└─────────────────────────────────────────┘
```

---

## 2. 页面结构

```
pages/
├── index/                    # 关卡列表首页
│   ├── index.js
│   ├── index.wxml
│   └── index.wxss
├── player/                   # 音频播放页
│   ├── player.js
│   ├── player.wxml
│   └── player.wxss
├── scan/                     # 扫描识别页
│   ├── scan.js
│   ├── scan.wxml
│   └── scan.wxss
├── compare/                  # 对照批改页
│   ├── compare.js
│   ├── compare.wxml
│   └── compare.wxss
├── result/                   # 结果展示页
│   ├── result.js
│   ├── result.wxml
│   └── result.wxss
└── profile/                  # 个人中心
    ├── profile.js
    ├── profile.wxml
    └── profile.wxss
```

---

## 3. 数据流设计

### 3.1 关卡列表加载
```
用户打开小程序
    ↓
从云数据库获取关卡列表
    ↓
合并本地缓存的进度数据
    ↓
渲染关卡列表
```

### 3.2 音频播放流程
```
用户点击关卡
    ↓
加载关卡详情(音频URL、原文)
    ↓
初始化音频播放器
    ↓
用户播放/暂停/复读操作
    ↓
记录播放次数到本地存储
```

### 3.3 扫描识别流程
```
用户点击"扫描文本"
    ↓
调用相机拍摄/选择图片
    ↓
裁剪/框选识别区域
    ↓
调用OCR服务识别文字
    ↓
显示识别结果(可编辑)
    ↓
用户确认后进入对照页
```

### 3.4 对照批改流程
```
获取原始文本 + 用户识别文本
    ↓
执行文本对比算法
    ↓
计算准确率、错误统计
    ↓
展示对照结果(高亮差异)
    ↓
保存成绩到云端
    ↓
更新用户积分和等级
```

---

## 4. 核心算法

### 4.1 文本对比算法 (Levenshtein Distance)
```javascript
function levenshteinDistance(s1, s2) {
    const m = s1.length, n = s2.length;
    const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
    
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (s1[i-1] === s2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = Math.min(
                    dp[i-1][j] + 1,    // 删除
                    dp[i][j-1] + 1,    // 插入
                    dp[i-1][j-1] + 1   // 替换
                );
            }
        }
    }
    return dp[m][n];
}

function calculateAccuracy(original, user) {
    const distance = levenshteinDistance(original, user);
    const maxLen = Math.max(original.length, user.length);
    return ((maxLen - distance) / maxLen * 100).toFixed(2);
}
```

### 4.2 积分计算公式
```javascript
function calculatePoints(accuracy, playCount, difficulty) {
    // 基础分 = 准确率 * 100
    const basePoints = accuracy;
    
    // 难度系数: easy=1, medium=1.5, hard=2
    const difficultyMultiplier = { easy: 1, medium: 1.5, hard: 2 }[difficulty];
    
    // 熟练度加成: 播放次数越少，加成越高
    const efficiencyBonus = Math.max(0, (10 - playCount) * 5);
    
    return Math.round((basePoints * difficultyMultiplier) + efficiencyBonus);
}
```

---

## 5. API 接口设计

### 5.1 本地存储 Key
```javascript
const STORAGE_KEYS = {
    USER_INFO: 'user_info',           // 用户信息
    LEVELS_PROGRESS: 'levels_progress', // 关卡进度
    PLAY_HISTORY: 'play_history',     // 播放历史
    SETTINGS: 'settings'              // 用户设置
};
```

### 5.2 云数据库集合
```javascript
// levels - 关卡数据
{
    _id: String,
    title: String,
    difficulty: String,  // easy/medium/hard
    duration: Number,
    audioUrl: String,
    originalText: String,
    sentences: Array,
    order: Number
}

// user_records - 用户成绩
{
    _id: String,
    userId: String,
    levelId: String,
    score: Number,
    accuracy: Number,
    playCount: Number,
    userText: String,
    createdAt: Date
}

// user_profiles - 用户档案
{
    _id: String,
    userId: String,
    level: Number,
    totalPoints: Number,
    streakDays: Number,
    lastStudyDate: Date
}
```

---

## 6. 组件设计

### 6.1 音频播放器组件 (audio-player)
```javascript
// 属性
{
    src: String,           // 音频地址
    currentTime: Number,   // 当前时间
    duration: Number,      // 总时长
    isPlaying: Boolean,    // 是否播放中
    loopStart: Number,     // AB复读起点
    loopEnd: Number,       // AB复读终点
    playbackRate: Number   // 播放速度
}

// 事件
{
    onPlay: Function,      // 播放
    onPause: Function,     // 暂停
    onTimeUpdate: Function, // 进度更新
    onEnded: Function      // 播放结束
}
```

### 6.2 扫描组件 (text-scanner)
```javascript
// 属性
{
    mode: String,          // camera/album
    cropEnabled: Boolean   // 是否启用裁剪
}

// 事件
{
    onCapture: Function,   // 拍摄完成
    onRecognize: Function  // 识别完成
}
```

### 6.3 文本对比组件 (text-compare)
```javascript
// 属性
{
    original: String,      // 原文
    userText: String       // 用户文本
}

// 输出
{
    accuracy: Number,      // 准确率
    errors: Array,         // 错误列表
    diffHtml: String       // 差异HTML
}
```

---

## 7. 状态管理

使用全局状态管理用户数据和关卡进度：

```javascript
// app.js
globalData: {
    userInfo: null,
    levels: [],
    currentLevel: null,
    playerState: {
        isPlaying: false,
        currentTime: 0,
        loopMode: false
    }
}
```

---

## 8. 性能优化

1. **音频预加载**: 关卡列表页预加载第一关音频
2. **图片压缩**: 扫描图片压缩至 1080p 以下
3. **分页加载**: 成绩记录分页加载
4. **本地缓存**: 关卡数据本地缓存，减少云请求

---

## 9. 错误处理

| 错误场景 | 处理方案 |
|---------|---------|
| 音频加载失败 | 显示重试按钮，记录错误日志 |
| OCR识别失败 | 提示手动输入，提供文本框 |
| 网络异常 | 本地缓存数据，提示稍后同步 |
| 相机权限拒绝 | 引导用户开启权限，或选择相册 |

---

**文档版本历史**
| 版本 | 日期 | 修改人 | 说明 |
|-----|------|-------|------|
| v1.0 | 2026-03-21 | AI | 初始版本 |
