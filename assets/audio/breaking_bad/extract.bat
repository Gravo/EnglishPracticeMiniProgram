@echo off
chcp 65001 >nul
REM ============================================
REM Breaking Bad 音频提取脚本 (对话精华版)
REM 基于字幕分析，提取最佳对话片段
REM ============================================

echo.
echo ============================================
echo  Breaking Bad 音频提取
echo ============================================
echo.

SET FFMPEG=D:\tools\ffmpeg\bin\ffmpeg.exe
SET SOURCE=E:\moive\Breaking Bad 01
SET OUTPUT=D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips

if not exist "%FFMPEG%" (
    echo [错误] 未找到 FFmpeg!
    pause
    exit /b 1
)

echo FFmpeg: %FFMPEG%
echo 源目录: %SOURCE%
echo 输出目录: %OUTPUT%
echo.

REM ============================================
REM 基于字幕分析的最佳片段参数
REM ============================================

echo [1/7] S01E01 打招呼 - 00:12:19开始，71秒
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv" -ss 739 -t 71 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\01_greeting.mp3"

echo [2/7] S01E02 问路 - 00:15:21开始，115秒
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 921 -t 115 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\02_asking_directions.mp3"

echo [3/7] S01E03 餐厅 - 00:12:56开始，147秒
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 776 -t 147 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\03_restaurant.mp3"

echo [4/7] S01E04 医院 - 00:23:03开始，139秒
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 1383 -t 139 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\04_hospital.mp3"

echo [5/7] S01E05 家庭 - 00:01:21开始，112秒
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 81 -t 112 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\05_family.mp3"

echo [6/7] S01E06 谈判 - 00:31:46开始，108秒
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv" -ss 1906 -t 108 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\06_negotiation.mp3"

echo [7/7] S01E07 复杂对话 - 00:24:28开始，76秒
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv" -ss 1468 -t 76 -vn -ar 44100 -b:a 128k -y "%OUTPUT%\07_complex_dialogue.mp3"

echo.
echo ============================================
echo 提取完成!
echo ============================================
echo.
dir /b "%OUTPUT%\*.mp3"
pause
