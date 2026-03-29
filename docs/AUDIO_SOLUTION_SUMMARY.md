# 完整音频获取方案

## 方案A：手动下载（最可靠）

### 步骤1：使用浏览器下载

1. 安装 Chrome 或 Firefox
2. 安装扩展 **"Video DownloadHelper"**
3. 访问播客页面
4. 播放音频
5. 点击扩展图标下载

### 步骤2：使用命令行工具 yt-dlp

```bash
# 安装 yt-dlp
pip install yt-dlp

# 下载播客（如果支持）
yt-dlp "https://www.thedigradio.com/podcast/thawra-ep-14-palestine-and-the-1967-war/"
```

### 步骤3：使用 RSS 解析

```bash
# 获取 RSS feed
curl https://thedigradio.libsyn.com/rss > feed.xml

# 解析获取音频链接
# 然后逐个下载
```

## 方案B：使用现成工具

### 推荐工具

1. **Podcast Addict** (Android)
   - 下载播客
   - 导出音频文件

2. **iTunes** (Windows/Mac)
   - 订阅播客
   - 下载后找到文件位置

3. **gPodder** (跨平台)
   - 开源播客客户端
   - https://gpodder.github.io/

## 方案C：直接联系作者

如果下载困难，可以：
- 发邮件给 Daniel Denvir 请求音频文件
- 在 Twitter/X 上联系 @DanDenvir
- 说明是用于英语学习目的

## 备选方案：使用其他资源

如果 The Dig 下载困难，可以使用：

### 1. VOA Learning English
https://learningenglish.voanews.com/
- 搜索 "Middle East"
- 大量免费音频+文字稿

### 2. BBC 6 Minute English
https://www.bbc.co.uk/learningenglish/english/features/6-minute-english
- 搜索中东相关话题

### 3. 自己录制
使用手机或电脑录制自己的朗读

## 当前状态

由于播客网站的限制，我无法直接帮你下载音频文件。

### 你能做的：

1. **使用播客客户端下载**（推荐）
   - 手机：Apple Podcasts, Spotify, Pocket Casts
   - 电脑：iTunes, gPodder

2. **使用浏览器扩展**
   - Video DownloadHelper
   - Audio Downloader Prime

3. **手动获取链接**
   - F12 打开开发者工具
   - Network 标签找到 .mp3
   - 复制链接用下载工具

### 我能做的：

一旦你下载了音频文件，我可以：
- ✓ 帮你处理音频（截取、转换格式）
- ✓ 生成处理脚本
- ✓ 创建小程序关卡配置
- ✓ 生成文字稿（使用语音识别）

## 下一步

请选择一个方案下载音频，然后告诉我：
1. 你是否成功下载了音频？
2. 需要我帮你处理音频吗？
3. 还是需要我推荐其他更容易获取的资源？
