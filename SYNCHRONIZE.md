# 多设备同步指南

## 在新电脑上克隆项目

### 1. 克隆仓库

在新电脑上打开终端/命令提示符：

```bash
git clone https://github.com/Gravo/EnglishPracticeMiniProgram.git
cd EnglishPracticeMiniProgram
```

### 2. 配置 Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 3. 拉取最新代码

```bash
git pull origin master
```

---

## 推送代码到 GitHub

### 1. 创建 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 登录你的 GitHub 账号
3. 点击 "Generate new token (classic)"
4. 设置：
   - **名称**: `EnglishPracticeMiniProgram`
   - **权限**: ✅ 勾选 `repo` (Full control of private repositories)
5. 点击 "Generate token"
6. **复制新生成的 Token**

### 2. 配置 Git 使用 Token

```bash
# 将你的用户名和 Token 替换下面的占位符
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/Gravo/EnglishPracticeMiniProgram.git

# 测试推送
git push origin master
```

---

## 常见问题

### Q: 克隆失败 "Authentication failed"
A: Token 无效或过期。请使用有效的 GitHub Token。

### Q: 如何把仓库转移到自己账号？
A: 
1. 在 GitHub 上 fork 这个仓库
2. 克隆你自己的 fork

### Q: 音频文件太大？
A: 音频文件（.mp3）已提交到 GitHub。如果不需要音频：
```bash
git clone --depth 1 https://github.com/Gravo/EnglishPracticeMiniProgram.git
```

---

## GitHub 仓库信息

| 项目 | 值 |
|------|-----|
| 地址 | https://github.com/Gravo/EnglishPracticeMiniProgram |
| 用户名 | Gravo |

---

## 安全提示

⚠️ **不要把 Token 写在代码或文档里！**

GitHub 有 secret-scanning，会自动检测并阻止包含 Token 的推送。

正确做法：
- Token 只保存在本地 Git 配置中
- 或使用 `git credential` 安全存储
