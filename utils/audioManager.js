// utils/audioManager.js
// 音频管理器 - 支持在线播放、下载缓存、离线播放
const audioConfig = require('../config/audio_config');

class AudioManager {
  constructor() {
    this.audioContext = null;
    this.downloadTasks = {};
    this.cacheMap = {};     // levelId -> local temp path
    this.downloadProgress = {}; // levelId -> percent
    this.listeners = new Map();
  }

  /**
   * 获取音频源 - 优先本地缓存，其次在线播放
   * @param {number} levelId 
   * @returns {string} 音频路径 (本地路径 或 云端URL)
   */
  async getAudioSource(levelId) {
    // 1. 检查本地缓存 (wx.env.USER_DATA_PATH)
    const cachedPath = await this._getCachedPath(levelId);
    if (cachedPath) {
      console.log('[AudioManager] 使用缓存:', cachedPath);
      return cachedPath;
    }

    // 2. 返回云端URL (在线播放)
    const cloudURL = audioConfig.getCloudURL(levelId);
    if (cloudURL) {
      console.log('[AudioManager] 使用云端URL:', cloudURL);
      return cloudURL;
    }

    // 3. fallback: 本地打包路径
    const info = audioConfig.getAudioInfo(levelId);
    if (info && info.localPath) {
      return info.localPath;
    }

    return '';
  }

  /**
   * 下载音频到本地缓存
   * @param {number} levelId 
   * @param {function} onProgress - 进度回调 (percent: 0-100)
   * @returns {Promise<string>} 本地缓存路径
   */
  downloadAudio(levelId, onProgress) {
    return new Promise((resolve, reject) => {
      const cloudURL = audioConfig.getCloudURL(levelId);
      if (!cloudURL) {
        reject(new Error('无法获取音频URL'));
        return;
      }

      // 检查是否已有缓存
      const fs = wx.getFileSystemManager();
      const cachePath = `${wx.env.USER_DATA_PATH}/audio_${levelId}.mp3`;

      try {
        const stat = fs.statSync(cachePath);
        if (stat && stat.size > 0) {
          this.cacheMap[levelId] = cachePath;
          onProgress && onProgress(100);
          resolve(cachePath);
          return;
        }
      } catch (e) {
        // 文件不存在，继续下载
      }

      // 开始下载
      const downloadTask = wx.downloadFile({
        url: cloudURL,
        filePath: cachePath,
        success: (res) => {
          if (res.statusCode === 200) {
            this.cacheMap[levelId] = cachePath;
            // 保存缓存记录
            this._saveCacheRecord(levelId, cachePath);
            onProgress && onProgress(100);
            resolve(cachePath);
          } else {
            reject(new Error(`下载失败: HTTP ${res.statusCode}`));
          }
        },
        fail: (err) => {
          console.error('[AudioManager] 下载失败:', err);
          reject(err);
        }
      });

      // 监听下载进度
      if (onProgress) {
        downloadTask.onProgressUpdate((res) => {
          onProgress(res.progress);
          this.downloadProgress[levelId] = res.progress;
          this._emit('downloadProgress', { levelId, progress: res.progress });
        });
      }

      this.downloadTasks[levelId] = downloadTask;
    });
  }

  /**
   * 取消下载
   */
  cancelDownload(levelId) {
    const task = this.downloadTasks[levelId];
    if (task) {
      task.abort();
      delete this.downloadTasks[levelId];
    }
  }

  /**
   * 检查音频是否已缓存
   */
  async isCached(levelId) {
    const path = await this._getCachedPath(levelId);
    return !!path;
  }

  /**
   * 获取缓存大小
   */
  async getCacheSize() {
    try {
      const fs = wx.getFileSystemManager();
      const files = fs.readdirSync(wx.env.USER_DATA_PATH);
      let totalSize = 0;
      files.forEach(f => {
        if (f.startsWith('audio_') && f.endsWith('.mp3')) {
          try {
            const stat = fs.statSync(`${wx.env.USER_DATA_PATH}/${f}`);
            totalSize += stat.size;
          } catch (e) {}
        }
      });
      return totalSize;
    } catch (e) {
      return 0;
    }
  }

  /**
   * 清除所有缓存
   */
  async clearCache() {
    try {
      const fs = wx.getFileSystemManager();
      const files = fs.readdirSync(wx.env.USER_DATA_PATH);
      let cleared = 0;
      files.forEach(f => {
        if (f.startsWith('audio_') && f.endsWith('.mp3')) {
          try {
            fs.unlinkSync(`${wx.env.USER_DATA_PATH}/${f}`);
            cleared++;
          } catch (e) {}
        }
      });
      this.cacheMap = {};
      wx.removeStorageSync('audio_cache_records');
      return cleared;
    } catch (e) {
      return 0;
    }
  }

  /**
   * 批量下载所有音频
   */
  async downloadAll(onProgress) {
    const allFiles = audioConfig.getAllAudioFiles();
    const ids = Object.keys(allFiles).map(Number);
    let completed = 0;
    const total = ids.length;

    for (const id of ids) {
      try {
        await this.downloadAudio(id, (pct) => {
          if (onProgress) {
            const overallPct = Math.round((completed + pct / 100) / total * 100);
            onProgress({ completed, total, current: id, overallPct });
          }
        });
        completed++;
      } catch (e) {
        console.error(`下载 Level ${id} 失败:`, e);
        completed++;
      }
    }

    if (onProgress) {
      onProgress({ completed: total, total, overallPct: 100 });
    }
  }

  // === 私有方法 ===

  async _getCachedPath(levelId) {
    // 先查内存缓存
    if (this.cacheMap[levelId]) {
      try {
        const fs = wx.getFileSystemManager();
        fs.accessSync(this.cacheMap[levelId]);
        return this.cacheMap[levelId];
      } catch (e) {
        delete this.cacheMap[levelId];
      }
    }

    // 再查文件系统
    const cachePath = `${wx.env.USER_DATA_PATH}/audio_${levelId}.mp3`;
    try {
      const fs = wx.getFileSystemManager();
      const stat = fs.statSync(cachePath);
      if (stat && stat.size > 0) {
        this.cacheMap[levelId] = cachePath;
        return cachePath;
      }
    } catch (e) {}

    return null;
  }

  _saveCacheRecord(levelId, path) {
    try {
      const records = wx.getStorageSync('audio_cache_records') || {};
      records[levelId] = {
        path,
        timestamp: Date.now(),
        size: audioConfig.getAudioInfo(levelId)?.size || 0
      };
      wx.setStorageSync('audio_cache_records', records);
    } catch (e) {}
  }

  // 事件系统
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const cbs = this.listeners.get(event).filter(cb => cb !== callback);
      this.listeners.set(event, cbs);
    }
  }

  _emit(event, data) {
    const cbs = this.listeners.get(event) || [];
    cbs.forEach(cb => cb(data));
  }
}

// 单例
const audioManager = new AudioManager();
module.exports = audioManager;
