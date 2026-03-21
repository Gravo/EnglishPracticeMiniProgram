// pages/listening/listening.js
const app = getApp();

Page({
  data: {
    materials: [
      { id: 1, title: 'BBC News', level: '中级', duration: '3:25', plays: 1234 },
      { id: 2, title: 'VOA Learning English', level: '初级', duration: '2:15', plays: 2567 },
      { id: 3, title: 'TED Talks', level: '高级', duration: '5:30', plays: 890 },
      { id: 4, title: '日常口语对话', level: '初级', duration: '1:45', votes: 3456 }
    ],
    currentAudio: null,
    isPlaying: false,
    isLoop: false,
    currentTime: 0,
    duration: 0,
    audioContext: null
  },

  onLoad() {
    // 创建音频上下文
    this.audioContext = wx.createInnerAudioContext();
    
    // 监听播放结束
    this.audioContext.onEnded(() => {
      if (this.data.isLoop) {
        this.audioContext.play();
      } else {
        this.setData({ isPlaying: false });
      }
    });
    
    // 监听错误
    this.audioContext.onError((err) => {
      console.error('音频播放错误', err);
      wx.showToast({ title: '播放失败', icon: 'none' });
    });
  },

  onUnload() {
    if (this.audioContext) {
      this.audioContext.stop();
      this.audioContext.destroy();
    }
  },

  // 播放音频
  playAudio(e) {
    const id = e.currentTarget.dataset.id;
    const material = this.data.materials.find(m => m.id === id);
    
    if (material) {
      this.setData({
        currentAudio: material,
        isPlaying: false,
        currentTime: 0,
        duration: 180 // 模拟时长（秒）
      });
      
      // 设置音频源
      // this.audioContext.src = '音频URL';
      
      this.audioContext.play();
      this.setData({ isPlaying: true });
      
      // 开始计时更新
      this.startTimeUpdate();
    }
  },

  // 关闭播放器
  closePlayer() {
    this.audioContext.stop();
    this.setData({
      currentAudio: null,
      isPlaying: false
    });
  },

  // 切换播放/暂停
  togglePlay() {
    if (this.data.isPlaying) {
      this.audioContext.pause();
    } else {
      this.audioContext.play();
    }
    this.setData({ isPlaying: !this.data.isPlaying });
  },

  // 切换循环模式
  toggleLoop() {
    this.setData({ isLoop: !this.data.isLoop });
    this.audioContext.loop = this.data.isLoop;
  },

  // 跳转进度
  seekAudio(e) {
    const time = e.detail.value;
    this.audioContext.seek(time);
    this.setData({ currentTime: time });
  },

  // 格式化时间
  formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  },

  // 模拟时间更新
  startTimeUpdate() {
    let timer = setInterval(() => {
      if (this.data.isPlaying && this.data.currentTime < this.data.duration) {
        this.setData({
          currentTime: this.data.currentTime + 1
        });
      } else {
        clearInterval(timer);
      }
    }, 1000);
  }
});
