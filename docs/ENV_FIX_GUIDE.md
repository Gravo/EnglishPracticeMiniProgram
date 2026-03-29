# 云开发环境配置修复指南

## 错误分析
```
errCode: -501000 | errMsg: [100003] Param Invalid: env check invalid
```

这个错误表示云开发环境ID配置不正确。

## 修复步骤

### 步骤1：查看正确的环境ID

在微信开发者工具中：
1. 点击 **"云开发"** 按钮（☁️ 云朵图标）
2. 看左上角显示的环境名称
3. 格式类似：`cloud1-xxx` 或 `你的环境名称-xxx`

### 步骤2：获取环境ID

在云开发控制台：
1. 点击右上角 **"设置"**
2. 找到 **"环境ID"**
3. 复制这个ID

### 步骤3：修改 app.js

打开 `app.js`，找到：
```javascript
wx.cloud.init({
  traceUser: true
});
```

修改为：
```javascript
wx.cloud.init({
  env: '你的实际环境ID',  // <-- 替换为步骤2复制的ID
  traceUser: true
});
```

### 步骤4：修改 scan.js

打开 `pages/scan/scan.js`，在调用云函数的地方添加环境：

找到：
```javascript
wx.cloud.callFunction({
  name: 'ocrRecognize',
  data: { ... }
})
```

修改为：
```javascript
wx.cloud.callFunction({
  name: 'ocrRecognize',
  data: { ... },
  config: {
    env: '你的实际环境ID'  // <-- 替换为步骤2复制的ID
  }
})
```

## 快速诊断

在微信开发者工具控制台运行：
```javascript
// 查看当前云开发环境
console.log('云开发环境:', wx.cloud.DYNAMIC_CURRENT_ENV);

// 列出所有环境
wx.cloud.getCloudEnvList().then(res => {
  console.log('环境列表:', res);
});
```

## 备选方案

如果不知道环境ID，可以尝试：

1. **使用 DYNAMIC_CURRENT_ENV**
```javascript
wx.cloud.init({
  env: wx.cloud.DYNAMIC_CURRENT_ENV,
  traceUser: true
});
```

2. **完全删除 env 参数**
```javascript
wx.cloud.init({
  traceUser: true
});
```

3. **重新关联云开发环境**
   - 点击 "云开发" 按钮
   - 选择 "更换环境"
   - 选择正确的环境

## 验证修复

修复后，在控制台运行：
```javascript
wx.cloud.callFunction({
  name: 'ocrRecognize',
  data: { test: true }
}).then(res => {
  console.log('成功:', res);
}).catch(err => {
  console.log('失败:', err);
});
```

## 常见环境ID格式

- `cloud1-xxx` (自动生成)
- `你的小程序名称-xxx`
- `自定义名称-xxx`

**请告诉我你的实际环境ID，我帮你修改代码！**
