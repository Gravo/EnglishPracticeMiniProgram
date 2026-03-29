@echo off
chcp 65001 >nul
REM ============================================
REM 音频压缩脚本 - 适配小程序2MB限制
REM 使用64kbps压缩，大幅减小文件体积
REM ============================================

echo.
echo ============================================
echo  音频压缩脚本
echo  将128kbps压缩为32kbps，适配小程序2MB限制
echo ============================================
echo.

SET FFMPEG=D:\tools\ffmpeg\bin\ffmpeg.exe
SET SOURCE=D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips

echo 源目录: %SOURCE%
echo.

REM 压缩所有MP3文件
echo 开始压缩音频文件...
echo.

for %%f in ("%SOURCE%\*.mp3") do (
    echo 压缩: %%~nxf
    "%FFMPEG%" -i "%%f" -vn -ar 22050 -b:a 32k -y "%%f.tmp" 2>nul
    if exist "%%f.tmp" (
        move /y "%%f.tmp" "%%f" >nul
        for %%s in ("%%f") do echo   完成: %%~zs bytes
    )
)

echo.
echo ============================================
echo  压缩完成！
echo ============================================
echo.
pause
