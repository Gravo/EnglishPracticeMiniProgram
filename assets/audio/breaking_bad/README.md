# Breaking Bad 音频素材

## 目录说明

本目录包含 Breaking Bad 第一季的音频学习素材，共7个关卡。

## 音频文件

将提取的音频文件放到 `clips\` 目录：

```
clips/
├── 01_greeting.mp3           (打招呼 - 入门)
├── 02_asking_directions.mp3   (问路 - 入门)
├── 03_restaurant.mp3          (餐厅 - 初级)
├── 04_hospital.mp3           (医院 - 中级)
├── 05_family.mp3             (家庭 - 中级)
├── 06_negotiation.mp3         (谈判 - 高级)
└── 07_complex_dialogue.mp3   (复杂对话 - 精通)
```

## 提取命令

如果需要重新提取音频，运行以下命令：

```cmd
mkdir D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips

"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e01 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\01_greeting.mp3"

"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e02 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\02_asking_directions.mp3"

"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e03 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\03_restaurant.mp3"

"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e04 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\04_hospital.mp3"

"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e05 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\05_family.mp3"

"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e06 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\06_negotiation.mp3"

"D:\tools\ffmpeg\bin\ffmpeg.exe" -i "E:\moive\Breaking Bad 01\Breaking Bad s01e07 720p.BRrip.Sujaidr.mkv" -ss 0 -t 600 -vn -ar 44100 -b:a 128k -y "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips\07_complex_dialogue.mp3"
```

## 字幕文件

字幕文件放到 `transcripts\` 目录：

```
transcripts/
├── 01_greeting.txt           (从 .srt 复制)
├── 02_asking_directions.txt
├── 03_restaurant.txt
├── 04_hospital.txt
├── 05_family.txt
├── 06_negotiation.txt
└── 07_complex_dialogue.txt
```

复制字幕命令：
```cmd
copy "E:\moive\Breaking Bad 01\Breaking Bad s01e01 720p.BRrip.Sujaidr.srt" "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\01_greeting.txt"
copy "E:\moive\Breaking Bad 01\Breaking Bad s01e02 720p.BRrip.Sujaidr.srt" "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\02_asking_directions.txt"
copy "E:\moive\Breaking Bad 01\Breaking Bad s01e03 720p.BRrip.Sujaidr.srt" "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\03_restaurant.txt"
copy "E:\moive\Breaking Bad 01\Breaking Bad s01e04 720p.BRrip.Sujaidr.srt" "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\04_hospital.txt"
copy "E:\moive\Breaking Bad 01\Breaking Bad s01e05 720p.BRrip.Sujaidr.srt" "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\05_family.txt"
copy "E:\moive\Breaking Bad 01\Breaking Bad s01e06 720p.BRrip.Sujaidr.srt" "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\06_negotiation.txt"
copy "E:\moive\Breaking Bad 01\Breaking Bad s01e07 720p.BRrip.Sujaidr.srt" "D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\transcripts\07_complex_dialogue.txt"
```
