const contentClient = require('../../utils/contentClient.js');
const eventQueue = require('../../utils/eventQueue.js');

Page({
  data: {
    loading: true,
    error: '',
    source: 'local',
    cards: [],
    words: [],
    currentIndex: 0,
    currentCard: null,
    showTranslation: false,
    showClozeAnswer: false,
    userState: {},
    wordProgress: {},
    sessionStartedAt: 0,
    stats: {
      seenWords: 0,
      completedWords: 0,
      totalWords: 0,
      totalCards: 0
    }
  },

  onLoad() {
    this.loadContent();
  },

  onUnload() {
    eventQueue.track({
      eventType: 'session_complete',
      durationMs: Date.now() - this.data.sessionStartedAt,
      completedCards: this.data.currentIndex + 1
    });
  },

  loadContent() {
    this.setData({
      loading: true,
      error: '',
      sessionStartedAt: Date.now()
    });

    contentClient.loadMvpContent().then((content) => {
      const userState = contentClient.getUserCardState();
      const currentCard = content.cards[0] || null;
      const wordProgress = this.buildWordProgress(content.cards, userState);

      this.setData({
        loading: false,
        source: content.source,
        cards: content.cards,
        words: content.words,
        currentIndex: 0,
        currentCard,
        showTranslation: false,
        showClozeAnswer: false,
        userState,
        wordProgress,
        stats: this.buildStats(content.words, wordProgress, content.cards.length)
      });

      eventQueue.track({ eventType: 'feed_open', source: content.source });
      this.trackCardImpression(currentCard);
    }).catch((e) => {
      this.setData({
        loading: false,
        error: e.message || '内容加载失败'
      });
    });
  },

  buildWordProgress(cards, userState) {
    const progress = {};
    cards.forEach((card) => {
      if (!progress[card.word]) {
        progress[card.word] = {
          seenCardIds: [],
          knownCount: 0,
          unknownCount: 0,
          favorite: false
        };
      }

      const state = userState[card.cardId];
      if (!state) return;

      if (state.seen && progress[card.word].seenCardIds.indexOf(card.cardId) === -1) {
        progress[card.word].seenCardIds.push(card.cardId);
      }
      if (state.status === 'known') progress[card.word].knownCount += 1;
      if (state.status === 'unknown') progress[card.word].unknownCount += 1;
      if (state.favorite) progress[card.word].favorite = true;
    });
    return progress;
  },

  buildStats(words, wordProgress, totalCards) {
    let seenWords = 0;
    let completedWords = 0;

    words.forEach((word) => {
      const progress = wordProgress[word.word] || { seenCardIds: [] };
      if (progress.seenCardIds.length > 0) seenWords += 1;
      if (progress.seenCardIds.length >= 7) completedWords += 1;
    });

    return {
      seenWords,
      completedWords,
      totalWords: words.length,
      totalCards
    };
  },

  getCurrentState(card) {
    if (!card) return {};
    return this.data.userState[card.cardId] || {};
  },

  trackCardImpression(card) {
    if (!card) return;

    const userState = Object.assign({}, this.data.userState);
    const previous = userState[card.cardId] || {};
    userState[card.cardId] = Object.assign({}, previous, {
      seen: true,
      lastSeenAt: new Date().toISOString()
    });

    const wordProgress = this.buildWordProgress(this.data.cards, userState);
    contentClient.saveUserCardState(userState);

    this.setData({
      userState,
      wordProgress,
      stats: this.buildStats(this.data.words, wordProgress, this.data.cards.length)
    });

    eventQueue.track({
      eventType: 'card_impression',
      word: card.word,
      cardId: card.cardId,
      cardType: card.cardType,
      exposureIndex: card.exposureIndex
    });
  },

  setCurrentIndex(index) {
    const cards = this.data.cards;
    if (index < 0 || index >= cards.length) return;

    const currentCard = cards[index];
    this.setData({
      currentIndex: index,
      currentCard,
      showTranslation: false,
      showClozeAnswer: false
    });
    this.trackCardImpression(currentCard);
  },

  nextCard() {
    if (this.data.currentIndex >= this.data.cards.length - 1) {
      wx.showToast({ title: '今日卡片完成', icon: 'success' });
      eventQueue.track({
        eventType: 'session_complete',
        completedCards: this.data.cards.length
      });
      return;
    }
    this.setCurrentIndex(this.data.currentIndex + 1);
  },

  prevCard() {
    this.setCurrentIndex(this.data.currentIndex - 1);
  },

  onSwiperChange(e) {
    this.setCurrentIndex(e.detail.current);
  },

  toggleTranslation() {
    const nextValue = !this.data.showTranslation;
    this.setData({ showTranslation: nextValue });
    eventQueue.track({
      eventType: 'translation_toggle',
      word: this.data.currentCard.word,
      cardId: this.data.currentCard.cardId,
      visible: nextValue
    });
  },

  revealCloze() {
    this.setData({
      showClozeAnswer: true,
      showTranslation: true
    });
    eventQueue.track({
      eventType: 'cloze_reveal',
      word: this.data.currentCard.word,
      cardId: this.data.currentCard.cardId
    });
  },

  markKnown() {
    this.updateCardState('known');
  },

  markUnknown() {
    this.updateCardState('unknown');
  },

  toggleFavorite() {
    const card = this.data.currentCard;
    const userState = Object.assign({}, this.data.userState);
    const previous = userState[card.cardId] || {};
    const favorite = !previous.favorite;

    userState[card.cardId] = Object.assign({}, previous, {
      seen: true,
      favorite,
      updatedAt: new Date().toISOString()
    });

    const wordProgress = this.buildWordProgress(this.data.cards, userState);
    contentClient.saveUserCardState(userState);
    this.setData({ userState, wordProgress });

    eventQueue.track({
      eventType: favorite ? 'favorite_add' : 'favorite_remove',
      word: card.word,
      cardId: card.cardId
    });

    wx.showToast({
      title: favorite ? '已收藏' : '已取消',
      icon: 'none'
    });
  },

  updateCardState(status) {
    const card = this.data.currentCard;
    const userState = Object.assign({}, this.data.userState);
    const previous = userState[card.cardId] || {};

    userState[card.cardId] = Object.assign({}, previous, {
      seen: true,
      status,
      updatedAt: new Date().toISOString()
    });

    const wordProgress = this.buildWordProgress(this.data.cards, userState);
    contentClient.saveUserCardState(userState);

    this.setData({
      userState,
      wordProgress,
      stats: this.buildStats(this.data.words, wordProgress, this.data.cards.length)
    });

    eventQueue.track({
      eventType: status === 'known' ? 'mark_known' : 'mark_unknown',
      word: card.word,
      cardId: card.cardId,
      cardType: card.cardType,
      exposureIndex: card.exposureIndex
    });

    wx.showToast({
      title: status === 'known' ? '已标记认识' : '已加入复习',
      icon: 'none'
    });
  },

  resetLocalProgress() {
    wx.showModal({
      title: '重置学习记录',
      content: '仅清除本机 MVP 卡片记录，不影响后续云端数据。',
      success: (res) => {
        if (!res.confirm) return;
        contentClient.saveUserCardState({});
        this.setData({ userState: {} });
        this.loadContent();
      }
    });
  }
});
