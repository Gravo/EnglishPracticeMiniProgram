# FFmpeg 音频提取脚本
# 使用方法: 右键 -> 使用 PowerShell 运行

$ErrorActionPreference = "Continue"

$FFMPEG = "D:\tools\ffmpeg\bin\ffmpeg.exe"
$SOURCE = "E:\moive\Breaking Bad 01"
$OUTPUT = "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips"

Write-Host "=== Breaking Bad 音频提取 ===" -ForegroundColor Cyan
Write-Host ""

# 检查 FFmpeg
if (-not (Test-Path $FFMPEG)) {
    Write-Host "[错误] 未找到 FFmpeg: $FFMPEG" -ForegroundColor Red
    Write-Host "请先安装 FFmpeg" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}

# 创建输出目录
if (-not (Test-Path $OUTPUT)) {
    New-Item -ItemType Directory -Path $OUTPUT -Force | Out-Null
}

Write-Host "FFmpeg: $FFMPEG" -ForegroundColor Gray
Write-Host "源目录: $SOURCE" -ForegroundColor Gray
Write-Host "输出目录: $OUTPUT" -ForegroundColor Gray
Write-Host ""

# 音频配置
$clips = @(
    @{Name="01_greeting"; File="Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv"; Scene="打招呼"},
    @{Name="02_asking_directions"; File="Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv"; Scene="问路"},
    @{Name="03_restaurant"; File="Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv"; Scene="餐厅"},
    @{Name="04_hospital"; File="Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv"; Scene="医院"},
    @{Name="05_family"; File="Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv"; Scene="家庭"},
    @{Name="06_negotiation"; File="Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv"; Scene="谈判"},
    @{Name="07_complex_dialogue"; File="Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv"; Scene="复杂对话"}
)

$total = $clips.Count
$success = 0

Write-Host "开始提取音频..." -ForegroundColor Green
Write-Host ""

for ($i = 0; $i -lt $total; $i++) {
    $clip = $clips[$i]
    $srcFile = Join-Path $SOURCE $clip.File
    $outFile = Join-Path $OUTPUT "$($clip.Name).mp3"
    
    Write-Host "[$($i+1)/$total] $($clip.Name) ($($clip.Scene))..." -NoNewline
    
    if (-not (Test-Path $srcFile)) {
        Write-Host " 源文件不存在!" -ForegroundColor Red
        continue
    }
    
    try {
        & $FFMPEG -i $srcFile -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y $outFile 2>$null
        
        if (Test-Path $outFile) {
            $size = [math]::Round((Get-Item $outFile).Length / 1MB, 1)
            Write-Host " OK ($size MB)" -ForegroundColor Green
            $success++
        } else {
            Write-Host " 失败" -ForegroundColor Red
        }
    } catch {
        Write-Host " 错误: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "提取完成: $success/$total" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "输出目录: $OUTPUT" -ForegroundColor Gray
Write-Host ""

# 显示生成的文件
Get-ChildItem $OUTPUT -Filter "*.mp3" | ForEach-Object {
    $size = [math]::Round($_.Length / 1MB, 1)
    Write-Host "  $($_.Name) ($size MB)" -ForegroundColor Gray
}

Write-Host ""
Read-Host "按 Enter 退出"
