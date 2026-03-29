# 🎓 英语学习小程序 - Breaking Bad 专版

基于《绝命毒师》(Breaking Bad) 英文学习的微信小程序，支持**听力训练**、**口语练习**、**AI智能批改**等功能。

> 通过观看经典美剧片段，学习地道的英语表达！

## 📱 功能特性

| 功能 | 说明 |
|------|------|
| 🎧 **听力训练** | 多集 Breaking Bad 经典对话，支持AB复读、变速播放 |
| 📷 **拍照识别** | 拍照上传手写英文，AI自动批改 |
| 🤖 **AI 批改** | 腾讯混元大模型，智能语法纠错 |
| 🏆 **关卡挑战** | 7个难度递进的关卡，完成挑战解锁新内容 |
| 🔄 **学习记录** | 自动保存学习进度，追踪成长轨迹 |

## 🎬 关卡内容

| 关卡 | 名称 | 场景 | 来源 |
|------|------|------|------|
| Level 1 | 打招呼 | Walter 经典自我介绍 | S01E01 |
| Level 2 | 问路 | 迷路讨论 | S01E02 |
| Level 3 | 餐厅 | 家庭聚会 | S01E04 |
| Level 4 | 医院 | 医疗讨论 | S01E04+S01E05 |
| Level 5 | 家庭 | 亲情对话 | S01E01+S01E04 |
| Level 6 | 谈判 | 工作面试 | S01E05 |
| Level 7 | 复杂对话 | 化学讲解 | S01E03 |

## 🛠️ 技术栈

| 技术 | 说明 |
|------|------|
| 微信小程序 | 主应用框架 |
| 云开发 | 数据库、存储、云函数 |
| 腾讯混元 | AI 批改能力 |
| FFmpeg | 音频处理 |

## 📁 项目结构

```
EnglishPracticeMiniProgram/
├── app.js                    # 小程序入口
├── app.json                  # 全局配置
├── app.wxss                 # 全局样式
├── config/                   # 配置文件
│   ├── audio_config.js       # 音频资源配置
│   └── breaking_bad_levels.js  # 关卡配置
├── pages/                   # 页面
│   ├── index/               # 关卡列表
│   ├── player/              # 播放器
│   ├── scan/                # 拍照识别
│   ├── compare/             # 对照批改
│   └── profile/             # 个人中心
├── cloudfunctions/           # 云函数
│   ├── hunyuanChat/         # 混元AI对话
│   └── ocrRecognize/        # OCR识别
├── utils/                    # 工具函数
│   └── audioManager.js      # 音频管理器
├── assets/                   # 静态资源
│   ├── audio/               # 音频文件
│   └── icons/               # 图标
└── tools/                   # 开发工具
    └── subtitle_audio_extractor.py  # 字幕搜索提取工具
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/sige-audit/EnglishPracticeMiniProgram.git
cd EnglishPracticeMiniProgram
```

### 2. 安装依赖
```bash
# 安装云函数依赖
cd cloudfunctions/hunyuanChat
npm install

cd cloudfunctions/ocrRecognize
npm install
```

### 3. 配置云开发
1. 打开微信开发者工具
2. 导入项目
3. 开通云开发
4. 创建云数据库

### 4. 配置 API 密钥
在 `cloudfunctions/` 目录下创建环境变量：
```bash
# 腾讯云密钥
TENCENT_SECRET_ID=your_secret_id
TENCENT_SECRET_KEY=your_secret_key
```

## 🔧 开发工具

### 字幕搜索音频提取工具

基于 Python Tkinter 开发的桌面工具，用于从 Breaking Bad 字幕中搜索并提取音频片段。

**功能：**
- 关键词搜索所有 SRT 字幕
- 10个快速场景按钮
- 音频预览
- 合并导出
- 批量提取

**运行：**
```bash
cd tools
python subtitle_audio_extractor.py
```

## 📖 开发文档

- [Breaking Bad 音频提取策略](./docs/AUDIO_EXTRACTION_STRATEGY.md)
- [场景分析报告](./docs/SCENE_ANALYSIS_COMPLETE.md)
- [字幕提取实施方案](./docs/EXTRACTION_IMPLEMENTATION_SUMMARY.md)
- [集成文档](./docs/BREAKING_BAD_INTEGRATION.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👤 作者

- GitHub: [sige-audit](https://github.com/sige-audit)

## 🙏 致谢

- 《绝命毒师》版权归 AMC 所有
- 字幕来源：[射手网](https://assrt.net)

---

*学习英语，从 Breaking Bad 开始！*
