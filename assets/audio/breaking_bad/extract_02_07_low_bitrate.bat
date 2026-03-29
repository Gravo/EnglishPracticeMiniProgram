@echo off
chcp 65001 >nul
REM ============================================
REM Breaking Bad 音频提取脚本 (低码率版)
REM 码率: 64k (适合语音学习，文件更小)
REM ============================================

echo.
echo ============================================
echo  Breaking Bad 音频提取 (第2-7集)
echo  码率: 64k (语音优化)
echo ============================================
echo.

SET FFMPEG=D:\tools\ffmpeg\bin\ffmpeg.exe
SET SOURCE=E:\moive\Breaking Bad 01
SET OUTPUT=D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips

REM 检查 FFmpeg
if not exist "%FFMPEG%" (
    echo [错误] 未找到 FFmpeg!
    echo 请确认 FFmpeg 已安装到: %FFMPEG%
    pause
    exit /b 1
)

echo FFmpeg: %FFMPEG%
echo 源目录: %SOURCE%
echo 输出目录: %OUTPUT%
echo 码率: 64k (语音优化)
echo.

REM 创建输出目录
if not exist "%OUTPUT%" (
    mkdir "%OUTPUT%"
    echo 创建输出目录成功
)

echo 开始提取音频...
echo.

REM 02 问路 - 提取关键对话片段
:extract_02
echo [2/7] 02_asking_directions.mp3
echo   提取场景: Jesse和Walter初次见面的对话...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 120 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\02_asking_directions.mp3" 2>nul
if exist "%OUTPUT%\02_asking_directions.mp3" (
    for %%F in ("%OUTPUT%\02_asking_directions.mp3") do echo   OK - 大小: %%~zF bytes
) else (
    echo   失败，尝试从开头提取...
    "%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\02_asking_directions.mp3" 2>nul
)

REM 03 餐厅 - 提取餐厅场景
:extract_03
echo [3/7] 03_restaurant.mp3
echo   提取场景: 餐厅点餐对话...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 300 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\03_restaurant.mp3" 2>nul
if exist "%OUTPUT%\03_restaurant.mp3" (
    for %%F in ("%OUTPUT%\03_restaurant.mp3") do echo   OK - 大小: %%~zF bytes
) else (
    echo   失败，尝试从开头提取...
    "%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\03_restaurant.mp3" 2>nul
)

REM 04 医院 - 提取医院场景
:extract_04
echo [4/7] 04_hospital.mp3
echo   提取场景: 医院对话...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 180 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\04_hospital.mp3" 2>nul
if exist "%OUTPUT%\04_hospital.mp3" (
    for %%F in ("%OUTPUT%\04_hospital.mp3") do echo   OK - 大小: %%~zF bytes
) else (
    echo   失败，尝试从开头提取...
    "%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\04_hospital.mp3" 2>nul
)

REM 05 家庭 - 提取家庭场景
:extract_05
echo [5/7] 05_family.mp3
echo   提取场景: Walter家庭对话...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 240 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\05_family.mp3" 2>nul
if exist "%OUTPUT%\05_family.mp3" (
    for %%F in ("%OUTPUT%\05_family.mp3") do echo   OK - 大小: %%~zF bytes
) else (
    echo   失败，尝试从开头提取...
    "%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\05_family.mp3" 2>nul
)

REM 06 谈判 - 提取商业谈判场景
:extract_06
echo [6/7] 06_negotiation.mp3
echo   提取场景: Walter和Jesse的交易谈判...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv" -ss 360 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\06_negotiation.mp3" 2>nul
if exist "%OUTPUT%\06_negotiation.mp3" (
    for %%F in ("%OUTPUT%\06_negotiation.mp3") do echo   OK - 大小: %%~zF bytes
) else (
    echo   失败，尝试从开头提取...
    "%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\06_negotiation.mp3" 2>nul
)

REM 07 复杂对话 - 提取化学对话场景
:extract_07
echo [7/7] 07_complex_dialogue.mp3
echo   提取场景: RV中的化学教学对话...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv" -ss 420 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\07_complex_dialogue.mp3" 2>nul
if exist "%OUTPUT%\07_complex_dialogue.mp3" (
    for %%F in ("%OUTPUT%\07_complex_dialogue.mp3") do echo   OK - 大小: %%~zF bytes
) else (
    echo   失败，尝试从开头提取...
    "%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\07_complex_dialogue.mp3" 2>nul
)

echo.
echo ============================================
echo 提取完成!
echo ============================================
echo.
echo 输出目录: %OUTPUT%
echo.
dir /b "%OUTPUT%\*.mp3"
echo.
pause
