# MVP Frontend Integration Plan

**目标**: 让微信小程序读取 `content/v1` 内容包，展示 10 个高考词 x 7 张语境卡，并记录基础学习状态。  
**当前状态**: 内容包已生成，音频待生成，前端尚未接入。

---

## 1. 页面规划

MVP 新增一个核心页面：

```text
pages/feed/
  feed.js
  feed.wxml
  feed.wxss
  feed.json
```

入口：

- 首页增加“今日语感流”按钮。
- 后续可加入 tabBar，但 MVP 先不动 tabBar，减少审核和 UI 改动。

页面职责：

- 加载 manifest。
- 加载 wordpack 和 cardpack。
- 按卡片顺序展示。
- 支持上一张/下一张或上下滑。
- 支持显示/隐藏中文。
- 支持“认识 / 不认识 / 收藏”。
- cloze 卡支持输入或点击揭晓。

---

## 2. Utils 规划

新增：

```text
utils/contentClient.js
utils/eventQueue.js
```

`contentClient.js`：

- `loadManifest()`
- `loadWordpack(packMeta)`
- `loadCardpack(packMeta)`
- `loadMvpContent()`
- 支持本地内容兜底：开发阶段可直接读取内置路径或临时 mock。

`eventQueue.js`：

- `track(event)`
- `flush()`
- `getLocalStats()`
- 网络不可用时先写 `wx.setStorageSync`

---

## 3. 数据加载流程

```text
feed.onLoad
  ↓
contentClient.loadMvpContent()
  ↓
读取 manifest
  ↓
读取 wordpack/cardpack
  ↓
合并 word 和 cards
  ↓
读取本地 user_card_state
  ↓
生成今日队列
  ↓
渲染第一张卡
```

开发阶段：

- 可以先使用 `content/v1` 的结构生成一份小程序可 require 的 JS mock。
- 或把内容上传到域名后走 `wx.request`。

正式阶段：

- `manifestUrl = https://your-domain.com/content/v1/manifest.json`
- 微信后台配置 request 合法域名。
- 资源域名必须 HTTPS。

---

## 4. 本地缓存策略

缓存 key：

```javascript
CONTENT_MANIFEST = 'content_manifest_v1'
WORDPACK_gaokao_mvp_words_001 = 'wordpack_gaokao_mvp_words_001'
CARDPACK_gaokao_mvp_cards_001 = 'cardpack_gaokao_mvp_cards_001'
USER_CARD_STATE = 'user_card_state'
STUDY_EVENT_QUEUE = 'study_event_queue'
```

规则：

- manifest 短缓存，可每次启动检查版本。
- wordpack/cardpack 按 `contentVersion` 缓存。
- 用户事件先本地保存，未来再上传。
- 切换内容版本时不清用户学习状态，只按 cardId 合并。

---

## 5. 事件埋点

MVP 至少记录：

| 事件 | 触发 |
|---|---|
| `feed_open` | 进入页面 |
| `card_impression` | 卡片展示 |
| `translation_toggle` | 显示/隐藏中文 |
| `mark_known` | 点击认识 |
| `mark_unknown` | 点击不认识 |
| `favorite_add` | 收藏 |
| `cloze_reveal` | cloze 揭晓 |
| `session_complete` | 完成一轮 |

事件字段：

```javascript
{
  eventType,
  word,
  cardId,
  cardType,
  exposureIndex,
  timestamp,
  durationMs
}
```

---

## 6. 学习状态规则

本地先实现：

```javascript
{
  word: {
    seenCardIds: [],
    knownCount: 0,
    unknownCount: 0,
    favorite: false,
    lastSeenAt: ''
  }
}
```

掌握提示：

- 看过 7 张不同卡：显示“完成 7 个语境”。
- 认识次数 >= 5 且不认识次数 <= 1：显示“基本熟悉”。
- 未来接入后端后再按跨天复习和主动回忆判断掌握。

---

## 7. 真机测试点

iPhone：

- 页面滑动是否顺畅。
- 英文长句是否换行正常。
- 中文显示/隐藏是否跳动过大。
- `wx.setStorageSync` 是否稳定。

鸿蒙/安卓：

- 字体、按钮高度、底部安全区。
- 网络请求失败提示。
- 页面返回后状态是否保存。
- 后续音频播放兼容性。

弱网：

- manifest 加载失败有提示。
- 已缓存内容可继续学习。
- 事件不丢失。

---

## 8. 第一周实施顺序

Day 1：

- 新增 `pages/feed` 静态 UI。
- 新增首页入口。

Day 2：

- 新增 `contentClient`。
- 用本地 mock 或远端 manifest 加载 70 张卡。

Day 3：

- 实现卡片切换、中文显示、认识/不认识。
- 保存本地学习状态。

Day 4：

- 实现 `eventQueue`。
- 增加完成统计。

Day 5：

- iPhone 和鸿蒙真机测试。
- 修 UI 和缓存问题。

Day 6：

- 接入 TTS 音频 URL，如果音频未完成则保留文本模式。

Day 7：

- 给 5-10 个学生试用。

