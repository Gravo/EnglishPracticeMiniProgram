// ============================================
// Breaking Bad 听写练习关卡配置
// Breaking Bad S01E01-S01E07
// ============================================
// 使用说明：
// 复制此配置到 app.js 中的 defaultLevels 数组
// 音频文件放到: assets/audio/breaking_bad/clips/
// 字幕文件放到: assets/audio/breaking_bad/transcripts/

const breakingBadLevels = [
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
      "Nice to meet you. (很高兴认识你。)",
      "See you later. (回头见。)",
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
      "Turn left at the corner. (在拐角左转。)",
      'Go straight for two blocks. (直走两个街区。)',
      "It's next to the pharmacy. (在药店旁边。)",
      'Can you give me directions? (你能告诉我怎么走吗？)'
    ]
  },
  {
    id: 14,
    title: 'Level 14: Breaking Bad - 餐厅',
    titleEn: 'Breaking Bad S01E03 - Restaurant',
    difficulty: 'medium',
    duration: 600,
    audioUrl: '/assets/audio/breaking_bad/clips/03_restaurant.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 80,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 400,
    keywords: ['order', 'menu', 'waiter', 'check', 'delicious'],
    source: 'Breaking Bad S01E03',
    description: '餐厅点餐与日常对话',
    scene: '餐厅场景',
    vocabulary: [
      'Can I take your order? (可以点餐了吗？)',
      "I'll have the steak. (我要牛排。)",
      'What would you recommend? (你推荐什么？)',
      'Could I see the menu? (可以看一下菜单吗？)',
      'The check, please. (买单。)'
    ]
  },
  {
    id: 15,
    title: 'Level 15: Breaking Bad - 医院',
    titleEn: 'Breaking Bad S01E04 - Hospital',
    difficulty: 'medium',
    duration: 600,
    audioUrl: '/assets/audio/breaking_bad/clips/04_hospital.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 75,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 450,
    keywords: ['doctor', 'nurse', 'patient', 'medicine', 'appointment'],
    source: 'Breaking Bad S01E04',
    description: '医院场景，医疗相关词汇',
    scene: '医院与健康',
    vocabulary: [
      'I need to see a doctor. (我需要看医生。)',
      'Take this medicine twice a day. (每天吃两次药。)',
      "When is my appointment? (我的预约是什么时候？)",
      "I'll write you a prescription. (我给你开个处方。)",
      'Do you have any allergies? (你有什么过敏吗？)'
    ]
  },
  {
    id: 16,
    title: 'Level 16: Breaking Bad - 家庭',
    titleEn: 'Breaking Bad S01E05 - Family',
    difficulty: 'medium',
    duration: 600,
    audioUrl: '/assets/audio/breaking_bad/clips/05_family.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 75,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 500,
    keywords: ['family', 'wife', 'kid', 'home', 'love'],
    source: 'Breaking Bad S01E05',
    description: '家庭场景，情感表达',
    scene: '家庭与情感',
    vocabulary: [
      'I love you. (我爱你。)',
      'How was your day? (今天怎么样？)',
      'We need to talk. (我们需要谈谈。)',
      "I'm proud of you. (我为你骄傲。)",
      "Everything will be fine. (一切都会好的。)"
    ]
  },
  {
    id: 17,
    title: 'Level 17: Breaking Bad - 谈判',
    titleEn: 'Breaking Bad S01E06 - Negotiation',
    difficulty: 'hard',
    duration: 600,
    audioUrl: '/assets/audio/breaking_bad/clips/06_negotiation.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 70,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 550,
    keywords: ['deal', 'money', 'business', 'price', 'agreement'],
    source: 'Breaking Bad S01E06',
    description: '商业谈判，高难度表达',
    scene: '商业与谈判',
    vocabulary: [
      "Let's make a deal. (我们来做个交易吧。)",
      "That's not acceptable. (这不能接受。)",
      'We have an agreement. (我们达成协议了。)',
      "Money talks. (有钱能使鬼推磨。)",
      "That's my final offer. (这是我的最终报价。)"
    ]
  },
  {
    id: 18,
    title: 'Level 18: Breaking Bad - 复杂对话',
    titleEn: 'Breaking Bad S01E07 - Complex Dialogue',
    difficulty: 'hard',
    duration: 600,
    audioUrl: '/assets/audio/breaking_bad/clips/07_complex_dialogue.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 70,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 600,
    keywords: ['chemistry', 'science', 'dangerous', 'careful', 'trust'],
    source: 'Breaking Bad S01E07',
    description: '复杂情节，高难度词汇',
    scene: '科学与危险',
    vocabulary: [
      'Chemistry is my specialty. (化学是我的专长。)',
      'This is very dangerous. (这非常危险。)',
      'You need to be careful. (你需要小心。)',
      'Can I trust you? (我能相信你吗？)',
      "I know what I'm doing. (我知道我在做什么。)"
    ]
  }
];

// 导出配置
module.exports = { breakingBadLevels };
