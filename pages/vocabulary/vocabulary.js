// pages/vocabulary/vocabulary.js
const app = getApp();

Page({
  data: {
    wordList: [],
    currentIndex: 0,
    currentWord: {},
    showMeaning: false,
    correctCount: 0,
    wrongCount: 0,
    currentBook: 'cet4',
    wordBooks: [
      { id: 'cet4', name: 'CET-4' },
      { id: 'cet6', name: 'CET-6' },
      { id: 'ielts', name: 'IELTS' },
      { id: 'toefl', name: 'TOEFL' }
    ],
    // 模拟单词数据
    sampleWords: [
      { word: 'abandon', phonetic: '/əˈbændən/', partOfSpeech: 'v.', definition: '放弃；遗弃' },
      { word: 'ability', phonetic: '/əˈbɪləti/', partOfSpeech: 'n.', definition: '能力；才能' },
      { word: 'able', phonetic: '/ˈeɪbl/', partOfSpeech: 'adj.', definition: '能够的；有能力的' },
      { word: 'about', phonetic: '/əˈbaʊt/', partOfSpeech: 'prep.', definition: '关于；大约' },
      { word: 'above', phonetic: '/əˈbʌv/', partOfSpeech: 'prep.', definition: '在...上面' }
    ]
  },

  onLoad() {
    this.loadWordList();
  },

  // 加载单词列表
  loadWordList() {
    // 从本地存储或使用示例数据
    const words = wx.getStorageSync('word_list_' + this.data.currentBook) || this.data.sampleWords;
    this.setData({
      wordList: words,
      currentWord: words[0] || {}
    });
  },

  // 切换词书
  selectBook(e) {
    const bookId = e.currentTarget.dataset.id;
    this.setData({
      currentBook: bookId,
      currentIndex: 0,
      showMeaning: false,
      correctCount: 0,
      wrongCount: 0
    });
    this.loadWordList();
  },

  // 翻转卡片
  flipCard() {
    this.setData({
      showMeaning: !this.data.showMeaning
    });
  },

  // 标记认识
  markKnow() {
    this.updateProgress(true);
  },

  // 标记不认识
  markFail() {
    this.updateProgress(false);
  },

  // 更新进度
  updateProgress(isCorrect) {
    const { currentIndex, wordList, correctCount, wrongCount } = this.data;
    
    if (isCorrect) {
      this.setData({ correctCount: correctCount + 1 });
    } else {
      this.setData({ wrongCount: wrongCount + 1 });
    }

    // 下一词
    if (currentIndex < wordList.length - 1) {
      this.setData({
        currentIndex: currentIndex + 1,
        currentWord: wordList[currentIndex + 1],
        showMeaning: false
      });
    } else {
      // 完成学习
      wx.showToast({
        title: '学习完成!',
        icon: 'success'
      });
      // 保存学习记录
      this.saveStudyRecord();
    }
  },

  // 计算正确率
  get correctRate() {
    const total = this.data.correctCount + this.data.wrongCount;
    return total === 0 ? 0 : Math.round((this.data.correctCount / total) * 100);
  },

  // 计算进度百分比
  get progressPercent() {
    const { currentIndex, wordList } = this.data;
    return wordList.length === 0 ? 0 : Math.round(((currentIndex + 1) / wordList.length) * 100);
  },

  // 保存学习记录
  saveStudyRecord() {
    try {
      const today = new Date().toDateString();
      const stats = wx.getStorageSync('today_stats') || { words: 0, listening: 0, reading: 0, streak: 0 };
      stats.words += this.data.correctCount;
      wx.setStorageSync('today_stats', stats);
    } catch (e) {
      console.error('保存学习记录失败', e);
    }
  }
});
