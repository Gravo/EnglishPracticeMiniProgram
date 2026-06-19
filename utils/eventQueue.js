const STORAGE_KEY = 'study_event_queue';
const STATS_KEY = 'study_local_stats';

function nowIso() {
  return new Date().toISOString();
}

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
    console.error('保存学习事件失败:', e);
  }
}

function track(event) {
  const queue = safeGet(STORAGE_KEY, []);
  const payload = Object.assign({}, {
    eventId: `evt_${Date.now()}_${Math.random().toString(16).slice(2)}`,
    timestamp: nowIso()
  }, event);

  queue.push(payload);
  safeSet(STORAGE_KEY, queue.slice(-500));
  updateStats(payload);
  return payload;
}

function updateStats(event) {
  const stats = safeGet(STATS_KEY, {
    impressions: 0,
    known: 0,
    unknown: 0,
    favorites: 0,
    clozeReveals: 0,
    sessions: 0
  });

  if (event.eventType === 'card_impression') stats.impressions += 1;
  if (event.eventType === 'mark_known') stats.known += 1;
  if (event.eventType === 'mark_unknown') stats.unknown += 1;
  if (event.eventType === 'favorite_add') stats.favorites += 1;
  if (event.eventType === 'cloze_reveal') stats.clozeReveals += 1;
  if (event.eventType === 'session_complete') stats.sessions += 1;

  stats.updatedAt = nowIso();
  safeSet(STATS_KEY, stats);
}

function getQueue() {
  return safeGet(STORAGE_KEY, []);
}

function clearQueue() {
  safeSet(STORAGE_KEY, []);
}

function getLocalStats() {
  return safeGet(STATS_KEY, {});
}

module.exports = {
  track,
  getQueue,
  clearQueue,
  getLocalStats
};
