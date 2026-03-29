# Breaking Bad 关卡集成指南

## 快速集成步骤

### 步骤1: 添加音频文件

运行提取脚本：
1. 打开 CMD
2. 切换到目录：
   ```cmd
   cd /d D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad
   ```
3. 运行提取脚本：
   ```cmd
   extract.bat
   ```

### 步骤2: 更新 app.js

在 `app.js` 的 `initLevels()` 函数中，找到 `defaultLevels` 数组，在现有5个关卡后添加 Breaking Bad 的7个关卡：

```javascript
// 在 Level 5 后面添加以下内容:

      {
        id: 12,
        title: 'Level 12: Breaking Bad - 打招呼',
        titleEn: 'Breaking Bad S01E01 - Greetings',
        difficulty: 'easy',
        duration: 600,
        audioUrl: '/assets/audio/breaking_bad/clips/01_greeting.mp3',
        originalText: '',
        sentences: [],
        unlockScore: 85,
        bestScore: 0,
        playCount: 0,
        status: 'locked',
        points: 300,
        keywords: ['yo', "what's up", 'how are you', 'nice to meet', 'later'],
        source: 'Breaking Bad S01E01',
        description: 'Walter和Jesse的经典开场对话，日常问候语',
        scene: '打招呼与日常问候',
        vocabulary: [
          "Yo, what's up? (嘿，怎么了？)",
          "How's it going? (你好吗？)",
          'Nice to meet you. (很高兴认识你。)',
          'See you later. (回头见。)',
          "Can't complain. (还行。)"
        ]
      },
      {
        id: 13,
        title: 'Level 13: Breaking Bad - 问路',
        titleEn: 'Breaking Bad S01E02 - Asking Directions',
        difficulty: 'easy',
        duration: 600,
        audioUrl: '/assets/audio/breaking_bad/clips/02_asking_directions.mp3',
        originalText: '',
        sentences: [],
        unlockScore: 85,
        bestScore: 0,
        playCount: 0,
        status: 'locked',
        points: 350,
        keywords: ['where', 'turn left', 'go straight', 'next to', 'address'],
        source: 'Breaking Bad S01E02',
        description: '问路与指路表达，实用日常英语',
        scene: '问路与方向指引',
        vocabulary: [
          'Where are you going? (你要去哪？)',
          'Turn left at the corner. (在拐角左转。)',
          'Go straight for two blocks. (直走两个街区。)',
          "It's next to the pharmacy. (在药店旁边。)",
          'Can you give me directions? (你能告诉我怎么走吗？)'
        ]
      },
      // ... (继续添加 Level 14-18)
```

### 步骤3: 更新关卡ID

将 Level 5 的 `unlockScore` 从 80 改为 70，让 Level 12 可以被解锁。

---

## 目录结构

```
D:\EnglishPracticeMiniProgram\
├── assets\
│   └── audio\
│       └── breaking_bad\
│           ├── clips\
│           │   ├── 01_greeting.mp3           (10分钟)
│           │   ├── 02_asking_directions.mp3 (10分钟)
│           │   ├── 03_restaurant.mp3         (10分钟)
│           │   ├── 04_hospital.mp3          (10分钟)
│           │   ├── 05_family.mp3             (10分钟)
│           │   ├── 06_negotiation.mp3        (10分钟)
│           │   └── 07_complex_dialogue.mp3   (10分钟)
│           ├── transcripts\
│           │   ├── 01_greeting.txt
│           │   ├── 02_asking_directions.txt
│           │   └── ...
│           └── vocabulary.md
├── config\
│   └── breaking_bad_levels.js    (完整关卡配置)
├── app.js                       (需要更新)
└── docs\
    └── BREAKING_BAD_INTEGRATION.md
```

---

## 完整关卡配置

完整的关卡配置已保存在：
`D:\EnglishPracticeMiniProgram\config\breaking_bad_levels.js`

可以直接复制其中的 `breakingBadLevels` 数组到 `app.js`。

---

## 验证清单

- [ ] 音频文件已提取到 `clips\` 目录
- [ ] 7个 MP3 文件大小正确（每个约 7-10 MB）
- [ ] `app.js` 已更新，包含新的关卡配置
- [ ] 小程序可正常编译
- [ ] 音频播放功能正常
