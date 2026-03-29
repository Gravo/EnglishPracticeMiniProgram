# Breaking Bad 音频素材整理方案

## 素材位置

**视频文件路径**: `E:\moive\Breaking Bad 01\`

### 可用视频文件

| 文件名 | 大小 | 集数 |
|--------|------|------|
| Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv | 464.62 MB | S01E01 |
| Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv | 385.60 MB | S01E02 |
| Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv | 385.48 MB | S01E03 |
| Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv | 385.98 MB | S01E04 |
| Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv | 385.39 MB | S01E05 |
| Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv | 384.47 MB | S01E06 |
| Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv | 381.64 MB | S01E07 |

### 英文字幕文件

每个视频都有对应的 .srt 字幕文件，可以直接用于提取对话文本！

---

## 学习内容规划

### 从入门到精通的学习路径

| 阶段 | 场景 | 对应集数 | 时长 |
|------|------|---------|------|
| **入门** | 打招呼、自我介绍 | S01E01 | 10分钟 |
| **初级** | 日常对话、问路 | S01E02 | 10分钟 |
| **初级** | 餐厅点餐、购物 | S01E03 | 10分钟 |
| **中级** | 医院场景、电话交流 | S01E04 | 10分钟 |
| **中级** | 家庭场景、情感表达 | S01E05 | 10分钟 |
| **高级** | 商业谈判、冲突对话 | S01E06 | 10分钟 |
| **精通** | 复杂情节、高难度表达 | S01E07 | 10分钟 |

---

## 详细关卡设计

### Level 1: 入门 - 打招呼 (S01E01)
**场景**: Walter White 和 Jesse Pinkman 的初次相遇
**难度**: Easy
**内容**:
- 日常问候语
- 简单的自我介绍
- 基础口语表达

**推荐截取段落**:
- 开场对话 (00:00 - 10:00)
- 实验室场景 (20:00 - 30:00)

---

### Level 2: 初级 - 问路与求助 (S01E02)
**场景**: Jesse 寻找毒贩、问路
**难度**: Easy
**内容**:
- 问路表达
- 求助与回应
- 口语化表达

---

### Level 3: 初级 - 餐厅场景 (S01E03)
**场景**: 餐厅对话
**难度**: Easy-Medium
**内容**:
- 点餐表达
- 日常对话
- 俚语学习

---

### Level 4: 中级 - 医院场景 (S01E04)
**场景**: Walter 在医院的对话
**难度**: Medium
**内容**:
- 医疗相关词汇
- 正式场合对话
- 复杂句型

---

### Level 5: 中级 - 家庭场景 (S01E05)
**场景**: Walter 与家人的对话
**难度**: Medium
**内容**:
- 家庭关系表达
- 情感描述
- 对话策略

---

### Level 6: 高级 - 商业谈判 (S01E06)
**场景**: Tuco 的谈判场景
**难度**: Medium-Hard
**内容**:
- 商业术语
- 谈判技巧
- 高难度词汇

---

### Level 7: 精通 - 复杂情节 (S01E07)
**场景**: 最终对决
**难度**: Hard
**内容**:
- 快速对话
- 专业术语
- 复杂情节理解

---

## 目录结构

```
E:\moive\Breaking Bad 01\
├── original\                    (原始视频)
│   ├── s01e01.mkv              (464 MB)
│   ├── s01e02.mkv              (385 MB)
│   └── ... (7集)
│
├── subtitles\                   (字幕文件)
│   ├── s01e01.srt              (5 KB)
│   ├── s01e02.srt
│   └── ...
│
└── (在下方新建以下目录)

D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\
├── clips\                      (截取片段 - MP3)
│   ├── 01_greeting.mp3         (10分钟)
│   ├── 02_asking_directions.mp3
│   ├── 03_restaurant.mp3
│   ├── 04_hospital.mp3
│   ├── 05_family.mp3
│   ├── 06_negotiation.mp3
│   └── 07_complex_dialogue.mp3
│
└── transcripts\                 (文字稿)
    ├── 01_greeting.txt
    ├── 02_asking_directions.txt
    └── ...
```

---

## 音频处理步骤

### 步骤1: 创建目录结构

在 `E:\moive\Breaking Bad 01\` 下创建:
- `clips\` (存放截取后的MP3)
- `transcripts\` (存放文字稿)

### 步骤2: 安装 FFmpeg

下载: https://ffmpeg.org/download.html

### 步骤3: 提取音频并截取

```bash
# Level 1: S01E01 开场 (00:00-10:00)
ffmpeg -i "Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "clips\01_greeting.mp3"

# Level 2: S01E02 问路 (00:00-10:00)
ffmpeg -i "Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "clips\02_asking_directions.mp3"

# Level 3: S01E03 餐厅 (00:00-10:00)
ffmpeg -i "Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "clips\03_restaurant.mp3"

# Level 4: S01E04 医院 (00:00-10:00)
ffmpeg -i "Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "clips\04_hospital.mp3"

# Level 5: S01E05 家庭 (00:00-10:00)
ffmpeg -i "Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "clips\05_family.mp3"

# Level 6: S01E06 谈判 (00:00-10:00)
ffmpeg -i "Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "clips\06_negotiation.mp3"

# Level 7: S01E07 复杂对话 (00:00-10:00)
ffmpeg -i "Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "clips\07_complex_dialogue.mp3"
```

**参数说明**:
- `-ss 0`: 从0秒开始
- `-t 600`: 持续600秒(10分钟)
- `-vn`: 不要视频
- `-ar 44100`: 采样率44.1kHz
- `-b:a 128k`: 音频比特率128k

### 步骤4: 复制到小程序

```
E:\moive\Breaking Bad 01\clips\*.mp3
  ↓
D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\
```

### 步骤5: 生成文字稿

从 .srt 字幕文件提取英文文本，复制到 transcripts\ 目录

---

## 字幕文件内容参考

Breaking Bad 的 .srt 字幕文件包含完整的英文对话文本，可以直接作为听写的原文！

例如 S01E01 的一些对话:
```
1
00:00:01,000 --> 00:00:02,500
Where are you from?

2
00:00:03,000 --> 00:00:04,500
I'm from New Mexico.

3
00:00:05,000 --> 00:00:07,000
Nice to meet you.
```

---

## 下一步

1. 安装 FFmpeg
2. 运行音频截取命令
3. 复制字幕文件到 transcripts\
4. 更新小程序 app.js 配置

需要我帮你写批量处理脚本吗？
