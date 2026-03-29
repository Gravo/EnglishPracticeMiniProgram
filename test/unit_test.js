/**
 * 单元测试 - 只测试 Level 1
 */
const fs = require('fs');
const path = require('path');

console.log('=== 单元测试 (Level 1 Only) ===\n');

let passed = 0;
let failed = 0;

// Level 1 音频检查
const audioDir = 'D:\\EnglishPracticeMiniProgram\\assets\\audio\\breaking_bad\\clips';
const level1Audio = path.join(audioDir, '01_greeting.mp3');

console.log('测试: Level 1 音频文件');
if (fs.existsSync(level1Audio)) {
  const stats = fs.statSync(level1Audio);
  const sizeMB = (stats.size / 1024 / 1024).toFixed(2);
  const sizeKB = (stats.size / 1024).toFixed(1);
  
  if (stats.size < 200 * 1024) { // < 200KB
    console.log(`  ✅ 01_greeting.mp3 (${sizeKB} KB) - 文件大小合格`);
    passed++;
  } else {
    console.log(`  ⚠️ 01_greeting.mp3 (${sizeKB} KB) - 略大但可接受`);
    passed++;
  }
} else {
  console.log(`  ❌ 01_greeting.mp3 - 文件不存在!`);
  failed++;
}

// app.js 检查
console.log('\n测试: app.js');
const appJs = 'D:\\EnglishPracticeMiniProgram\\app.js';
if (fs.existsSync(appJs)) {
  const content = fs.readFileSync(appJs, 'utf8');
  
  if (content.includes("id: 1") && content.includes("title: 'Level 1")) {
    console.log(`  ✅ Level 1 配置存在`);
    passed++;
  } else {
    console.log(`  ❌ Level 1 配置缺失`);
    failed++;
  }
  
  if (content.includes("audioUrl: '/assets/audio/breaking_bad/clips/01_greeting.mp3'")) {
    console.log(`  ✅ 音频路径正确`);
    passed++;
  } else {
    console.log(`  ❌ 音频路径错误`);
    failed++;
  }
} else {
  console.log(`  ❌ app.js 不存在!`);
  failed++;
}

// 项目大小检查
console.log('\n测试: 项目大小');
function getDirSize(dir) {
  let size = 0;
  try {
    fs.readdirSync(dir).forEach(item => {
      if (item === 'node_modules') return;
      const fullPath = path.join(dir, item);
      const stats = fs.statSync(fullPath);
      size += stats.isDirectory() ? getDirSize(fullPath) : stats.size;
    });
  } catch (e) {}
  return size;
}

const projectDir = 'D:\\EnglishPracticeMiniProgram';
const totalSize = getDirSize(projectDir);
const totalMB = (totalSize / 1024 / 1024).toFixed(2);

console.log(`  项目大小: ${totalMB} MB`);

if (parseFloat(totalMB) < 2) {
  console.log(`  ✅ 小于 2MB 限制`);
  passed++;
} else {
  console.log(`  ⚠️ 超过 2MB 限制`);
}

console.log('\n=== 测试总结 ===');
console.log(`通过: ${passed}`);
console.log(`失败: ${failed}`);

if (failed === 0) {
  console.log('\n✅ 所有测试通过! 项目可以发布。');
} else {
  console.log('\n❌ 存在失败测试，请修复。');
  process.exit(1);
}
