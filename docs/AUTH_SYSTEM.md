# 微信登录与授权系统架构

## 系统概览

```
┌─────────────────────────────────────────────────────────────┐
│                    小程序客户端                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │  登录页面   │    │  页面守卫   │    │  授权管理器  │   │
│  │  login.js  │ -> │ authGuard  │ -> │ authManager │   │
│  └─────────────┘    └─────────────┘    └─────────────┘   │
│         │                   │                   │         │
│         v                   v                   v         │
│  ┌─────────────────────────────────────────────────┐     │
│  │              本地存储 (Storage)                   │     │
│  │  - wx_user_info      (微信用户信息)              │     │
│  │  - license_info      (激活码信息)                │     │
│  │  - levels_progress   (关卡进度)                │     │
│  └─────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 文件结构

```
utils/
├── authManager.js      ← 核心授权管理器
├── authGuard.js        ← 页面守卫
└── ...

pages/login/
├── login.js            ← 登录页面逻辑
├── login.wxml          ← 登录页面模板
├── login.wxss           ← 登录页面样式
└── login.json          ← 登录页面配置

pages/index/
└── index.js            ← 已整合授权检查
```

## 登录流程

```
用户打开小程序
      │
      ▼
┌─────────────┐
│ 检查存储状态 │
└─────────────┘
      │
      ▼
  ┌───────┴───────┐
  │               │
  ▼               ▼
未登录          已登录
  │               │
  ▼               ▼
显示登录页      检查激活状态
  │               │
  ▼               ▼
微信授权        ┌───┴───┐
  │            │         │
  ▼            ▼         ▼
获取用户信息   已激活    未激活
  │          │          │
  ▼          ▼          ▼
保存到Storage  允许使用  显示激活页
```

## 激活码验证

### 格式要求
- `XXXX-XXXX-XXXX-XXXX` 格式
- 或 8-32 位字母数字组合
- 或 8-16 位纯数字

### 验证流程

```
用户输入激活码
      │
      ▼
┌─────────────────┐
│ 1. 检查演示码    │ ── 是 ──→ 返回演示权限
└─────────────────┘
      │ 否
      ▼
┌─────────────────┐
│ 2. 本地校验和   │ ── 失败 ──→ 返回格式错误
└─────────────────┘
      │ 通过
      ▼
┌─────────────────┐
│ 3. 调用云函数   │ ← 实际生产环境应调用后端API
│    验证激活码    │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ 4. 保存激活信息 │ → 返回激活结果
└─────────────────┘
```

## 本地文件访问

### 微信小程序文件访问限制

| 能力 | 支持 | 说明 |
|------|------|------|
| `wx.chooseMessageFile` | ✅ | 选择聊天文件（最多100MB） |
| `wx.chooseImage` | ✅ | 选择图片 |
| `wx.getFileSystemManager` | ✅ | 读取用户选择的文件 |
| 直接访问本地路径 | ❌ | 沙箱限制，无法直接访问 |

### 使用场景

```
用户选择文件流程：
1. 用户点击"选择本地音频"
2. 弹出微信文件选择器
3. 用户从聊天记录或本地选择文件
4. 小程序获取文件临时路径
5. 使用 AudioContext 播放

支持的音频格式：
- MP3
- WAV  
- M4A
- OGG

支持的文本格式：
- TXT
- SRT（字幕）
- LRC（歌词）
- JSON
```

### 代码示例

```javascript
// 选择音频
wx.chooseMessageFile({
  count: 1,
  type: 'file',
  extension: ['mp3', 'wav'],
  success: (res) => {
    const audioPath = res.tempFiles[0].path;
    // 使用内部 AudioContext 播放
    innerAudioContext.src = audioPath;
  }
});

