# 子用户 english_teacher 权限配置指南

## 已创建子用户
- 用户名：english_teacher
- 用途：英语听写小程序OCR服务

---

## 步骤1：为子用户添加OCR权限

### 方法A：通过用户详情页添加（推荐）

1. 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
2. 点击右上角 **头像** → **"访问管理"**
3. 点击左侧 **"用户"** → **"用户列表"**
4. 找到 **english_teacher**，点击 **用户名称**
5. 点击 **"关联策略"**
6. 搜索以下策略并勾选：
   - **QcloudOCRFullAccess** （文字识别完全访问权限）✅ 推荐
   - 或 **QcloudOCRReadOnlyAccess** （只读权限）
7. 点击 **"确定"**

### 方法B：通过策略页面添加

1. 访问管理 → **"策略"**
2. 搜索 **"QcloudOCRFullAccess"**
3. 点击策略名称
4. 点击 **"关联用户/用户组"**
5. 选择 **english_teacher**
6. 点击 **"确定"**

---

## 步骤2：为子用户创建API密钥

1. 在用户列表中找到 **english_teacher**
2. 点击用户名称进入详情
3. 点击 **"API密钥"** 标签
4. 点击 **"新建密钥"**
5. 记录 **SecretId** 和 **SecretKey**
   - ⚠️ **SecretKey只显示一次，务必保存！**

---

## 步骤3：配置云函数环境变量

1. 打开微信开发者工具
2. 点击 **"云开发"** 按钮
3. 进入 **"云函数"**
4. 找到 **ocrRecognize**
5. 点击 **"版本与配置"**
6. 点击 **"配置"** 标签
7. 修改环境变量：

| 变量名 | 变量值 |
|--------|--------|
| TENCENT_SECRET_ID | english_teacher的SecretId |
| TENCENT_SECRET_KEY | english_teacher的SecretKey |

8. 点击 **"确定保存"**
9. **重新部署云函数**

---

## 步骤4：验证配置

### 测试1：检查权限
在腾讯云控制台：
1. 访问管理 → 用户 → english_teacher
2. 查看 **"关联策略"**
3. 确认有 **QcloudOCRFullAccess**

### 测试2：在线调试
1. 进入 [通用印刷体识别](https://console.cloud.tencent.com/ocr/general)
2. 切换用户为 english_teacher
3. 上传图片测试
4. 如果能识别，说明权限正常

### 测试3：小程序测试
1. 在微信开发者工具控制台运行：
```javascript
wx.cloud.callFunction({
  name: 'ocrRecognize',
  data: { imageBase64: 'test' }
}).then(res => console.log(res))
  .catch(err => console.error(err));
```

---

## 权限策略详情

### QcloudOCRFullAccess（推荐）
允许的操作：
- 所有文字识别接口
- 通用印刷体识别
- 英文识别
- 手写体识别
- 等全部OCR功能

### 自定义最小权限（可选）
如果只需要特定功能，可以创建自定义策略：

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "ocr:GeneralBasicOCR",
        "ocr:GeneralAccurateOCR",
        "ocr:EnglishOCR"
      ],
      "resource": "*"
    }
  ]
}
```

---

## 安全建议

1. **定期轮换密钥** - 每90天更换一次
2. **最小权限原则** - 只给必要的权限
3. **监控调用情况** - 在腾讯云查看调用日志
4. **设置告警** - 异常调用时接收通知

---

## 常见问题

### Q: 子用户和主用户有什么区别？
A: 子用户权限更可控，建议用子用户

### Q: 可以多个小程序共用同一个子用户吗？
A: 可以，但建议每个项目单独一个子用户

### Q: SecretKey泄露了怎么办？
A: 立即在控制台禁用或删除该密钥，创建新密钥

---

## 配置检查清单

- [ ] 子用户 english_teacher 已创建
- [ ] 已关联 QcloudOCRFullAccess 策略
- [ ] 已为子用户创建API密钥
- [ ] 已保存 SecretId 和 SecretKey
- [ ] 云函数环境变量已更新
- [ ] 云函数已重新部署
- [ ] OCR测试成功

---

**配置完成后告诉我，我帮你验证！**
