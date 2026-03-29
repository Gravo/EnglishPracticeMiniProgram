@echo off
chcp 65001 >nul
cd /d "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad"

set FFMPEG=D:\tools\ffmpeg\bin\ffmpeg.exe
set SOURCE=E:\moive\Breaking Bad 01
set OUTPUT=clips

echo [2/7] Extracting 02_asking_directions.mp3...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 120 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\02_asking_directions.mp3"
if %errorlevel%==0 (echo   SUCCESS) else (echo   FAILED)

echo [3/7] Extracting 03_restaurant.mp3...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 300 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\03_restaurant.mp3"
if %errorlevel%==0 (echo   SUCCESS) else (echo   FAILED)

echo [4/7] Extracting 04_hospital.mp3...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 180 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\04_hospital.mp3"
if %errorlevel%==0 (echo   SUCCESS) else (echo   FAILED)

echo [5/7] Extracting 05_family.mp3...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 240 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\05_family.mp3"
if %errorlevel%==0 (echo   SUCCESS) else (echo   FAILED)

echo [6/7] Extracting 06_negotiation.mp3...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv" -ss 360 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\06_negotiation.mp3"
if %errorlevel%==0 (echo   SUCCESS) else (echo   FAILED)

echo [7/7] Extracting 07_complex_dialogue.mp3...
"%FFMPEG%" -i "%SOURCE%\Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv" -ss 420 -t 600 -vn -ar 44100 -b:a 64k -ac 1 -y "%OUTPUT%\07_complex_dialogue.mp3"
if %errorlevel%==0 (echo   SUCCESS) else (echo   FAILED)

echo.
echo Done! Check clips folder.
pause
