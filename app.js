// app.js - 英语听写练习小程序 (Breaking Bad 专版)
App({
  globalData: {
    userInfo: null,
    levels: [],
    currentLevel: null,
    playerState: {
      isPlaying: false,
      currentTime: 0,
      loopMode: false,
      loopStart: 0,
      loopEnd: 0
    }
  },

  onLaunch() {
    console.log('英语听写练习小程序启动 - Breaking Bad 专版');
    this.initCloud();
    this.initLevels();
    this.loadUserProgress();
  },

  // 初始化云开发
  initCloud() {
    if (!wx.cloud) return;
    try {
      wx.cloud.init({
        env: wx.cloud.DYNAMIC_CURRENT_ENV,
        traceUser: false
      });
      console.log('云开发初始化成功');
    } catch (e) {
      console.log('云开发初始化失败:', e.message);
    }
  },

  // 初始化关卡数据 - 只保留 Level 1
  initLevels() {
    const defaultLevels = [
      {
        id: 1,
        title: 'Level 1: Breaking Bad - 打招呼',
        titleEn: 'Breaking Bad S01E01 - Greetings',
        difficulty: 'easy',
        difficultyText: '入门',
        duration: 71,
        audioUrl: '/assets/audio/breaking_bad/clips/01_greeting.mp3',
        originalText: '',
        sentences: [],
        unlockScore: 0,
        bestScore: 0,
        playCount: 0,
        status: 'unlocked',
        points: 100,
        keywords: ['yo', "what's up", 'how are you', 'nice to meet', 'later'],
        source: 'Breaking Bad S01E01',
        description: 'Walter的经典自我介绍对话',
        scene: '打招呼与日常问候',
        vocabulary: [
          "Oh, my God. Christ! (哦，我的天啊！)",
          "I live at 308 Negra Arroyo Lane. (我住在Negra Arroyo Lane 308号。)",
          "Albuquerque, New Mexico, 87104. (新墨西哥州阿尔伯克基，87104。)",
          "To all law-enforcement entities... (致所有执法部门...)",
          "This is not an admission... (这不是承认...)"
        ]
      }
    ];

    try {
      const savedProgress = wx.getStorageSync('levels_progress');
      if (savedProgress && Array.isArray(savedProgress)) {
        defaultLevels.forEach((level, index) => {
          if (savedProgress[index]) {
            Object.assign(level, savedProgress[index]);
          }
        });
      }
    } catch (e) {
      console.log('加载进度失败');
    }

    this.globalData.levels = defaultLevels;
  },

  // 加载用户进度
  loadUserProgress() {
    try {
      const userInfo = wx.getStorageSync('user_info');
      if (userInfo) {
        this.globalData.userInfo = userInfo;
      }
    } catch (e) {
      console.log('加载用户信息失败');
    }
  },

  // 保存关卡进度
  saveLevelProgress(levelId, data) {
    try {
      const levels = this.globalData.levels;
      const index = levels.findIndex(l => l.id === levelId);
      if (index !== -1) {
        Object.assign(levels[index], data);
        wx.setStorageSync('levels_progress', levels.map(l => ({
          id: l.id,
          bestScore: l.bestScore,
          playCount: l.playCount,
          status: l.status
        })));
      }
    } catch (e) {
      console.log('保存进度失败');
    }
  },

  // 检查关卡解锁
  checkLevelUnlock() {
    const levels = this.globalData.levels;
    for (let i = 1; i < levels.length; i++) {
      if (levels[i-1].bestScore >= levels[i].unlockScore) {
        levels[i].status = 'unlocked';
      }
    }
  }
});
