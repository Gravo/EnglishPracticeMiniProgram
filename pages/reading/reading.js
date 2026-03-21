// pages/reading/reading.js
Page({
  data: {
    articles: [
      {
        id: 1,
        title: 'The Importance of Reading English',
        summary: 'Reading is one of the best ways to learn English. It helps expand vocabulary and improve comprehension.',
        cover: '/assets/images/article1.jpg',
        category: '学习方法',
        words: 500,
        difficulty: 'easy',
        difficultyText: '简单'
      },
      {
        id: 2,
        title: 'Technology Changes Our Lives',
        summary: 'How technology has transformed the way we live, work, and communicate with each other.',
        cover: '/assets/images/article2.jpg',
        category: '科技',
        words: 800,
        difficulty: 'medium',
        difficultyText: '中等'
      },
      {
        id: 3,
        title: 'Climate Change and Our Future',
        summary: 'Understanding climate change and what we can do to protect our planet for future generations.',
        cover: '/assets/images/article3.jpg',
        category: '环境',
        words: 1000,
        difficulty: 'hard',
        difficultyText: '困难'
      }
    ]
  },

  onLoad() {
    this.loadArticles();
  },

  // 加载文章列表
  loadArticles() {
    // 实际项目中从服务器获取
    const cached = wx.getStorageSync('article_list');
    if (cached) {
      this.setData({ articles: cached });
    }
  },

  // 阅读文章
  readArticle(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/article/article?id=${id}`
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadArticles();
    wx.stopPullDownRefresh();
  }
});
