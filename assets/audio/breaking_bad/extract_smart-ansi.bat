@echo off
chcp 65001 >nul
REM ============================================
REM Breaking Bad Smart Audio Extraction Script
REM Scheme B: Cross-episode topic aggregation
REM Bitrate: 64k (optimized for speech)
REM ============================================

echo.
echo ============================================
echo  Breaking Bad Smart Audio Extraction
echo  Scheme: Cross-episode aggregation
echo  Bitrate: 64k (speech optimized)
echo ============================================
echo.

SET FFMPEG=D:\tools\ffmpeg\bin\ffmpeg.exe
SET SOURCE=E:\moive\Breaking Bad 01
SET OUTPUT=D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips
SET TEMP=D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\temp

REM 修改为你的实际文件名（请按实际情况修改）
SET FILE_EP01=Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv
SET FILE_EP02=Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv
SET FILE_EP03=Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv
SET FILE_EP04=Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv
SET FILE_EP05=Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv

REM Check FFmpeg
if not exist "%FFMPEG%" (
    echo [Error] FFmpeg not found!
    pause
    exit /b 1
)

REM Create directories
if not exist "%OUTPUT%" mkdir "%OUTPUT%"
if not exist "%TEMP%" mkdir "%TEMP%"

echo FFmpeg: %FFMPEG%
echo Output: %OUTPUT%
echo.

REM ============================================
REM Level 13: Asking directions (from S01E02)
REM ============================================
echo.
echo [Level 13] Extracting asking directions (S01E02)...
echo.

