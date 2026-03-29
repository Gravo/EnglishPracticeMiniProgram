# OCR 配置测试指南

## 配置步骤

### 1. 填入API密钥

编辑 `config/ocr.config.js`:

```javascript
const OCR_CONFIG = {
  tencent: {
    secretId: 'YOUR_SECRET_ID',    // 替换为你的SecretId
    secretKey: 'YOUR_SECRET_KEY',  // 替换为你的SecretKey
    region: 'ap-beijing'
  },
  currentProvider: 'tencent'  // 切换到腾讯云
};
```

### 2. 配置云函数环境变量

在微信开发者工具中：
1. 右键 `cloudfunctions/ocrRecognize` 文件夹
2. 选择"创建并部署：云端安装依赖"
3. 部署成功后，右键选择"设置环境变量"
4. 添加：
   - `TENCENT_SECRET_ID` = 你的SecretId
   - `TENCENT_SECRET_KEY` = 你的SecretKey

### 3. 测试OCR功能

在微信开发者工具中：
1. 打开小程序
2. 进入任意关卡
3. 点击"扫描文本"
4. 拍照或选择图片
5. 点击"开始识别"

## 常见问题

### Q: 提示"未配置腾讯云API密钥"
A: 检查云函数环境变量是否设置正确

### Q: 提示"OCR服务调用失败"
A: 
1. 确认已在腾讯云开通OCR服务
2. 检查API密钥是否有OCR权限
3. 查看云函数日志获取详细错误

### Q: 识别结果为空
A: 
1. 确保图片清晰，文字可见
2. 检查图片是否过大（建议压缩到1MB以下）
3. 尝试使用英文识别模式

## 查看日志

在微信开发者工具中：
1. 点击"云开发"按钮
2. 选择"云函数"
3. 找到 `ocrRecognize`
4. 点击"日志"查看调用记录

## 费用说明

腾讯云OCR免费额度：
- 通用印刷体识别：每月1000次免费
- 超出后按次计费

查看用量：腾讯云控制台 → 文字识别 → 用量统计
