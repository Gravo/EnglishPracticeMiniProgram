# 云开发环境配置

## 问题
错误提示：`Cloud API isn't enabled, please call wx.cloud.init first`

## 原因
app.js 中没有初始化云开发

## 已修复
已在 app.js 的 onLaunch 中添加：
```javascript
wx.cloud.init({
  env: 'cloud1', // 云开发环境ID
  traceUser: true
});
```

## 确认环境ID

### 查看你的环境ID：
1. 在微信开发者工具中点击 **"云开发"** 按钮
2. 看左上角显示的环境名称
3. 通常是 `cloud1-xxxxxx` 格式

### 如果环境ID不是 cloud1：

修改 `app.js` 中的配置：

```javascript
wx.cloud.init({
  env: '你的实际环境ID',  // <-- 改成你的环境ID
  traceUser: true
});
```

## 验证修复

1. 点击 **"编译"** 重新编译小程序
2. 在控制台应该看到：`云开发初始化成功`
3. 再次运行测试代码

## 备选方案

如果不确定环境ID，可以使用自动获取：

```javascript
wx.cloud.init({
  traceUser: true
});
```

这样会自动使用默认环境。
