# 手动创建下载目录指南

## 目录结构

在 D盘 创建以下文件夹：

```
D:\downloads_english\
├── middle_east_history\      (中东历史)
├── modern_conflicts\          (现代冲突)
├── us_foreign_policy\         (美国外交政策)
├── transcripts\               (文字稿)
└── vocabulary\                (词汇表)
```

## 创建步骤

### 方法1：使用文件资源管理器

1. 打开 **此电脑** → **D盘**
2. 右键空白处 → **新建** → **文件夹**
3. 命名为 `downloads_english`
4. 双击进入 `downloads_english`
5. 依次创建5个子文件夹

### 方法2：使用命令提示符

1. 按 `Win + R`，输入 `cmd`，回车
2. 输入以下命令：

```cmd
cd /d D:\
mkdir downloads_english
cd downloads_english
mkdir middle_east_history
mkdir modern_conflicts
mkdir us_foreign_policy
mkdir transcripts
mkdir vocabulary
```

### 方法3：使用PowerShell

1. 按 `Win + X`，选择 **Windows PowerShell**
2. 输入：

```powershell
New-Item -ItemType Directory -Path "D:\downloads_english\middle_east_history" -Force
New-Item -ItemType Directory -Path "D:\downloads_english\modern_conflicts" -Force
New-Item -ItemType Directory -Path "D:\downloads_english\us_foreign_policy" -Force
New-Item -ItemType Directory -Path "D:\downloads_english\transcripts" -Force
New-Item -ItemType Directory -Path "D:\downloads_english\vocabulary" -Force
```

## 下载内容规划

### 目标：5-10篇中东主题音频

| 序号 | 主题 | 时长 | 难度 | 保存位置 |
|-----|------|-----|------|---------|
| 01 | Oil in the Middle East | 2-3分钟 | 中等 | middle_east_history |
| 02 | The Creation of Israel | 2-3分钟 | 中等 | middle_east_history |
| 03 | The 1973 Oil Crisis | 2-3分钟 | 中等 | modern_conflicts |
| 04 | The Iran-Iraq War | 3-4分钟 | 较难 | modern_conflicts |
| 05 | The Gulf War | 3-4分钟 | 较难 | modern_conflicts |
| 06 | US Policy in Middle East | 2-3分钟 | 中等 | us_foreign_policy |
| 07 | The Arab Spring | 3-4分钟 | 较难 | modern_conflicts |
| 08 | Syrian Civil War | 3-4分钟 | 较难 | modern_conflicts |
| 09 | ISIS and Terrorism | 2-3分钟 | 中等 | modern_conflicts |
| 10 | Israel-Palestine Conflict | 3-4分钟 | 较难 | middle_east_history |

## 推荐下载来源

### 1. VOA Learning English
https://www.manythings.org/voa/
- 搜索关键词: oil, Israel, Iran, Iraq, war, Middle East
- 下载MP3和文字稿

### 2. BBC 6 Minute English
https://www.bbc.co.uk/learningenglish/english/features/6-minute-english
- 搜索中东相关话题

### 3. Breaking News English
https://breakingnewsenglish.com/
- 当前新闻，分级难度

### 4. 中文资源（参考）
- 观察者网国际版
- 澎湃新闻国际
- 用于理解背景

## 文件命名规范

```
[序号]_[主题关键词]_[时长]_[来源].[mp3/txt]

示例：
01_oil_middle_east_3min_voa.mp3
01_oil_middle_east_3min_voa.txt (文字稿)
```

## 转换为小程序关卡

收集完成后，可以：
1. 调整音频时长（60-180秒）
2. 提取核心句子作为原文
3. 生成关键词汇表
4. 导入小程序作为新关卡

需要我帮你写转换脚本吗？
