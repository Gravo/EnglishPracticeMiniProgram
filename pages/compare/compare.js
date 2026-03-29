// pages/compare/compare.js
const app = getApp();

Page({
  data: {
    level: null,
    levelId: null,
    originalText: '',
    userText: '',
    score: 0,
    accuracy: 0,
    earnedPoints: 0,
    stats: {
      correct: 0,
      error: 0,
      missing: 0,
      extra: 0
    },
    errors: [],
    compareHtml: '',
    activeTab: 'compare'
  },

  onLoad(options) {
    const levelId = parseInt(options.levelId);
    const level = app.globalData.levels.find(l => l.id === levelId);

    if (!level) {
      wx.showToast({ title: '关卡不存在', icon: 'none' });
      wx.navigateBack();
      return;
    }

    const userText = app.globalData.userTranscript || '';

    this.setData({
      level,
      levelId,
      originalText: level.originalText || '',
      userText
    });

    // 如果没有原文，显示提示
    if (!level.originalText) {
      wx.showModal({
        title: '提示',
        content: '该关卡暂无原文，请联系管理员添加',
        showCancel: false
      });
    }

    this.compareTexts(level.originalText || '', userText, level);
  },

  // 文本对比核心算法
  compareTexts(original, user, level) {
    // 如果没有原文，无法对比
    if (!original || original.trim().length === 0) {
      this.setData({
        score: 0,
        accuracy: 0,
        earnedPoints: 0,
        compareHtml: '<p class="info">暂无原文</p>',
        errors: [],
        stats: { correct: 0, error: 0, missing: 0, extra: 0 }
      });
      return;
    }

    // 标准化文本
    const cleanOriginal = this.normalizeText(original);
    const cleanUser = this.normalizeText(user);

    // 计算Levenshtein距离
    const distance = this.levenshteinDistance(cleanOriginal, cleanUser);
    const maxLen = Math.max(cleanOriginal.length, cleanUser.length);

    // 计算准确率
    const accuracy = maxLen > 0 ? Math.round((1 - distance / maxLen) * 100) : 0;
    const score = Math.max(0, Math.min(100, accuracy));

    // 详细对比
    const { compareHtml, errors, stats } = this.detailedCompare(original, user);

    // 计算积分
    const earnedPoints = this.calculatePoints(score, level.playCount || 0, level.difficulty);

    this.setData({
      score,
      accuracy,
      earnedPoints,
      compareHtml,
      errors,
      stats
    });

    // 保存成绩
    this.saveResult(score, accuracy, earnedPoints, user);
  },

  // 标准化文本
  normalizeText(text) {
    return text
      .toLowerCase()
      .replace(/[.,!?;:'"()-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  },

  // Levenshtein距离算法
  levenshteinDistance(s1, s2) {
    const m = s1.length;
    const n = s2.length;
    const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (s1[i - 1] === s2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = Math.min(
            dp[i - 1][j] + 1,     // 删除
            dp[i][j - 1] + 1,     // 插入
            dp[i - 1][j - 1] + 1  // 替换
          );
        }
      }
    }

    return dp[m][n];
  },

  // 详细对比 - 单词级别
  detailedCompare(original, user) {
    const originalWords = original.split(/\s+/).filter(w => w.length > 0);
    const userWords = user.split(/\s+/).filter(w => w.length > 0);

    let html = '';
    let errors = [];
    let correctCount = 0, errorCount = 0, missingCount = 0, extraCount = 0;

    let i = 0, j = 0;

    while (i < originalWords.length || j < userWords.length) {
      if (i >= originalWords.length) {
        // 用户多了
        html += `<span class="extra">${this.escapeHtml(userWords[j])}</span> `;
        errors.push({
          type: 'extra',
          typeText: '多余',
          original: '(无)',
          user: userWords[j]
        });
        extraCount++;
        j++;
      } else if (j >= userWords.length) {
        // 用户漏了
        html += `<span class="missing">${this.escapeHtml(originalWords[i])}</span> `;
        errors.push({
          type: 'missing',
          typeText: '遗漏',
          original: originalWords[i],
          user: '(无)'
        });
        missingCount++;
        i++;
      } else if (originalWords[i].toLowerCase() === userWords[j].toLowerCase()) {
        // 正确
        html += `<span class="correct">${this.escapeHtml(userWords[j])}</span> `;
        correctCount++;
        i++;
        j++;
      } else {
        // 查找最佳匹配
        let found = false;
        for (let k = j; k < Math.min(j + 3, userWords.length); k++) {
          if (originalWords[i].toLowerCase() === userWords[k].toLowerCase()) {
            // 中间有遗漏
            for (let m = j; m < k; m++) {
              html += `<span class="error">${this.escapeHtml(userWords[m])}</span> `;
              errors.push({
                type: 'error',
                typeText: '错误',
                original: originalWords[i],
                user: userWords[m]
              });
              errorCount++;
            }
            html += `<span class="correct">${this.escapeHtml(originalWords[i])}</span> `;
            correctCount++;
            j = k + 1;
            i++;
            found = true;
            break;
          }
        }

        if (!found) {
          // 真正的错误
          html += `<span class="error">${this.escapeHtml(userWords[j])}</span> `;
          errors.push({
            type: 'error',
            typeText: '错误',
            original: originalWords[i],
            user: userWords[j]
          });
          errorCount++;
          i++;
          j++;
        }
      }
    }

    const stats = {
      correct: correctCount,
      error: errorCount,
      missing: missingCount,
      extra: extraCount
    };

    return { compareHtml: html, errors, stats };
  },

  // HTML转义
  escapeHtml(text) {
    const div = text;
    return div
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  },

  // 计算积分
  calculatePoints(score, playCount, difficulty) {
    const basePoints = Math.round(score * 0.5); // 分数的50%作为基础积分
    const difficultyMultiplier = { easy: 1, medium: 1.5, hard: 2 };
    const multiplier = difficultyMultiplier[difficulty] || 1;
    const efficiencyBonus = Math.max(0, (10 - playCount) * 5);

    return Math.round((basePoints * multiplier) + efficiencyBonus);
  },

  // 保存成绩
  saveResult(score, accuracy, earnedPoints, userText) {
    const level = this.data.level;
    if (!level) return;

    // 更新关卡进度
    const isCompleted = score >= (level.unlockScore || 60);
    const newStatus = isCompleted ? 'completed' : (level.status === 'completed' ? 'completed' : 'in_progress');

    app.saveLevelProgress(this.data.levelId, {
      bestScore: Math.max(level.bestScore || 0, score),
      status: newStatus,
      playCount: (level.playCount || 0) + 1
    });

    // 保存成绩记录
    try {
      const records = wx.getStorageSync('score_records') || [];
      records.push({
        levelId: this.data.levelId,
        score,
        accuracy,
        earnedPoints,
        userText,
        date: new Date().toISOString()
      });
      wx.setStorageSync('score_records', records);
    } catch (e) {
      console.log('保存成绩记录失败:', e);
    }

    // 检查是否解锁下一关
    if (isCompleted) {
      app.checkLevelUnlock();
    }

    // 更新用户积分
    try {
      const userInfo = wx.getStorageSync('user_info') || { totalPoints: 0, streakDays: 1 };
      userInfo.totalPoints = (userInfo.totalPoints || 0) + earnedPoints;
      wx.setStorageSync('user_info', userInfo);
    } catch (e) {
      console.log('更新用户积分失败:', e);
    }

    // 显示成绩
    if (isCompleted) {
      wx.showModal({
        title: '🎉 恭喜过关！',
        content: `得分: ${score}分\n获得 ${earnedPoints} 积分！`,
        showCancel: false
      });
    }
  },

  // 切换Tab
  switchTab(e) {
    this.setData({ activeTab: e.currentTarget.dataset.tab });
  },

  // 重新听写
  retryLevel() {
    wx.navigateBack();
  },

  // 下一关
  nextLevel() {
    const nextLevelId = this.data.levelId + 1;
    const levels = app.globalData.levels;

    if (nextLevelId > levels.length) {
      wx.showToast({ title: '已是最后一关', icon: 'none' });
      return;
    }

    const nextLevel = levels.find(l => l.id === nextLevelId);
    if (nextLevel && nextLevel.status === 'locked') {
      wx.showToast({ title: '请先完成当前关卡', icon: 'none' });
      return;
    }

    wx.redirectTo({
      url: `/pages/player/player?levelId=${nextLevelId}`
    });
  },

  // 返回列表
  backToList() {
    wx.switchTab({ url: '/pages/index/index' });
  }
});
