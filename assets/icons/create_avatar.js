// 使用代码生成简单的PNG头像
// 在微信开发者工具控制台运行

function createAvatar() {
  const canvas = document.createElement('canvas');
  canvas.width = 100;
  canvas.height = 100;
  const ctx = canvas.getContext('2d');
  
  // 背景圆
  ctx.fillStyle = '#4A90E2';
  ctx.beginPath();
  ctx.arc(50, 50, 50, 0, Math.PI * 2);
  ctx.fill();
  
  // 头像（白色圆形）
  ctx.fillStyle = '#fff';
  ctx.beginPath();
  ctx.arc(50, 40, 20, 0, Math.PI * 2);
  ctx.fill();
  
  // 身体
  ctx.beginPath();
  ctx.ellipse(50, 85, 30, 25, 0, 0, Math.PI * 2);
  ctx.fill();
  
  // 导出为图片
  const dataUrl = canvas.toDataURL('image/png');
  console.log('头像已生成，请右键保存为 default_avatar.png');
  console.log(dataUrl);
  
  return dataUrl;
}

createAvatar();
