# Breaking Bad 音频提取 - 完成脚本
# 运行此脚本完成剩余提取工作

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Breaking Bad 音频提取 - 完成脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 配置
$ffmpeg = "D:\tools\ffmpeg\bin\ffmpeg.exe"
$source = "E:\moive\Breaking Bad 01"
$output = "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips"
$transcripts = "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts"

# 检查 FFmpeg
if (-not (Test-Path $ffmpeg)) {
    Write-Host "[错误] 未找到 FFmpeg: $ffmpeg" -ForegroundColor Red
    Write-Host "请从 https://ffmpeg.org 下载并安装 FFmpeg" -ForegroundColor Yellow
    exit 1
}

Write-Host "FFmpeg: $ffmpeg" -ForegroundColor Green
Write-Host "输出目录: $output" -ForegroundColor Green
Write-Host ""

# ============================================
# 1. 提取 03_restaurant.mp3
# ============================================
Write-Host "[1/3] 提取餐厅场景..." -ForegroundColor Cyan

$restaurantFile = Join-Path $output "03_restaurant.mp3"
if (Test-Path $restaurantFile) {
    Write-Host "  03_restaurant.mp3 已存在，跳过" -ForegroundColor Gray
} else {
    $s01e04 = Join-Path $source "Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv"
    Write-Host "  从 S01E04 提取 (02:43-03:15, 32秒)..." -ForegroundColor Yellow

    & $ffmpeg -i $s01e04 -ss 163 -t 32 -vn -ar 44100 -b:a 64k -ac 1 -y $restaurantFile 2>&1 | Out-Null

    if (Test-Path $restaurantFile) {
        $size = (Get-Item $restaurantFile).Length / 1KB
        Write-Host "  [OK] 03_restaurant.mp3 ($([math]::Round($size,1)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  [失败] 无法创建 03_restaurant.mp3" -ForegroundColor Red
    }
}

# ============================================
# 2. 替换字幕文件
# ============================================
Write-Host ""
Write-Host "[2/3] 更新字幕文件..." -ForegroundColor Cyan

$newFiles = @(
    "02_asking_directions",
    "03_restaurant",
    "04_hospital",
    "05_family",
    "06_negotiation",
    "07_complex_dialogue"
)

foreach ($name in $newFiles) {
    $newFile = Join-Path $transcripts "${name}_new.txt"
    $targetFile = Join-Path $transcripts "${name}.txt"

    if (Test-Path $newFile) {
        Copy-Item $newFile $targetFile -Force
        Write-Host "  [OK] ${name}.txt" -ForegroundColor Green
    } else {
        Write-Host "  [跳过] ${name}_new.txt 不存在" -ForegroundColor Gray
    }
}

# ============================================
# 3. 验证结果
# ============================================
Write-Host ""
Write-Host "[3/3] 验证提取结果..." -ForegroundColor Cyan
Write-Host ""

$mp3Files = Get-ChildItem $output -Filter "*.mp3"
$totalSize = 0
$totalDuration = 0

Write-Host "音频文件:" -ForegroundColor White
Write-Host "--------" -ForegroundColor Gray

foreach ($file in $mp3Files) {
    $sizeKB = [math]::Round($file.Length / 1KB, 1)
    $totalSize += $file.Length

    # 获取时长
    $info = & $ffmpeg -i $file.FullName 2>&1 | Select-String "Duration"
    $duration = ""
    if ($info -match "Duration: (\d{2}:\d{2}:\d{2})") {
        $duration = $matches[1]
    }

    Write-Host "  $($file.Name) | $sizeKB KB | $duration" -ForegroundColor White
}

Write-Host ""
Write-Host "总计: $([math]::Round($totalSize/1MB,2)) MB" -ForegroundColor Cyan

$txtFiles = Get-ChildItem $transcripts -Filter "*.txt" | Where-Object { $_.Name -notlike "*_new.txt" }
Write-Host "字幕文件: $($txtFiles.Count) 个" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " 提取完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "1. 在微信开发者工具中测试音频播放" -ForegroundColor White
Write-Host "2. 更新 config/breaking_bad_levels.js 中的 originalText 字段" -ForegroundColor White
Write-Host "3. 测试小程序功能" -ForegroundColor White
Write-Host ""
