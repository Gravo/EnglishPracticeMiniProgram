# MVP Delivery Plan

**目标**: 用最小成本验证“高中生愿意通过短语境卡流泛读泛听，并在 7 次不同语境中记住高考词”。  
**MVP1 范围**: 10 个高考词，70 张卡片，暂不生成音频文件，先跑通内容结构和前端接入。

---

## 1. 当前已完成

| 项目 | 状态 | 路径 |
|---|---|---|
| 高考基线词表 | 已完成 | `docs/zhejiang_gaokao_vocab/` |
| 50 页高阶架构 | 已完成 | `docs/HIGH_LEVEL_ARCHITECTURE_50P.md` |
| MVP 内容生成脚本 | 已完成 | `tools/build_mvp_content_pack.py` |
| MVP manifest | 已完成 | `content/v1/manifest.json` |
| MVP wordpack | 已完成 | `content/v1/wordpacks/gaokao_mvp_words_001.json` |
| MVP cardpack | 已完成 | `content/v1/cardpacks/gaokao_mvp_cards_001.json` |

---

## 2. MVP1 内容范围

首批词：

1. approach
2. benefit
3. affect
4. admit
5. consider
6. develop
7. improve
8. support
9. challenge
10. experience

每词 7 张卡：

- meaning
- campus
- family
- news/science
- dialogue
- cloze
- transfer

---

## 3. 第一阶段：本地内容闭环

验收目标：

- `python tools/build_mvp_content_pack.py` 能生成 10 词 70 卡。
- `content/v1/manifest.json` 能作为远端入口。
- cardpack 中每张卡都有 word、sentence、translation、cardType、exposureIndex。
- audioUrl 允许为空，标记为 `tts_pending`。

负责人：

- CEO 主代理
- 质量/合规 Agent

人工控制点：

- 抽查 70 张卡是否自然、准确、适合高中生。
- 打回任何生硬、成人化、版权不清或翻译不准的内容。

---

## 4. 第二阶段：小程序接入

要新增/修改：

- 新增 `utils/contentClient.js`
- 新增 `utils/eventQueue.js`
- 新增 `pages/feed`
- 修改 `app.json` 注册页面
- 可选：在首页加入“今日语感流”入口

验收目标：

- 小程序能读取本地或远端 manifest。
- 能加载 wordpack 和 cardpack。
- 能展示 70 张卡。
- 能记录“看过、认识、不认识、收藏、完成 cloze”。
- 本地缓存学习事件，未来可上传服务器。

负责人：

- 小程序技术 Agent

人工控制点：

- iPhone 真机测试
- 鸿蒙/安卓真机测试
- 弱网加载测试
- 页面不卡、不乱、不像背单词表

---

## 5. 第三阶段：TTS 音频

输入：

- `card.audioText`

输出：

- `/audio/tts/mvp_approach_01.mp3`
- audio manifest
- 更新后的 cardpack `audioUrl`

验收目标：

- 每张卡都有可播放音频。
- 单条音频 3-10 秒为主。
- 音量稳定。
- 发音自然。
- 文件总体积可控。

负责人：

- TTS/音频 Agent

人工控制点：

- 抽听每个词至少 2 条。
- 重点检查 admit、affect、develop 等发音。

---

## 6. 第四阶段：10 人试用

用户：

- 你的女儿
- 3-5 个同学
- 2-3 个家长旁观
- 可选 1 个英语老师

试用周期：

- 7 天

观察指标：

- 是否每天打开
- 是否完成 10-30 张卡
- 是否觉得像“刷内容”而不是“做作业”
- 是否记得住 3-5 个词
- 家长是否愿意为 100 天计划付费

人工控制点：

- 第 3 天做一次访谈
- 第 7 天做一次复盘

---

## 7. 扩到 300 词的条件

只有同时满足这些条件，才扩量：

- 70 张卡审核通过率高于 90%
- 小程序 feed 页面完成主流程
- 5 个以上学生完成 3 天试用
- 至少 3 个学生愿意继续用
- 至少 2 个家长认为值得付费或继续观察

扩量目标：

- 300 个 A/B 级高考词
- 每词 7 卡
- 共 2100 张卡
- 每词至少 2 张主动回忆卡

---

## 8. CEO 下一步命令

1. 等待三个子 agent 产出审核、技术、运营文档。
2. 整合并确认 MVP1 规格。
3. 实现 `pages/feed` 和 `contentClient`。
4. 审核 70 张卡。
5. 生成第一批 TTS 音频。
6. 上传到域名或先用本地调试。
7. 找 5-10 个真实学生试用。

