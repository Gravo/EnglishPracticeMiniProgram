# 腾讯云OCR权限配置详细指南

## 错误信息
```
You are not authorized to perform operation (ocr:GeneralBasicOCR)
resource (*) has no permission
```

这表示你的腾讯云API密钥没有调用OCR服务的权限。

---

## 步骤1：确认OCR服务已开通

### 方法1：通过控制台检查

1. 打开 [腾讯云控制台](https://console.cloud.tencent.com/)
2. 在顶部搜索框输入 **"文字识别"** 或 **"OCR"**
3. 点击 **"文字识别"** 进入控制台

![OCR控制台](https://console.cloud.tencent.com/)

4. 如果看到以下界面，说明已开通：
   - 产品概述
   - 通用印刷体识别
   - 文字识别控制台

5. 如果提示 **"开通服务"**，点击开通（个人认证后有免费额度）

### 方法2：检查是否免费

- 个人认证用户：每月1000次免费
- 企业认证用户：每月10000次免费

---

## 步骤2：检查API密钥权限

### 2.1 查找API密钥

1. 点击右上角头像
2. 选择 **"访问管理"**
3. 点击 **"API密钥管理"**
4. 找到你正在使用的密钥（或者创建新密钥）

### 2.2 检查密钥权限

1. 在API密钥管理页面，点击密钥对应的 **"名称"**
2. 查看 **"关联策略"**
3. 检查是否有以下策略：
   - `QcloudOCRFullAccess` ✅ （完全访问，推荐）
   - `QcloudOCRReadOnlyAccess` ✅ （只读权限）
   - `AdministratorAccess` ✅ （管理员，完全权限）

### 2.3 如果没有权限，添加策略

#### 方式A：通过策略页面添加

1. 进入 [腾讯云策略控制台](https://console.cloud.tencent.com/policy)
2. 点击 **"创建自定义策略"**
3. 选择 **"按产品/功能/接口维度"**
4. 填写：
   - 产品/功能：**文字识别**
   - 接口：**全部接口**
5. 选择 **"关联用户/用户组/角色"**
6. 选择你的API密钥对应的角色

#### 方式B：直接关联预置策略

1. 在API密钥管理页面
2. 点击 **"关联策略"**
3. 搜索 `QcloudOCRFullAccess`
4. 勾选并确认

---

## 步骤3：确认环境变量配置正确

### 3.1 检查云函数环境变量

1. 打开微信开发者工具
2. 点击 **"云开发"** 按钮
3. 进入 **"云函数"** 页面
4. 找到 `ocrRecognize`
5. 点击 **"版本与配置"**
6. 查看 **"环境变量"**

确保有以下两个：
| 变量名 | 变量值 |
|--------|--------|
| TENCENT_SECRET_ID | 你的SecretId（如AKID...） |
| TENCENT_SECRET_KEY | 你的SecretKey（如...） |

### 3.2 如果变量不对，修改

1. 点击 **"编辑环境变量"**
2. 填入正确的值
3. 点击 **"确定"**
4. **重新部署云函数**

---

## 步骤4：测试OCR是否可用

### 4.1 腾讯云在线测试

1. 进入 [通用印刷体识别](https://console.cloud.tencent.com/ocr/general)
2. 点击 **"在线调试"**
3. 上传一张图片
4. 点击 **"发送请求"**
5. 如果返回结果，说明API正常

### 4.2 小程序中测试

1. 在微信开发者工具控制台运行：
```javascript
wx.cloud.callFunction({
  name: 'ocrRecognize',
  data: {
    imageBase64: 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
  }
}).then(res => {
  console.log('OCR结果:', res.result);
}).catch(err => {
  console.error('错误:', err);
});
```

---

## 常见问题

### Q: 提示"未开通服务"
A: 在腾讯云控制台开通文字识别服务

### Q: 提示"没有权限"
A: 按照步骤2添加OCR权限策略

### Q: 环境变量在哪设置？
A: 云开发 → 云函数 → ocrRecognize → 配置 → 环境变量

### Q: 密钥从哪找？
A: 访问管理 → API密钥管理

---

## 快速验证清单

- [ ] 腾讯云已登录
- [ ] 已开通文字识别（OCR）服务
- [ ] API密钥有OCR权限（QcloudOCRFullAccess）
- [ ] 云函数环境变量正确设置
- [ ] 云函数已重新部署

---

## 如需帮助

如果以上步骤都不行，请提供以下信息：
1. 腾讯云控制台OCR页面截图
2. API密钥关联的策略截图
3. 云函数环境变量截图
