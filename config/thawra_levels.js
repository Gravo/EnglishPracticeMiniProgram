// 小程序关卡配置 - The Dig Thawra 播客内容
// 复制到 app.js 中的 defaultLevels 数组

const thawraLevels = [
  {
    id: 6,
    title: 'Level 6: 纳赛尔时代与1967年战争',
    titleEn: 'The Nasser Era and the 1967 War',
    difficulty: 'hard',
    duration: 1200, // 20分钟
    audioUrl: '/assets/audio/level_6_nasser_era.mp3',
    originalText: '', // 待填写：使用语音识别生成
    sentences: [], // 待填写：按句子拆分
    unlockScore: 70,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 350,
    keywords: ['Nasser', 'Suez Crisis', 'Six-Day War', 'Israel', 'Egypt'],
    source: 'The Dig - Thawra Podcast, Ep.14',
    description: '巴勒斯坦革命与1967年战争，纳赛尔时期的阿拉伯民族主义'
  },
  {
    id: 7,
    title: 'Level 7: 1973年赎罪日战争',
    titleEn: 'The 1973 Yom Kippur War',
    difficulty: 'hard',
    duration: 1200,
    audioUrl: '/assets/audio/level_7_1973_war.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 75,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 400,
    keywords: ['Yom Kippur War', 'Sadat', 'Oil Crisis', 'OPEC', 'Syria'],
    source: 'The Dig - Thawra Podcast, Ep.15',
    description: '黑色九月事件与1973年战争，石油危机的起源'
  },
  {
    id: 8,
    title: 'Level 8: 1982年贝鲁特围城',
    titleEn: 'The 1982 Lebanon War and Beirut Siege',
    difficulty: 'hard',
    duration: 1200,
    audioUrl: '/assets/audio/level_8_beirut_siege.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 75,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 450,
    keywords: ['Lebanon War', 'Beirut', 'PLO', 'Sharon', 'Refugee Camps'],
    source: 'The Dig - Thawra Podcast, Ep.16',
    description: '1982年黎巴嫩战争与贝鲁特围城，巴解组织的命运'
  },
  {
    id: 9,
    title: 'Level 9: 伊朗伊斯兰革命',
    titleEn: 'The Iranian Revolution of 1979',
    difficulty: 'hard',
    duration: 1200,
    audioUrl: '/assets/audio/level_9_iran_revolution.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 80,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 500,
    keywords: ['Khomeini', 'Shah', 'Islamic Republic', 'Hostage Crisis', 'Shia'],
    source: 'The Dig - Thawra Podcast, Epilogue 1',
    description: '伊朗伊斯兰革命与霍梅尼的崛起，美伊关系破裂'
  },
  {
    id: 10,
    title: 'Level 10: 2003年伊拉克战争',
    titleEn: 'The 2003 Iraq War',
    difficulty: 'hard',
    duration: 1200,
    audioUrl: '/assets/audio/level_10_iraq_invasion.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 80,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 550,
    keywords: ['Saddam Hussein', 'WMD', 'Bush', 'Baghdad', 'Occupation'],
    source: 'The Dig - Thawra Podcast, Epilogue 2',
    description: '9·11后的伊拉克战争，萨达姆倒台与占领'
  },
  {
    id: 11,
    title: 'Level 11: 当前加沙冲突',
    titleEn: 'The Current Gaza Conflict',
    difficulty: 'hard',
    duration: 900, // 15分钟
    audioUrl: '/assets/audio/level_11_gaza_war.mp3',
    originalText: '',
    sentences: [],
    unlockScore: 85,
    bestScore: 0,
    playCount: 0,
    status: 'locked',
    points: 600,
    keywords: ['October 7', 'Hamas', 'Gaza', 'Netanyahu', 'Humanitarian Crisis'],
    source: 'The Dig - Thawra Podcast, Epilogue 3',
    description: '2023年10月7日事件与当前加沙战争'
  }
];

module.exports = { thawraLevels };
