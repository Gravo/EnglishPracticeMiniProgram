# The Dig - Thawra 播客音频整理方案

## 资源信息

**播客名称**: The Dig - Thawra (革命)
**主持人**: Daniel Denvir & Abdel Razzaq Takriti
**主题**: 20世纪阿拉伯激进主义历史
**版权状态**: 可免费收听，允许截取学习使用

## 剧集清单

| 剧集 | 主题 | 总时长 | 推荐截取 | 截取时长 | 难度 |
|------|------|--------|----------|----------|------|
| Ep.14 | 巴勒斯坦革命、1967年战争 | 2h48m | 第20-40分钟 | 20分钟 | 高 |
| Ep.15 | 黑色九月、1973年战争 | 2h50m | 第30-50分钟 | 20分钟 | 高 |
| Ep.16 | 1982年黎巴嫩战争、贝鲁特围城 | 2h33m | 开篇20分钟 | 20分钟 | 高 |
| Epilogue 1 | 伊朗革命、两伊战争 | 3h21m | 第10-30分钟 | 20分钟 | 高 |
| Epilogue 2 | 9·11、伊拉克战争 | 2h59m | 第30-50分钟 | 20分钟 | 高 |
| Epilogue 3 | 10月7日、加沙战争 | 2h32m | 开篇15分钟 | 15分钟 | 高 |

**总计**: 6个音频片段，约115分钟

## 下载平台

### 1. Apple Podcasts
https://podcasts.apple.com/
搜索: "The Dig Thawra"

### 2. Spotify
https://open.spotify.com/
搜索: "The Dig Thawra"

### 3. Radio.net
https://www.radio.net/
搜索: "The Dig"

### 4. 官方网站
https://www.thedigradio.com/

## 目录结构

```
D:\downloads_english\
└── the_dig_thawra\
    ├── original\              (原始完整音频)
    │   ├── ep14_palestine_revolution_1967.mp3
    │   ├── ep15_black_september_1973.mp3
    │   ├── ep16_lebanon_war_1982.mp3
    │   ├── epilogue1_iran_revolution.mp3
    │   ├── epilogue2_911_iraq_war.mp3
    │   └── epilogue3_oct7_gaza.mp3
    ├── clips\                  (截取片段)
    │   ├── 01_nasser_era.mp3
    │   ├── 02_1973_war.mp3
    │   ├── 03_beirut_siege.mp3
    │   ├── 04_iran_revolution.mp3
    │   ├── 05_iraq_invasion.mp3
    │   └── 06_gaza_war.mp3
    ├── transcripts\            (文字稿)
    │   ├── 01_nasser_era.txt
    │   ├── 02_1973_war.txt
    │   └── ...
    └── vocabulary\             (词汇表)
        ├── key_terms.txt
        └── people_places.txt
```

## 音频处理流程

### 步骤1: 下载完整音频
使用播客客户端或网站下载完整剧集

### 步骤2: 截取片段
使用音频编辑工具截取推荐段落

### 步骤3: 格式转换
- 转换为MP3
- 采样率: 44.1kHz
- 比特率: 128kbps
- 音量标准化

### 步骤4: 生成文字稿
使用语音识别API生成英文原文

### 步骤5: 生成词汇表
提取关键术语、人名、地名

## 转换为小程序关卡

| 片段 | 小程序关卡 | 时长 | 主题 |
|------|-----------|------|------|
| 01_nasser_era | Level 6 | 20分钟 | 纳赛尔与1967战争 |
| 02_1973_war | Level 7 | 20分钟 | 1973年赎罪日战争 |
| 03_beirut_siege | Level 8 | 20分钟 | 1982年黎巴嫩战争 |
| 04_iran_revolution | Level 9 | 20分钟 | 伊朗伊斯兰革命 |
| 05_iraq_invasion | Level 10 | 20分钟 | 2003年伊拉克战争 |
| 06_gaza_war | Level 11 | 15分钟 | 当前加沙冲突 |

## 推荐音频编辑工具

### 免费工具
1. **Audacity** (Windows/Mac/Linux)
   - 专业级音频编辑
   - 支持截取、合并、格式转换

2. **Ocenaudio** (Windows/Mac/Linux)
   - 简单易用
   - 实时预览效果

3. **GarageBand** (Mac/iOS)
   - 苹果用户免费
   - 功能强大

### 在线工具
1. **Audio Trimmer** (https://audiotrimmer.com/)
2. **MP3Cut** (https://mp3cut.net/)

## 批量处理脚本

我可以为你编写：
1. 音频信息提取脚本
2. 批量格式转换脚本
3. 文件名规范化脚本
4. 关卡配置生成脚本

需要哪个脚本？
