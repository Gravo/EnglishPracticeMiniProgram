@echo off
chcp 65001 >nul
REM ============================================
REM Breaking Bad 音频提取脚本
REM 需要先安装 FFmpeg 到 D:\tools\ffmpeg\bin\
REM ============================================

echo.
echo ============================================
echo  Breaking Bad 音频提取
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
echo.

REM 创建输出目录
if not exist "%OUTPUT%" (
    mkdir "%OUTPUT%"
    echo 创建输出目录成功
)

echo 开始提取音频...
echo.

REM 01 打招呼
echo [1/7] 01_greeting.mp3
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\01_greeting.mp3"
if exist "%OUTPUT%\01_greeting.mp3" echo   OK

REM 02 问路
echo [2/7] 02_asking_directions.mp3
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\02_asking_directions.mp3"
if exist "%OUTPUT%\02_asking_directions.mp3" echo   OK

REM 03 餐厅
echo [3/7] 03_restaurant.mp3
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\03_restaurant.mp3"
if exist "%OUTPUT%\03_restaurant.mp3" echo   OK

REM 04 医院
echo [4/7] 04_hospital.mp3
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\04_hospital.mp3"
if exist "%OUTPUT%\04_hospital.mp3" echo   OK

REM 05 家庭
echo [5/7] 05_family.mp3
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\05_family.mp3"
if exist "%OUTPUT%\05_family.mp3" echo   OK

REM 06 谈判
echo [6/7] 06_negotiation.mp3
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\06_negotiation.mp3"
if exist "%OUTPUT%\06_negotiation.mp3" echo   OK

REM 07 复杂对话
echo [7/7] 07_complex_dialogue.mp3
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\07_complex_dialogue.mp3"
if exist "%OUTPUT%\07_complex_dialogue.mp3" echo   OK

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
