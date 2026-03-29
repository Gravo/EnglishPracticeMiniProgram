# Breaking Bad 音频素材处理完整指南

## 当前状态

### ✅ 已完成
- [x] 视频文件扫描 (E:\moive\Breaking Bad 01\)
- [x] 7集视频文件确认
- [x] 字幕文件确认 (.srt)
- [x] 学习内容规划
- [x] 关卡配置文件
- [x] 批处理脚本

### ⏳ 待完成
- [ ] 安装 FFmpeg
- [ ] 提取音频
- [ ] 复制字幕
- [ ] 复制到小程序目录
- [ ] 更新 app.js

---

## 步骤1: 安装 FFmpeg

### 方法A: 下载压缩包 (推荐)

1. 访问: https://ffmpeg.org/download.html
2. 点击 Windows 版本链接
3. 下载 "ffmpeg-7.1-essentials_build.zip"
4. 解压到 `D:\tools\ffmpeg\`
5. 应该看到 `D:\tools\ffmpeg\bin\ffmpeg.exe`

### 方法B: winget (如果可用)

```powershell
winget install ffmpeg
```

### 方法C: Chocolatey

```powershell
choco install ffmpeg
```

---

## 步骤2: 添加到系统 PATH

1. 右键 "此电脑" → 属性 → 高级系统设置
2. 点击 "环境变量"
3. 在 "系统变量" 中找到 "Path"，双击
4. 点击 "新建"，添加: `D:\tools\ffmpeg\bin`
5. 确定保存

**验证安装:**
打开新的命令提示符，输入:
```
ffmpeg -version
```

---

## 步骤3: 运行音频提取脚本

1. 打开文件资源管理器
2. 导航到: `E:\moive\Breaking Bad 01\`
3. 双击运行 `extract_audio.bat`
4. 等待处理完成

**脚本内容预览:**
```
提取以下7个音频片段 (每个10分钟):
- 01_greeting.mp3 (打招呼)
- 02_asking_directions.mp3 (问路)
- 03_restaurant.mp3 (餐厅)
- 04_hospital.mp3 (医院)
- 05_family.mp3 (家庭)
- 06_negotiation.mp3 (谈判)
- 07_complex_dialogue.mp3 (复杂对话)
```

---

## 步骤4: 创建小程序目录

在 `D:\EnglishPracticeMiniProgram\assets\audio\` 下创建:

```
breaking_bad\
├── clips\           (放7个MP3文件)
├── transcripts\     (放字幕/文字稿)
└── vocabulary\     (放词汇表)
```

**快速创建:**
```cmd
cd D:\EnglishPracticeMiniProgram\assets\audio
mkdir breaking_bad
cd breaking_bad
mkdir clips transcripts vocabulary
```

---

## 步骤5: 复制文件

### 复制音频
从 `E:\moive\Breaking Bad 01\clips\` 复制到 `D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\`

### 复制字幕
1. 打开 `E:\moive\Breaking Bad 01\`
2. 复制所有 `.srt` 文件
3. 粘贴到 `D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\`
4. 可选: 重命名为 `.txt` 后缀

---

## 步骤6: 更新小程序配置

### 复制关卡配置

复制 `config/breaking_bad_levels.js` 中的配置到 `app.js`

### 或者创建新的 app.js 配置块

```javascript
// 在 app.js 中找到 defaultLevels 数组
// 在现有关卡后添加:

const breakingBadLevels = [
  {
    id: 12,
    title: 'Level 12: Breaking Bad - 打招呼',
    audioUrl: '/assets/audio/breaking_bad/clips/01_greeting.mp3',
    // ... 其他配置见 config/breaking_bad_levels.js
  },
  // ... 7个关卡
];

// 合并关卡
const allLevels = [...originalLevels, ...breakingBadLevels];
```

---

## 目录结构最终状态

```
D:\EnglishPracticeMiniProgram\
├── assets\
│   └── audio\
│       └── breaking_bad\
│           ├── clips\
│           │   ├── 01_greeting.mp3
│           │   ├── 02_asking_directions.mp3
│           │   ├── 03_restaurant.mp3
│           │   ├── 04_hospital.mp3
│           │   ├── 05_family.mp3
│           │   ├── 06_negotiation.mp3
│           │   └── 07_complex_dialogue.mp3
│           ├── transcripts\
│           │   ├── 01_greeting.srt
│           │   └── ...
│           └── vocabulary\
│               └── key_terms.txt
├── config\
│   └── breaking_bad_levels.js
└── app.js (已更新)
```

---

## 验证清单

- [ ] FFmpeg 已安装并可运行
- [ ] 7个 MP3 文件已生成
- [ ] 音频文件在正确目录
- [ ] app.js 已更新关卡配置
- [ ] 小程序可正常编译
- [ ] 音频播放功能正常

---

## 预期结果

完成后，你的小程序将包含:

| 关卡 | 场景 | 难度 |
|------|------|------|
| 1-5 | 原有政治历史关卡 | 入门到精通 |
| 12 | Breaking Bad - 打招呼 | 入门 |
| 13 | Breaking Bad - 问路 | 入门 |
| 14 | Breaking Bad - 餐厅 | 初级 |
| 15 | Breaking Bad - 医院 | 中级 |
| 16 | Breaking Bad - 家庭 | 中级 |
| 17 | Breaking Bad - 谈判 | 高级 |
| 18 | Breaking Bad - 复杂对话 | 精通 |

---

## 需要帮助?

如果遇到问题:
1. 检查 FFmpeg 是否正确安装
2. 检查文件路径是否正确
3. 检查字幕文件是否可读

也可以手动使用 FFmpeg:
```cmd
ffmpeg -i "E:\moive\Breaking Bad 01\Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\01_greeting.mp3"
```
