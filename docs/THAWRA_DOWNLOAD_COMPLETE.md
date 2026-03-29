# The Dig Thawra 播客完整下载指南

## 播客信息

**名称**: The Dig - Thawra (Revolution)
**主持人**: Daniel Denvir
**嘉宾**: Abdel Razzaq Takriti (历史学家)
**主题**: 20世纪阿拉伯激进主义历史
**版权**: 免费收听，允许截取学习使用

## 官方网站

- 主站: https://www.thedigradio.com/
- 播客页面: https://www.thedigradio.com/podcast

## 收听和下载平台

### 1. Apple Podcasts
https://podcasts.apple.com/us/podcast/the-dig/id1223744496
- 搜索: "The Dig Thawra"
- 支持离线下载

### 2. Spotify
https://open.spotify.com/show/2joN2r4JXnJdM6fJb9sU7j
- 搜索: "The Dig"
- 免费用户可收听

### 3. Google Podcasts
https://podcasts.google.com/feed/aHR0cHM6Ly90aGVkaWdyYWRpby5saWJzeW4uY29tL3Jzcw

### 4. Stitcher
https://www.stitcher.com/show/the-dig

### 5. RadioPublic
https://radiopublic.com/the-dig-WD0k1m

### 6. RSS Feed (直接订阅)
https://thedigradio.libsyn.com/rss

## 具体剧集链接

### Thawra 系列

| 剧集 | 标题 | 链接 |
|------|------|------|
| Ep.14 | Palestine and the 1967 War | https://www.thedigradio.com/podcast/thawra-ep-14-palestine-and-the-1967-war/ |
| Ep.15 | Black September and the 1973 War | https://www.thedigradio.com/podcast/thawra-ep-15-black-september-and-the-1973-war/ |
| Ep.16 | Lebanon and the 1982 War | https://www.thedigradio.com/podcast/thawra-ep-16-lebanon-and-the-1982-war/ |
| Epilogue 1 | Iran and the Iran-Iraq War | https://www.thedigradio.com/podcast/thawra-epilogue-1-iran-and-the-iran-iraq-war/ |
| Epilogue 2 | 9/11 and the Iraq War | https://www.thedigradio.com/podcast/thawra-epilogue-2-9-11-and-the-iraq-war/ |
| Epilogue 3 | October 7 and the Gaza War | https://www.thedigradio.com/podcast/thawra-epilogue-3-october-7-and-the-gaza-war/ |

## 下载方法

### 方法1: 使用播客客户端 (推荐)

1. **手机下载**
   - 安装 Apple Podcasts / Spotify / Pocket Casts
   - 搜索 "The Dig"
   - 找到 Thawra 系列
   - 点击下载按钮
   - 通过文件管理器导出音频文件

2. **电脑下载**
   - 使用 iTunes (Windows/Mac)
   - 订阅播客
   - 下载剧集
   - 找到文件位置导出

### 方法2: 使用 RSS 下载工具

**推荐工具**:
- **podcast-dl** (命令行工具)
  ```bash
  npm install -g podcast-dl
  podcast-dl https://thedigradio.libsyn.com/rss --episode "Thawra"
  ```

- **gPodder** (桌面应用)
  https://gpodder.github.io/

### 方法3: 浏览器扩展

- **Podcast Downloader** (Chrome扩展)
- **Audio Downloader Prime** (Firefox扩展)

### 方法4: 直接获取音频链接

1. 打开剧集网页
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 点击播放按钮
5. 找到 .mp3 请求
6. 右键 → Copy → Copy URL
7. 使用下载工具下载

## 音频处理步骤

### 1. 截取推荐片段

| 剧集 | 截取时间 | 时长 | 输出文件名 |
|------|---------|------|-----------|
| Ep.14 | 20:00 - 40:00 | 20min | 01_nasser_era.mp3 |
| Ep.15 | 30:00 - 50:00 | 20min | 02_1973_war.mp3 |
| Ep.16 | 00:00 - 20:00 | 20min | 03_beirut_siege.mp3 |
| Epilogue 1 | 10:00 - 30:00 | 20min | 04_iran_revolution.mp3 |
| Epilogue 2 | 30:00 - 50:00 | 20min | 05_iraq_invasion.mp3 |
| Epilogue 3 | 00:00 - 15:00 | 15min | 06_gaza_war.mp3 |

### 2. 使用 FFmpeg 处理

```bash
# 安装 FFmpeg: https://ffmpeg.org/download.html

# Ep.14: 纳赛尔时代 (20:00-40:00)
ffmpeg -i "ep14.mp3" -ss 1200 -t 1200 -ar 44100 -b:a 128k "01_nasser_era.mp3"

# Ep.15: 1973年战争 (30:00-50:00)
ffmpeg -i "ep15.mp3" -ss 1800 -t 1200 -ar 44100 -b:a 128k "02_1973_war.mp3"

# Ep.16: 贝鲁特围城 (00:00-20:00)
ffmpeg -i "ep16.mp3" -ss 0 -t 1200 -ar 44100 -b:a 128k "03_beirut_siege.mp3"

# Epilogue 1: 伊朗革命 (10:00-30:00)
ffmpeg -i "epilogue1.mp3" -ss 600 -t 1200 -ar 44100 -b:a 128k "04_iran_revolution.mp3"

# Epilogue 2: 伊拉克战争 (30:00-50:00)
ffmpeg -i "epilogue2.mp3" -ss 1800 -t 1200 -ar 44100 -b:a 128k "05_iraq_invasion.mp3"

# Epilogue 3: 加沙战争 (00:00-15:00)
ffmpeg -i "epilogue3.mp3" -ss 0 -t 900 -ar 44100 -b:a 128k "06_gaza_war.mp3"
```

### 3. 参数说明

- `-ss`: 开始时间（秒）
- `-t`: 持续时间（秒）
- `-ar`: 采样率 (44100 Hz)
- `-b:a`: 音频比特率 (128k)

## 目录结构

```
D:\downloads_english\
└── the_dig_thawra\
    ├── original\          (完整音频)
    │   ├── ep14.mp3
    │   ├── ep15.mp3
    │   ├── ep16.mp3
    │   ├── epilogue1.mp3
    │   ├── epilogue2.mp3
    │   └── epilogue3.mp3
    ├── clips\             (截取片段)
    │   ├── 01_nasser_era.mp3
    │   ├── 02_1973_war.mp3
    │   ├── 03_beirut_siege.mp3
    │   ├── 04_iran_revolution.mp3
    │   ├── 05_iraq_invasion.mp3
    │   └── 06_gaza_war.mp3
    └── transcripts\       (文字稿)
        ├── 01_nasser_era.txt
        └── ...
```

## 生成文字稿

### 方法1: 腾讯云语音识别
- 上传音频到腾讯云
- 使用语音识别API
- 获取英文原文

### 方法2: 其他工具
- **Whisper** (OpenAI)
- **Otter.ai**
- **Descript**

## 导入小程序

1. 复制音频到小程序目录:
   ```
   clips\01_nasser_era.mp3 → D:\EnglishPracticeMiniProgram\assets\audio\level_6_nasser_era.mp3
   ```

2. 更新 app.js 关卡配置

3. 测试音频播放

## 注意事项

1. **版权问题**: 该播客允许个人学习使用，但请勿商业传播
2. **文件大小**: 20分钟MP3约15-20MB，注意小程序包大小限制
3. **音质**: 播客音质足够听写练习使用

## 替代资源

如果下载困难，也可以考虑:
- VOA Learning English (中东专题)
- BBC Learning English (6 Minute English)
- 自己录制或AI生成内容
