@echo off
chcp 65001 >nul
REM ============================================
REM Breaking Bad 智能音频提取脚本
REM 方案B: 跨集主题聚合
REM 码率: 64k (适合语音学习)
REM ============================================

echo.
echo ============================================
echo  Breaking Bad 智能音频提取
echo  方案: 跨集主题聚合
echo  码率: 64k (语音优化)
echo ============================================
echo.

SET FFMPEG=D:\tools\ffmpeg\bin\ffmpeg.exe
SET SOURCE=E:\moive\Breaking Bad 01
SET OUTPUT=D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips
SET TEMP=D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\temp

REM 检查 FFmpeg
if not exist "%FFMPEG%" (
    echo [错误] 未找到 FFmpeg!
    pause
    exit /b 1
)

REM 创建目录
if not exist "%OUTPUT%" mkdir "%OUTPUT%"
if not exist "%TEMP%" mkdir "%TEMP%"

echo FFmpeg: %FFMPEG%
echo 输出目录: %OUTPUT%
echo.

REM ============================================
REM Level 13: 问路场景 (从S01E02提取)
REM ============================================
echo.
echo [Level 13] 提取问路场景 (S01E02)...
echo.

REM 片段1: 迷路描述 (02:00-02:18)
echo   片段1/3: 迷路经历 (18秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 120 -t 18 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\13_01.mp3" 2>nul

REM 片段2: 自责 (02:18-02:25)
echo   片段2/3: 自责对话 (7秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 138 -t 7 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\13_02.mp3" 2>nul

REM 片段3: 去谁家 (03:41-03:54)
echo   片段3/3: 去谁家对话 (13秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 221 -t 13 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\13_03.mp3" 2>nul

REM 合并片段
echo   合并片段...
echo file '%TEMP:\=\\%\\13_01.mp3' > "%TEMP%\list13.txt"
echo file '%TEMP:\=\\%\\13_02.mp3' >> "%TEMP%\list13.txt"
echo file '%TEMP:\=\\%\\13_03.mp3' >> "%TEMP%\list13.txt"
"%FFMPEG%" -f concat -i "%TEMP%\list13.txt" -c copy "%OUTPUT%\02_asking_directions.mp3" 2>nul

if exist "%OUTPUT%\02_asking_directions.mp3" (
    for %%F in ("%OUTPUT%\02_asking_directions.mp3") do echo   [OK] 02_asking_directions.mp3 (%%~zF bytes)
) else (
    echo   [失败]
)

REM ============================================
REM Level 15: 医院场景 (从S01E04+S01E05提取)
REM ============================================
echo.
echo [Level 15] 提取医院场景 (S01E04+S01E05)...
echo.

REM S01E04 片段1: 医疗费用讨论 (17:57-18:35)
echo   片段1/4: 医疗费用 (38秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 1077 -t 38 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_01.mp3" 2>nul

REM S01E04 片段2: 保险讨论 (18:35-19:35)
echo   片段2/4: 保险讨论 (60秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 1115 -t 60 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_02.mp3" 2>nul

REM S01E05 片段3: Elliott提供保险 (13:30-14:15)
echo   片段3/4: 工作保险 (45秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 810 -t 45 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_03.mp3" 2>nul

REM S01E04 片段4: Skyler和Walt讨论 (14:35-15:15)
echo   片段4/4: 家庭讨论 (40秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 875 -t 40 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_04.mp3" 2>nul

REM 合并片段
echo   合并片段...
echo file '%TEMP:\=\\%\\15_01.mp3' > "%TEMP%\list15.txt"
echo file '%TEMP:\=\\%\\15_02.mp3' >> "%TEMP%\list15.txt"
echo file '%TEMP:\=\\%\\15_03.mp3' >> "%TEMP%\list15.txt"
echo file '%TEMP:\=\\%\\15_04.mp3' >> "%TEMP%\list15.txt"
"%FFMPEG%" -f concat -i "%TEMP%\list15.txt" -c copy "%OUTPUT%\04_hospital.mp3" 2>nul

if exist "%OUTPUT%\04_hospital.mp3" (
    for %%F in ("%OUTPUT%\04_hospital.mp3") do echo   [OK] 04_hospital.mp3 (%%~zF bytes)
) else (
    echo   [失败]
)

REM ============================================
REM Level 16: 家庭场景 (从S01E01+S01E04提取)
REM ============================================
echo.
echo [Level 16] 提取家庭场景 (S01E01+S01E04)...
echo.

REM S01E01 片段1: 对Skyler告白 (02:35-02:48)
echo   片段1/4: 对妻子告白 (13秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv" -ss 155 -t 13 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_01.mp3" 2>nul

REM S01E01 片段2: 对Walter Jr. (02:48-03:07)
echo   片段2/4: 对儿子的话 (19秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv" -ss 168 -t 19 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_02.mp3" 2>nul

REM S01E04 片段3: 烧烤聚会 (02:43-03:15)
echo   片段3/4: 家庭聚会 (32秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 163 -t 32 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_03.mp3" 2>nul

REM S01E04 片段4: Walter Jr.关心父亲 (09:33-10:04)
echo   片段4/4: 父子对话 (31秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 573 -t 31 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_04.mp3" 2>nul

REM 合并片段
echo   合并片段...
echo file '%TEMP:\=\\%\\16_01.mp3' > "%TEMP%\list16.txt"
echo file '%TEMP:\=\\%\\16_02.mp3' >> "%TEMP%\list16.txt"
echo file '%TEMP:\=\\%\\16_03.mp3' >> "%TEMP%\list16.txt"
echo file '%TEMP:\=\\%\\16_04.mp3' >> "%TEMP%\list16.txt"
"%FFMPEG%" -f concat -i "%TEMP%\list16.txt" -c copy "%OUTPUT%\05_family.mp3" 2>nul

if exist "%OUTPUT%\05_family.mp3" (
    for %%F in ("%OUTPUT%\05_family.mp3") do echo   [OK] 05_family.mp3 (%%~zF bytes)
) else (
    echo   [失败]
)

REM ============================================
REM Level 17: 谈判场景 (从S01E05提取)
REM ============================================
echo.
echo [Level 17] 提取谈判场景 (S01E05)...
echo.

REM 片段1: 面试 (00:04-01:02)
echo   片段1/3: 工作面试 (58秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 4 -t 58 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\17_01.mp3" 2>nul

REM 片段2: Jesse和Badger (02:20-03:15)
echo   片段2/3: 合作提议 (55秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 140 -t 55 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\17_02.mp3" 2>nul

REM 片段3: Elliott给offer (12:20-13:30)
echo   片段3/3: 工作邀请 (70秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 740 -t 70 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\17_03.mp3" 2>nul

REM 合并片段
echo   合并片段...
echo file '%TEMP:\=\\%\\17_01.mp3' > "%TEMP%\list17.txt"
echo file '%TEMP:\=\\%\\17_02.mp3' >> "%TEMP%\list17.txt"
echo file '%TEMP:\=\\%\\17_03.mp3' >> "%TEMP%\list17.txt"
"%FFMPEG%" -f concat -i "%TEMP%\list17.txt" -c copy "%OUTPUT%\06_negotiation.mp3" 2>nul

if exist "%OUTPUT%\06_negotiation.mp3" (
    for %%F in ("%OUTPUT%\06_negotiation.mp3") do echo   [OK] 06_negotiation.mp3 (%%~zF bytes)
) else (
    echo   [失败]
)

REM ============================================
REM Level 18: 复杂对话 (从S01E03提取)
REM ============================================
echo.
echo [Level 18] 提取复杂对话 (S01E03)...
echo.

REM 片段1: 化学讲解完整版 (00:45-02:47)
echo   片段1/1: 人体化学组成 (122秒)...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 45 -t 122 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\07_complex_dialogue.mp3" 2>nul

if exist "%OUTPUT%\07_complex_dialogue.mp3" (
    for %%F in ("%OUTPUT%\07_complex_dialogue.mp3") do echo   [OK] 07_complex_dialogue.mp3 (%%~zF bytes)
) else (
    echo   [失败]
)

REM ============================================
REM 清理临时文件
REM ============================================
echo.
echo 清理临时文件...
del /q "%TEMP%\*.mp3" 2>nul
del /q "%TEMP%\*.txt" 2>nul
rmdir "%TEMP%" 2>nul

REM ============================================
REM 完成报告
REM ============================================
echo.
echo ============================================
echo 提取完成!
echo ============================================
echo.
echo 输出文件:
dir /b "%OUTPUT%\*.mp3"
echo.
echo 文件详情:
dir "%OUTPUT%\*.mp3"
echo.
pause
