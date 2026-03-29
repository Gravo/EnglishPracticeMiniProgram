@echo off
"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 163 -t 32 -vn -ar 44100 -b:a 64k -ac 1 -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\03_restaurant.mp3"
pause
