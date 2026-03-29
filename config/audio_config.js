// config/audio_config.js
// 音频资源配置 - 云存储在线播放架构
// 
// 架构说明:
// 1. 音频文件上传到微信云存储 (cloud://env_id.breaking-bad-audio/xxx)
// 2. 小程序通过 fileID 或 HTTP URL 播放
// 3. 支持下载缓存到本地，离线播放
// 4. 支持断点续播

// 云存储基础路径 (上传后替换为实际的 cloud:// 或 https:// URL)
const AUDIO_BASE_URL = 'cloud://your-env-id.breaking-bad-audio';

// 如果使用自定义域名或CDN，可以用 HTTP URL
// const AUDIO_BASE_URL = 'https://your-cdn.com/audio/breaking_bad';

// 音频文件映射
const audioFiles = {
  // Level 12: 打招呼
  12: {
    cloudPath: 'breaking_bad/clips/01_greeting.mp3',
    localPath: '/assets/audio/breaking_bad/clips/01_greeting.mp3',
    size: 139200, // bytes
    duration: 71,
    source: 'S01E01'
  },
  // Level 13: 问路
  13: {
    cloudPath: 'breaking_bad/clips/02_asking_directions.mp3',
    localPath: '/assets/audio/breaking_bad/clips/02_asking_directions.mp3',
    size: 298000,
    duration: 38,
    source: 'S01E02'
  },
  // Level 14: 餐厅
  14: {
    cloudPath: 'breaking_bad/clips/03_restaurant.mp3',
    localPath: '/assets/audio/breaking_bad/clips/03_restaurant.mp3',
    size: 250600,
    duration: 32,
    source: 'S01E04'
  },
  // Level 15: 医院
  15: {
    cloudPath: 'breaking_bad/clips/04_hospital.mp3',
    localPath: '/assets/audio/breaking_bad/clips/04_hospital.mp3',
    size: 1431100,
    duration: 183,
    source: 'S01E04+S01E05'
  },
  // Level 16: 家庭
  16: {
    cloudPath: 'breaking_bad/clips/05_family.mp3',
    localPath: '/assets/audio/breaking_bad/clips/05_family.mp3',
    size: 743500,
    duration: 95,
    source: 'S01E01+S01E04'
  },
  // Level 17: 谈判
  17: {
    cloudPath: 'breaking_bad/clips/06_negotiation.mp3',
    localPath: '/assets/audio/breaking_bad/clips/06_negotiation.mp3',
    size: 1430900,
    duration: 183,
    source: 'S01E05'
  },
  // Level 18: 复杂对话
  18: {
    cloudPath: 'breaking_bad/clips/07_complex_dialogue.mp3',
    localPath: '/assets/audio/breaking_bad/clips/07_complex_dialogue.mp3',
    size: 953900,
    duration: 122,
    source: 'S01E03'
  }
};

// 获取音频的云端URL
function getCloudURL(levelId) {
  const file = audioFiles[levelId];
  if (!file) return '';
  return `${AUDIO_BASE_URL}/${file.cloudPath}`;
}

// 获取音频文件信息
function getAudioInfo(levelId) {
  return audioFiles[levelId] || null;
}

// 获取所有音频文件列表
function getAllAudioFiles() {
  return audioFiles;
}

// 计算总大小
function getTotalSize() {
  return Object.values(audioFiles).reduce((sum, f) => sum + f.size, 0);
}

module.exports = {
  audioFiles,
  getCloudURL,
  getAudioInfo,
  getAllAudioFiles,
  getTotalSize,
  AUDIO_BASE_URL
};