// 选择字幕/文本
wx.chooseMessageFile({
  count: 1,
  type: 'file',
  extension: ['txt', 'srt'],
  success: (res) => {
    const textPath = res.tempFiles[0].path;
    wx.getFileSystemManager().readFile({
      filePath: textPath,
      encoding: 'utf-8',
      success: (content) => {
        console.log('文件内容:', content.data);
      }
    });
  }
});
```

## 页面守卫

### 使用方式

```javascript
// 在页面的 onLoad 中调用
const authGuard = require('../../utils/authGuard.js');

Page({
  data: {},
  
  onLoad(options) {
    // 检查授权
    const auth = authGuard.checkPageAuth({
      requiredLogin: true,
      requiredActivation: true,
      redirectToLogin: true
    });
    
    if (!auth.allowed) {
      return; // 不继续执行
    }
    
    // 正常加载页面
    this.loadData();
  }
});
```

### 守卫规则

| 页面 | 需要登录 | 需要激活 |
|------|---------|---------|
| /pages/login/login | ❌ | ❌ |
| /pages/index/index | 部分 | ❌ |
| /pages/player/player | ✅ | ✅ |
| /pages/scan/scan | ✅ | ✅ |
| /pages/compare/compare | ✅ | ✅ |
| /pages/profile/profile | ✅ | ❌ |

## 数据存储

### Storage Key 说明

| Key | 内容 | 说明 |
|-----|------|------|
| `wx_user_info` | 微信用户信息 | 昵称、头像等 |
| `wx_login_code` | 登录凭证 | 用于服务端验证 |
| `wx_login_time` | 登录时间 | 用于判断登录有效性 |
| `license_info` | 激活信息 | 激活码、有效期等 |
| `levels_progress` | 关卡进度 | 各关卡的分数、状态 |

### license_info 结构

```javascript
{
  code: 'BBPRO-2024-ABCD-EFGH',  // 激活码
  checksum: '42',                 // 校验和
  salt: 'abc123...',              // 盐值
  type: 'premium',                // 激活类型
  expires: 1748563200000,          // 过期时间戳
  user: '用户昵称',               // 绑定的微信用户
  activatedAt: 1716028800000       // 激活时间
}
```

## 安全建议

### 生产环境必做

1. **激活码验证必须在服务端进行**
   ```javascript
   // 错误：前端验证（可被破解）
   if (code === 'MY_SECRET_CODE') { ... }
   
   // 正确：调用云函数验证
   const res = await wx.cloud.callFunction({
     name: 'verifyLicense',
     data: { code, wxUserInfo }
   });
   ```

2. **不要在前端存储激活码原文**
   - 只存储加密后的信息
   - 服务器端保存完整的激活码数据库

3. **使用 HTTPS**
   - 所有 API 调用必须使用 HTTPS
   - 防止中间人攻击

4. **限制激活码使用次数**
   - 每个码只能绑定有限设备
   - 记录设备指纹

### 激活码生成建议

```
激活码格式建议：
BB-PRO-XXXX-XXXX-XXXX-XXXX

结构：
- BB-PRO    : 产品标识
- XXXX      : 随机字符
- ...       : 校验位、时间戳等

示例：
BB-PRO-A3K9-M7F2-L5P8-Q1R4
```

## 演示模式

测试用激活码：

| 激活码 | 类型 | 有效期 |
|--------|------|--------|
| `BBDEMO-2024-FREE` | 演示 | 30天 |
| `BBTEST-12345678` | 测试 | 30天 |

> ⚠️ 仅用于开发测试，生产环境请删除

## 微信登录注意事项

1. **隐私合规**
   - 必须提供用户协议
   - 明确告知数据使用目的
   - 尊重用户选择权

2. **头像昵称获取**
   - 新版 API 需要用户主动点击授权
   - 建议使用 button 组件的 open-type="chooseAvatar"

3. **登录有效期**
   - `wx.login()` 的 code 有效期 5 分钟
   - `wx.checkSession()` 可检查 session 是否有效
   - 建议每次进入小程序时检查

## 更新日志

### v1.0 (2026-03-29)
- 实现微信登录功能
- 实现激活码系统
- 实现页面守卫
- 实现本地文件选择功能
- 整合到现有页面
