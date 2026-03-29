// pages/player/player.js
const app = getApp();

Page({
  data: {
    level: null,
    levelId: null,
    
    // 播放状态
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    playCount: 0,
    
    // AB复读
    loopEnabled: false,
    loopStart: 0,
    loopEnd: 0,
    loopStartText: '00:00',
    loopEndText: '00:00',
    
    // 播放速度
    playbackRate: 1,
    
    // 音频上下文
    audioContext: null
  },

  onLoad(options) {
    const levelId = parseInt(options.levelId);
    const level = app.globalData.levels.find(l => l.id === levelId);
    
    if (!level) {
      wx.showToast({ title: '关卡不存在', icon: 'none' });
      wx.navigateBack();
      return;
    }

    this.setData({
      level,
      levelId,
      playCount: level.playCount || 0,
      duration: level.duration || 0
    });

    this.initAudio();
  },

  onUnload() {
    if (this.data.audioContext) {
      this.data.audioContext.destroy();
    }
    // 保存播放次数
    if (this.data.playCount > 0) {
      app.saveLevelProgress(this.data.levelId, {
        playCount: this.data.playCount
      });
    }
  },

  // 初始化音频
  initAudio() {
    const audioContext = wx.createInnerAudioContext();
    
    // 设置音频源
    if (this.data.level && this.data.level.audioUrl) {
      audioContext.src = this.data.level.audioUrl;
      console.log('音频源:', this.data.level.audioUrl);
    }
    
    // 监听播放事件
    audioContext.onPlay(() => {
      this.setData({ isPlaying: true });
    });
    
    audioContext.onPause(() => {
      this.setData({ isPlaying: false });
    });
    
    audioContext.onStop(() => {
      this.setData({ isPlaying: false, currentTime: 0 });
    });
    
    audioContext.onEnded(() => {
      this.setData({ isPlaying: false });
      if (this.data.loopEnabled && this.data.loopStart < this.data.loopEnd) {
        // AB循环模式下，回到A点重新播放
        audioContext.seek(this.data.loopStart);
        audioContext.play();
      }
    });
    
    audioContext.onTimeUpdate(() => {
      const currentTime = audioContext.currentTime;
      
      // 检查AB循环
      if (this.data.loopEnabled && this.data.loopStart < this.data.loopEnd) {
        if (currentTime >= this.data.loopEnd) {
          audioContext.seek(this.data.loopStart);
          return;
        }
      }
      
      this.setData({ currentTime });
    });
    
    audioContext.onError((err) => {
      console.error('音频播放错误:', err);
      wx.showToast({ title: '音频加载失败', icon: 'none' });
    });
    
    audioContext.onCanplay(() => {
      this.setData({ duration: audioContext.duration || this.data.level.duration });
    });

    this.setData({ audioContext });
  },

  // 播放/暂停
  togglePlay() {
    const { audioContext, isPlaying } = this.data;
    
    if (!audioContext) {
      wx.showToast({ title: '音频未加载', icon: 'none' });
      return;
    }
    
    if (isPlaying) {
      audioContext.pause();
    } else {
      audioContext.play();
      // 增加播放次数
      if (this.data.currentTime === 0) {
        this.setData({ playCount: this.data.playCount + 1 });
      }
    }
  },

  // 进度条拖动
  onSeek(e) {
    const time = e.detail.value;
    if (this.data.audioContext) {
      this.data.audioContext.seek(time);
      this.setData({ currentTime: time });
    }
  },

  onSeeking(e) {
    this.setData({ currentTime: e.detail.value });
  },

  // 后退5秒
  seekBackward() {
    const newTime = Math.max(0, this.data.currentTime - 5);
    if (this.data.audioContext) {
      this.data.audioContext.seek(newTime);
      this.setData({ currentTime: newTime });
    }
  },

  // 快进5秒
  seekForward() {
    const newTime = Math.min(this.data.duration, this.data.currentTime + 5);
    if (this.data.audioContext) {
      this.data.audioContext.seek(newTime);
      this.setData({ currentTime: newTime });
    }
  },

  // 设置播放速度
  setPlaybackRate(e) {
    const rate = parseFloat(e.currentTarget.dataset.rate);
    if (this.data.audioContext) {
      this.data.audioContext.playbackRate = rate;
    }
    this.setData({ playbackRate: rate });
  },

  // 切换AB复读
  toggleLoop(e) {
    const enabled = e.detail.value;
    this.setData({ 
      loopEnabled: enabled,
      loopStart: enabled ? this.data.loopStart : 0,
      loopEnd: enabled ? this.data.loopEnd : 0
    });
  },

  // 设置循环点
  setLoopPoint(e) {
    const point = e.currentTarget.dataset.point;
    const currentTime = this.data.currentTime;
    const timeText = this.formatTime(currentTime);
    
    if (point === 'start') {
      this.setData({
        loopStart: currentTime,
        loopStartText: timeText
      });
    } else {
      this.setData({
        loopEnd: currentTime,
        loopEndText: timeText
      });
    }
  },

  // 格式化时间
  formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return '00:00';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  },

  // 跳转到扫描页
  goToScan() {
    // 暂停播放
    if (this.data.isPlaying && this.data.audioContext) {
      this.data.audioContext.pause();
    }
    
    wx.navigateTo({
      url: `/pages/scan/scan?levelId=${this.data.levelId}`
    });
  }
});
