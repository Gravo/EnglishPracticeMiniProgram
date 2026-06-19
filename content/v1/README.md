# MVP Content Pack v1

此目录模拟未来部署到域名或虚拟主机上的静态内容结构。

入口文件：

- `manifest.json`

内容文件：

- `wordpacks/gaokao_mvp_words_001.json`
- `cardpacks/gaokao_mvp_cards_001.json`

当前版本：

- 10 个高考核心词
- 每词 7 个不同语境
- 共 70 张卡
- 音频暂未生成，`audioUrl` 为空

未来部署到域名后，小程序可通过以下形式访问：

```text
https://your-domain.com/content/v1/manifest.json
https://your-domain.com/content/v1/wordpacks/gaokao_mvp_words_001.json
https://your-domain.com/content/v1/cardpacks/gaokao_mvp_cards_001.json
```

生成命令：

```bash
python tools/build_mvp_content_pack.py
```

