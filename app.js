// app.js
App({
  onLaunch() {
    // 小程序启动时执行的逻辑
    console.log('小程序启动');
  },
  onShow() {
    // 小程序显示时执行的逻辑
  },
  onHide() {
    // 小程序隐藏时执行的逻辑
  },
  globalData: {
    userInfo: null,
    // 学习数据存储key
    vocabularyKey: 'vocabulary_data',
    listeningKey: 'listening_progress',
    readingKey: 'reading_records',
    userSettingsKey: 'user_settings'
  }
});
