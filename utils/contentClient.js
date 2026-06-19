const localContent = require('../content/v1/mvpContentData.js');

const CONTENT_STATE_KEY = 'mvp_content_state_v1';
const REMOTE_MANIFEST_URL = '';

function safeGet(key, fallback) {
  try {
    const value = wx.getStorageSync(key);
    return value || fallback;
  } catch (e) {
    return fallback;
  }
}

function safeSet(key, value) {
  try {
    wx.setStorageSync(key, value);
  } catch (e) {
    console.error('保存内容缓存失败:', e);
  }
}

function requestJson(url) {
  return new Promise((resolve, reject) => {
    wx.request({
      url,
      method: 'GET',
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      },
      fail: reject
    });
  });
}

function loadRemoteContent(manifestUrl) {
  return requestJson(manifestUrl).then((manifest) => {
    const baseUrl = manifest.baseUrl || manifestUrl.replace(/\/manifest\.json$/, '/');
    const wordpackMeta = manifest.wordpacks && manifest.wordpacks[0];
    const cardpackMeta = manifest.cardpacks && manifest.cardpacks[0];

    if (!wordpackMeta || !cardpackMeta) {
      throw new Error('远端内容包缺少 wordpack 或 cardpack');
    }

    return Promise.all([
      requestJson(baseUrl + wordpackMeta.path),
      requestJson(baseUrl + cardpackMeta.path)
    ]).then((results) => normalizeContent({
      manifest,
      wordpack: results[0],
      cardpack: results[1]
    }, 'remote'));
  });
}

function normalizeContent(raw, source) {
  const words = raw.wordpack.words || [];
  const cards = raw.cardpack.cards || [];
  const wordMap = {};

  words.forEach((word) => {
    wordMap[word.word] = word;
  });

  return {
    source,
    manifest: raw.manifest,
    wordpack: raw.wordpack,
    cardpack: raw.cardpack,
    words,
    cards: cards.map((card, index) => Object.assign({}, card, {
      index,
      wordMeta: wordMap[card.word] || {},
      isCloze: card.cardType === 'cloze',
      isAudioReady: !!card.audioUrl,
      cardNumber: index + 1,
      totalCards: cards.length,
      progressPercent: Math.round(((index + 1) / cards.length) * 100)
    }))
  };
}

function loadMvpContent(options = {}) {
  const manifestUrl = options.manifestUrl || REMOTE_MANIFEST_URL;

  if (manifestUrl) {
    return loadRemoteContent(manifestUrl).then((remote) => {
      safeSet(CONTENT_STATE_KEY, remote);
      return remote;
    }).catch((e) => {
      console.warn('远端内容加载失败，改用本地内容:', e.message || e);
      const content = normalizeContent(localContent, 'local');
      safeSet(CONTENT_STATE_KEY, content);
      return content;
    });
  }

  const content = normalizeContent(localContent, 'local');
  safeSet(CONTENT_STATE_KEY, content);
  return Promise.resolve(content);
}

function getCachedContent() {
  return safeGet(CONTENT_STATE_KEY, null);
}

function getUserCardState() {
  return safeGet('user_card_state', {});
}

function saveUserCardState(state) {
  safeSet('user_card_state', state);
}

module.exports = {
  loadMvpContent,
  getCachedContent,
  getUserCardState,
  saveUserCardState
};