echo   Fragment 1/3: Getting lost (18 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP02%" -ss 120 -t 18 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\13_01.mp3"
if not exist "%TEMP%\13_01.mp3" ( echo   [Error] Fragment 1 failed & goto :skip13 )

echo   Fragment 2/3: Self-blame (7 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP02%" -ss 138 -t 7 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\13_02.mp3"
if not exist "%TEMP%\13_02.mp3" ( echo   [Error] Fragment 2 failed & goto :skip13 )

echo   Fragment 3/3: Whose house (13 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP02%" -ss 221 -t 13 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\13_03.mp3"
if not exist "%TEMP%\13_03.mp3" ( echo   [Error] Fragment 3 failed & goto :skip13 )

echo   Concatenating...
echo file '%TEMP:\=\\%\\13_01.mp3' > "%TEMP%\list13.txt"
echo file '%TEMP:\=\\%\\13_02.mp3' >> "%TEMP%\list13.txt"
echo file '%TEMP:\=\\%\\13_03.mp3' >> "%TEMP%\list13.txt"
"%FFMPEG%" -safe 0 -f concat -i "%TEMP%\list13.txt" -c copy "%OUTPUT%\02_asking_directions.mp3"
if exist "%OUTPUT%\02_asking_directions.mp3" (
    for %%F in ("%OUTPUT%\02_asking_directions.mp3") do echo   [OK] 02_asking_directions.mp3 (%%~zF bytes)
) else (
    echo   [Failed] Concatenation failed
)
:skip13

REM ============================================
REM Level 15: Hospital scenes (S01E04 + S01E05)
REM ============================================
echo.
echo [Level 15] Extracting hospital scenes (S01E04 + S01E05)...
echo.

echo   Fragment 1/4: Medical costs (38 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP04%" -ss 1077 -t 38 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_01.mp3"
if not exist "%TEMP%\15_01.mp3" ( echo   [Error] Fragment 1 failed & goto :skip15 )

echo   Fragment 2/4: Insurance (60 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP04%" -ss 1115 -t 60 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_02.mp3"
if not exist "%TEMP%\15_02.mp3" ( echo   [Error] Fragment 2 failed & goto :skip15 )

echo   Fragment 3/4: Job offer insurance (45 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP05%" -ss 810 -t 45 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_03.mp3"
if not exist "%TEMP%\15_03.mp3" ( echo   [Error] Fragment 3 failed & goto :skip15 )

echo   Fragment 4/4: Family talk (40 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP04%" -ss 875 -t 40 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\15_04.mp3"
if not exist "%TEMP%\15_04.mp3" ( echo   [Error] Fragment 4 failed & goto :skip15 )

echo   Concatenating...
echo file '%TEMP:\=\\%\\15_01.mp3' > "%TEMP%\list15.txt"
echo file '%TEMP:\=\\%\\15_02.mp3' >> "%TEMP%\list15.txt"
echo file '%TEMP:\=\\%\\15_03.mp3' >> "%TEMP%\list15.txt"
echo file '%TEMP:\=\\%\\15_04.mp3' >> "%TEMP%\list15.txt"
"%FFMPEG%" -safe 0 -f concat -i "%TEMP%\list15.txt" -c copy "%OUTPUT%\04_hospital.mp3"
if exist "%OUTPUT%\04_hospital.mp3" (
    for %%F in ("%OUTPUT%\04_hospital.mp3") do echo   [OK] 04_hospital.mp3 (%%~zF bytes)
) else (
    echo   [Failed] Concatenation failed
)
:skip15

REM ============================================
REM Level 16: Family scenes (S01E01 + S01E04)
REM ============================================
echo.
echo [Level 16] Extracting family scenes (S01E01 + S01E04)...
echo.

echo   Fragment 1/4: To Skyler (13 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP01%" -ss 155 -t 13 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_01.mp3"
if not exist "%TEMP%\16_01.mp3" ( echo   [Error] Fragment 1 failed & goto :skip16 )

echo   Fragment 2/4: To Walter Jr. (19 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP01%" -ss 168 -t 19 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_02.mp3"
if not exist "%TEMP%\16_02.mp3" ( echo   [Error] Fragment 2 failed & goto :skip16 )

echo   Fragment 3/4: Party (32 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP04%" -ss 163 -t 32 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_03.mp3"
if not exist "%TEMP%\16_03.mp3" ( echo   [Error] Fragment 3 failed & goto :skip16 )

echo   Fragment 4/4: Father-son talk (31 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP04%" -ss 573 -t 31 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\16_04.mp3"
if not exist "%TEMP%\16_04.mp3" ( echo   [Error] Fragment 4 failed & goto :skip16 )

echo   Concatenating...
echo file '%TEMP:\=\\%\\16_01.mp3' > "%TEMP%\list16.txt"
echo file '%TEMP:\=\\%\\16_02.mp3' >> "%TEMP%\list16.txt"
echo file '%TEMP:\=\\%\\16_03.mp3' >> "%TEMP%\list16.txt"
echo file '%TEMP:\=\\%\\16_04.mp3' >> "%TEMP%\list16.txt"
"%FFMPEG%" -safe 0 -f concat -i "%TEMP%\list16.txt" -c copy "%OUTPUT%\05_family.mp3"
if exist "%OUTPUT%\05_family.mp3" (
    for %%F in ("%OUTPUT%\05_family.mp3") do echo   [OK] 05_family.mp3 (%%~zF bytes)
) else (
    echo   [Failed] Concatenation failed
)
:skip16

REM ============================================
REM Level 17: Negotiation scenes (S01E05)
REM ============================================
echo.
echo [Level 17] Extracting negotiation scenes (S01E05)...
echo.

echo   Fragment 1/3: Interview (58 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP05%" -ss 4 -t 58 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\17_01.mp3"
if not exist "%TEMP%\17_01.mp3" ( echo   [Error] Fragment 1 failed & goto :skip17 )

echo   Fragment 2/3: Partnership offer (55 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP05%" -ss 140 -t 55 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\17_02.mp3"
if not exist "%TEMP%\17_02.mp3" ( echo   [Error] Fragment 2 failed & goto :skip17 )

echo   Fragment 3/3: Job offer (70 sec)...
"%FFMPEG%" -i "%SOURCE%\%FILE_EP05%" -ss 740 -t 70 -vn -ar 44100 -b:a 64k -ac 1 -y "%TEMP%\17_03.mp3"
if not exist "%TEMP%\17_03.mp3" ( echo   [Error] Fragment 3 failed & goto :skip17 )

echo   Concatenating...
echo file '%TEMP:\=\\%\\17_01.mp3' > "%TEMP%\list17.txt"
echo file '%TEMP:\=\\%\\17_02.mp3' >> "%TEMP%\list17.txt"
echo file '%TEMP:\=\\%\\17_03.mp3' >> "%TEMP%\list17.txt"
"%FFMPEG%" -safe 0 -f concat -i "%TEMP%\list17.txt" -c copy "%OUTPUT%\06_negotiation.mp3"
if exist "%OUTPUT%\06_negotiation.mp3" (
    for %%F in ("%OUTPUT%\06_negotiation.mp3") do echo   [OK] 06_negotiation.mp3 (%%~zF bytes)
) else (
    echo   [Failed] Concatenation failed
)
:skip17

REM ============================================
REM Level 18: Complex dialogue (S01E03)
REM ============================================
echo.
echo [Level 18] Extracting complex dialogue (S01E03)...
echo.

"%FFMPEG%" -i "%SOURCE%\%FILE_EP03%" -ss 45 -t 122 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\07_complex_dialogue.mp3"
if exist "%OUTPUT%\07_complex_dialogue.mp3" (
    for %%F in ("%OUTPUT%\07_complex_dialogue.mp3") do echo   [OK] 07_complex_dialogue.mp3 (%%~zF bytes)
) else (
    echo   [Failed]
)

REM ============================================
REM Clean up temporary files
REM ============================================
echo.
echo Cleaning temporary files...
if exist "%TEMP%" (
    del /q "%TEMP%\*.mp3" 2>nul
    del /q "%TEMP%\*.txt" 2>nul
    rmdir "%TEMP%" 2>nul
)

REM ============================================
REM Completion report
REM ============================================
echo.
echo ============================================
echo Extraction completed!
echo ============================================
echo.
echo Output files:
dir /b "%OUTPUT%\*.mp3"
echo.
echo File details:
dir "%OUTPUT%\*.mp3"
echo.
pause