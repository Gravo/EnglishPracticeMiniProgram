// pages/scan/scan.js - 扫描识别页面
// 支持云函数OCR和模拟识别两种模式

const app = getApp();

// OCR模式枚举
const OCR_MODE = {
  CLOUD: 'cloud',     // 云函数识别
  MOCK: 'mock'        // 模拟识别
};

Page({
  data: {
    levelId: null,
    imageSrc: '',
    flashMode: 'auto',
    isCropping: false,
    isRecognizing: false,
    recognizedText: '',
    ocrMode: OCR_MODE.CLOUD  // 默认使用云函数
  },

  // ========== 生命周期 ==========
  onLoad(options) {
    this.setData({ levelId: parseInt(options.levelId) });
  },

  // ========== 图片选择 ==========
  chooseFromAlbum() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album'],
      success: (res) => {
        this.setData({ imageSrc: res.tempFiles[0].tempFilePath });
      },
      fail: () => {
        wx.showToast({ title: '选择失败', icon: 'none' });
      }
    });
  },

  takePhoto() {
    const cameraContext = wx.createCameraContext();
    cameraContext.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({ imageSrc: res.tempImagePath });
      },
      fail: () => {
        wx.showToast({ title: '拍照失败', icon: 'none' });
      }
    });
  },

  retakePhoto() {
    this.setData({ imageSrc: '', recognizedText: '' });
  },

  toggleFlash() {
    const modes = ['auto', 'on', 'off'];
    const idx = modes.indexOf(this.data.flashMode);
    this.setData({ flashMode: modes[(idx + 1) % 3] });
  },

  // ========== OCR识别 ==========
  async startRecognize() {
    if (!this.data.imageSrc) {
      wx.showToast({ title: '请先拍摄或选择图片', icon: 'none' });
      return;
    }

    this.setData({ isRecognizing: true });

    try {
      if (this.data.ocrMode === OCR_MODE.CLOUD) {
        await this._recognizeWithCloud();
      } else {
        await this._recognizeWithMock();
      }
    } catch (error) {
      console.error('识别失败:', error);
      wx.showToast({ title: '识别失败，使用模拟模式', icon: 'none' });
      await this._recognizeWithMock();
    }

    this.setData({ isRecognizing: false });
  },

  // 云函数识别
  async _recognizeWithCloud() {
    try {
      const fs = wx.getFileSystemManager();
      const fileData = fs.readFileSync(this.data.imageSrc, 'base64');

      const result = await wx.cloud.callFunction({
        name: 'ocrRecognize',
        data: { imageBase64: fileData },
        config: { env: wx.cloud.DYNAMIC_CURRENT_ENV }
      });

      if (result && result.result && result.result.success) {
        this.setData({ recognizedText: result.result.text });
        wx.showToast({ title: '识别成功', icon: 'success' });
      } else {
        throw new Error(result.result?.error || '识别失败');
      }
    } catch (error) {
      console.error('云函数OCR失败:', error);
      throw error;
    }
  },

  // 模拟识别 - 获取当前关卡词汇
  async _recognizeWithMock() {
    const level = app.globalData.levels.find(l => l.id === this.data.levelId);
    let mockText = '';

    if (level?.vocabulary?.length) {
      mockText = level.vocabulary
        .filter(v => v.includes('('))
        .map(v => v.replace(/\s*\([^)]+\)\s*/g, ''))
        .join(' ');
    }

    if (!mockText) {
      mockText = 'This is a mock recognition result. Please use manual input.';
    }

    // 模拟延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    this.setData({ recognizedText: mockText, ocrMode: OCR_MODE.MOCK });
    wx.showToast({ title: '模拟识别完成', icon: 'success' });
  },

  // 切换OCR模式
  toggleOcrMode() {
    const newMode = this.data.ocrMode === OCR_MODE.CLOUD ? OCR_MODE.MOCK : OCR_MODE.CLOUD;
    this.setData({ ocrMode: newMode });
    wx.showToast({
      title: newMode === OCR_MODE.CLOUD ? '云函数模式' : '模拟模式',
      icon: 'none'
    });
  },

  // ========== 文本编辑 ==========
  editText() {
    wx.showModal({
      title: '编辑文本',
      editable: true,
      content: this.data.recognizedText,
      success: (res) => {
        if (res.confirm && res.content) {
          this.setData({ recognizedText: res.content });
        }
      }
    });
  },

  manualInput() {
    wx.showModal({
      title: '输入听写文本',
      editable: true,
      placeholderText: '请输入你听到的内容...',
      success: (res) => {
        if (res.confirm && res.content) {
          this.setData({ recognizedText: res.content });
        }
      }
    });
  },

  // ========== 导航 ==========
  goToCompare() {
    if (!this.data.recognizedText) {
      wx.showToast({ title: '请先完成识别或手动输入', icon: 'none' });
      return;
    }
    app.globalData.userTranscript = this.data.recognizedText;
    wx.navigateTo({
      url: `/pages/compare/compare?levelId=${this.data.levelId}`
    });
  }
});
