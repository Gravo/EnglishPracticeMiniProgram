// pages/scan/scan.js - 前端直接调用腾讯云OCR版本
const app = getApp();

// 腾讯云API配置 - 请填入你的密钥
const TENCENT_CONFIG = {
  secretId: '', // 填写你的SecretId
  secretKey: '', // 填写你的SecretKey
  region: 'ap-beijing'
};

Page({
  data: {
    levelId: null,
    imageSrc: '',
    flashMode: 'auto',
    isCropping: false,
    isRecognizing: false,
    recognizedText: ''
  },

  onLoad(options) {
    this.setData({ levelId: parseInt(options.levelId) });
  },

  // 从相册选择
  chooseFromAlbum() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album'],
      success: (res) => {
        this.setData({
          imageSrc: res.tempFiles[0].tempFilePath
        });
      }
    });
  },

  // 拍照
  takePhoto() {
    const cameraContext = wx.createCameraContext();
    cameraContext.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          imageSrc: res.tempImagePath
        });
      },
      fail: () => {
        wx.showToast({ title: '拍照失败', icon: 'none' });
      }
    });
  },

  // 重拍
  retakePhoto() {
    this.setData({
      imageSrc: '',
      recognizedText: ''
    });
  },

  // 切换闪光灯
  toggleFlash() {
    const modes = ['auto', 'on', 'off'];
    const currentIndex = modes.indexOf(this.data.flashMode);
    const nextMode = modes[(currentIndex + 1) % modes.length];
    this.setData({ flashMode: nextMode });
  },

  // 开始识别
  startRecognize() {
    if (!this.data.imageSrc) {
      wx.showToast({ title: '请先拍摄或选择图片', icon: 'none' });
      return;
    }

    // 检查是否配置了密钥
    if (!TENCENT_CONFIG.secretId || !TENCENT_CONFIG.secretKey) {
      wx.showModal({
        title: '提示',
        content: '请先配置腾讯云API密钥，或使用模拟识别',
        showCancel: true,
        cancelText: '使用模拟',
        confirmText: '去配置',
        success: (res) => {
          if (res.confirm) {
            // 打开配置文件
            wx.showToast({ title: '请修改scan.js中的配置', icon: 'none' });
          } else {
            // 使用模拟识别
            this.mockRecognize();
          }
        }
      });
      return;
    }

    this.setData({ isRecognizing: true });
    this.recognizeWithTencentCloudDirect();
  },

  // 腾讯云OCR直接调用（前端版本，适合测试）
  recognizeWithTencentCloudDirect() {
    const fs = wx.getFileSystemManager();
    
    // 读取图片为base64
    fs.readFile({
      filePath: this.data.imageSrc,
      encoding: 'base64',
      success: (res) => {
        const imageBase64 = res.data;
        
        // 调用腾讯云OCR API
        this.callTencentOCR(imageBase64);
      },
      fail: (err) => {
        console.error('读取图片失败:', err);
        this.setData({ isRecognizing: false });
        wx.showToast({ title: '读取图片失败', icon: 'none' });
      }
    });
  },

  // 调用腾讯云OCR API
  callTencentOCR(imageBase64) {
    const timestamp = Math.floor(Date.now() / 1000);
    const date = new Date(timestamp * 1000).toISOString().split('T')[0];
    
    // 构建请求参数
    const payload = JSON.stringify({
      ImageBase64: imageBase64
    });
    
    // 构建签名（简化版）
    const service = 'ocr';
    const host = 'ocr.tencentcloudapi.com';
    const action = 'GeneralBasicOCR';
    const version = '2018-11-19';
    
    // 注意：前端直接调用需要处理CORS，建议通过云函数
    // 这里使用微信小程序的request，需要先在腾讯云配置域名白名单
    
    wx.request({
      url: 'https://ocr.tencentcloudapi.com',
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Host': host,
        'X-TC-Action': action,
        'X-TC-Version': version,
        'X-TC-Timestamp': timestamp.toString(),
        'X-TC-Region': TENCENT_CONFIG.region,
        'Authorization': this.generateSignature(timestamp, date, payload)
      },
      data: payload,
      success: (res) => {
        this.setData({ isRecognizing: false });
        
        if (res.data.Response && res.data.Response.TextDetections) {
          const text = res.data.Response.TextDetections
            .map(item => item.DetectedText)
            .join(' ');
          
          this.setData({ recognizedText: text });
          wx.showToast({ title: '识别完成', icon: 'success' });
        } else {
          console.error('OCR识别失败:', res.data);
          wx.showToast({ title: '识别失败', icon: 'none' });
        }
      },
      fail: (err) => {
        console.error('请求失败:', err);
        this.setData({ isRecognizing: false });
        wx.showToast({ title: '网络请求失败', icon: 'none' });
      }
    });
  },

  // 生成签名（简化版，生产环境建议使用SDK）
  generateSignature(timestamp, date, payload) {
    // 这里需要实现TC3-HMAC-SHA256签名算法
    // 由于前端暴露密钥不安全，建议使用云函数
    // 这里返回一个占位符，实际使用时需要完整实现签名逻辑
    return 'TC3-HMAC-SHA256 ' + TENCENT_CONFIG.secretId;
  },

  // 模拟识别（开发测试用）
  mockRecognize() {
    const levelId = this.data.levelId;
    const levels = app.globalData.levels;
    const level = levels.find(l => l.id === levelId);
    
    let mockText = '';
    if (level) {
      const originalText = level.originalText;
      const words = originalText.split(' ');
      const simplifiedWords = words.slice(0, Math.floor(words.length * 0.8));
      mockText = simplifiedWords.join(' ');
    } else {
      mockText = 'China has many important inventions. The four great inventions changed the world.';
    }

    this.setData({ isRecognizing: true });
    
    setTimeout(() => {
      this.setData({
        isRecognizing: false,
        recognizedText: mockText
      });
      wx.showToast({ title: '模拟识别完成', icon: 'success' });
    }, 1500);
  },

  // 编辑识别结果
  editText() {
    wx.showModal({
      title: '编辑文本',
      editable: true,
      content: this.data.recognizedText,
      success: (res) => {
        if (res.confirm) {
          this.setData({ recognizedText: res.content });
        }
      }
    });
  },

  // 手动输入
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

  // 跳转到对照页
  goToCompare() {
    if (!this.data.recognizedText) {
      wx.showToast({ title: '请先完成识别', icon: 'none' });
      return;
    }

    app.globalData.userTranscript = this.data.recognizedText;

    wx.navigateTo({
      url: `/pages/compare/compare?levelId=${this.data.levelId}`
    });
  }
});
