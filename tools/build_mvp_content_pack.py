#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the first MVP content pack.

The MVP rule is: one target word must appear in seven different learning
contexts before we count it as "ready for mastery tracking".
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "v1"


WORDS = [
    {
        "word": "approach",
        "phonetic": "əˈprəʊtʃ",
        "definitionCn": "方法；接近；处理",
        "priority": "A",
        "cards": [
            ("meaning", "A calm approach can make a hard problem easier.", "冷静的方法可以让难题变得更容易。", "definition"),
            ("campus", "Our teacher showed us a new approach to reading long passages.", "老师向我们展示了一种阅读长篇文章的新方法。", "school"),
            ("family", "My father uses a patient approach when he helps me with homework.", "爸爸辅导我作业时会用一种耐心的方法。", "home"),
            ("science", "Scientists need a careful approach before they test a new idea.", "科学家在测试新想法前需要谨慎的方法。", "science"),
            ("dialogue", "Maybe we should try a different approach.", "也许我们应该试试不同的方法。", "dialogue"),
            ("cloze", "We need a better ___ to solve this problem.", "我们需要一个更好的方法来解决这个问题。", "cloze"),
            ("transfer", "When one approach fails, good learners try another.", "当一种方法失败时，优秀的学习者会尝试另一种。", "review"),
        ],
    },
    {
        "word": "benefit",
        "phonetic": "ˈbenɪfɪt",
        "definitionCn": "好处；受益",
        "priority": "A",
        "cards": [
            ("meaning", "Daily reading brings a clear benefit to language learners.", "每日阅读给语言学习者带来明显好处。", "definition"),
            ("campus", "The main benefit of joining the club is more speaking practice.", "加入社团的主要好处是有更多口语练习。", "school"),
            ("family", "My parents believe exercise will benefit both my body and mind.", "父母相信锻炼会让我的身心都受益。", "home"),
            ("news", "The new library will benefit students in the whole town.", "新图书馆会让全镇学生受益。", "news"),
            ("dialogue", "What benefit can we get from this plan?", "我们能从这个计划中得到什么好处？", "dialogue"),
            ("cloze", "Sleep is not a waste of time; it can ___ your memory.", "睡眠不是浪费时间；它能让你的记忆受益。", "cloze"),
            ("transfer", "A small habit can bring a long-term benefit.", "一个小习惯可以带来长期好处。", "review"),
        ],
    },
    {
        "word": "affect",
        "phonetic": "əˈfekt",
        "definitionCn": "影响",
        "priority": "A",
        "cards": [
            ("meaning", "Weather can affect our mood and our plans.", "天气会影响我们的心情和计划。", "definition"),
            ("campus", "Too much screen time may affect a student's sleep.", "过多看屏幕可能影响学生睡眠。", "school"),
            ("family", "One kind word can affect the feeling of the whole family.", "一句友善的话能影响整个家庭的气氛。", "home"),
            ("science", "Light and water affect how fast a plant grows.", "光和水会影响植物生长的速度。", "science"),
            ("dialogue", "Will this mistake affect my final grade?", "这个错误会影响我的最终成绩吗？", "dialogue"),
            ("cloze", "Noise can ___ how well we understand a recording.", "噪音会影响我们理解录音的效果。", "cloze"),
            ("transfer", "Good choices today affect who we become tomorrow.", "今天好的选择会影响明天的我们。", "review"),
        ],
    },
    {
        "word": "admit",
        "phonetic": "ədˈmɪt",
        "definitionCn": "承认；准许进入",
        "priority": "A",
        "cards": [
            ("meaning", "It is brave to admit a mistake and correct it.", "承认错误并改正是勇敢的。", "definition"),
            ("campus", "The student admitted that he had forgotten the homework.", "这个学生承认自己忘了作业。", "school"),
            ("family", "My brother finally admitted he had eaten the last piece of cake.", "弟弟终于承认他吃了最后一块蛋糕。", "home"),
            ("news", "The museum will admit students for free on Friday.", "博物馆周五将允许学生免费进入。", "news"),
            ("dialogue", "I have to admit that your idea is better.", "我得承认你的想法更好。", "dialogue"),
            ("cloze", "She did not want to ___ that she was nervous.", "她不想承认自己很紧张。", "cloze"),
            ("transfer", "People trust you more when you admit the truth.", "当你承认真相时，人们会更信任你。", "review"),
        ],
    },
    {
        "word": "consider",
        "phonetic": "kənˈsɪdə",
        "definitionCn": "考虑；认为",
        "priority": "A",
        "cards": [
            ("meaning", "Please consider all the facts before you decide.", "做决定前请考虑所有事实。", "definition"),
            ("campus", "I will consider joining the English reading group.", "我会考虑加入英语阅读小组。", "school"),
            ("family", "We should consider grandma's feelings before changing the plan.", "改变计划前我们应该考虑奶奶的感受。", "home"),
            ("news", "The city will consider building more bike lanes.", "这座城市将考虑建设更多自行车道。", "news"),
            ("dialogue", "Would you consider studying abroad in the future?", "你将来会考虑出国学习吗？", "dialogue"),
            ("cloze", "A good writer must ___ the reader's point of view.", "好作者必须考虑读者的视角。", "cloze"),
            ("transfer", "To consider is to slow down before choosing.", "考虑，就是在选择之前慢下来。", "review"),
        ],
    },
    {
        "word": "develop",
        "phonetic": "dɪˈveləp",
        "definitionCn": "发展；培养；开发",
        "priority": "A",
        "cards": [
            ("meaning", "You can develop confidence through practice.", "你可以通过练习培养自信。", "definition"),
            ("campus", "Reading every day helps students develop a better vocabulary.", "每天阅读帮助学生发展更好的词汇量。", "school"),
            ("family", "Children develop good habits when adults set clear examples.", "成年人树立明确榜样时，孩子会养成好习惯。", "home"),
            ("science", "Engineers develop new tools to solve real problems.", "工程师开发新工具来解决实际问题。", "science"),
            ("dialogue", "How can I develop my listening skills?", "我怎样才能提高听力能力？", "dialogue"),
            ("cloze", "The team wants to ___ a simple app for learners.", "团队想为学习者开发一个简单应用。", "cloze"),
            ("transfer", "Skills develop slowly, then suddenly feel natural.", "技能是慢慢发展的，然后突然变得自然。", "review"),
        ],
    },
    {
        "word": "improve",
        "phonetic": "ɪmˈpruːv",
        "definitionCn": "提高；改善",
        "priority": "A",
        "cards": [
            ("meaning", "Small daily actions can improve your English.", "每天的小行动可以提高你的英语。", "definition"),
            ("campus", "The class used short videos to improve listening.", "这个班用短视频提高听力。", "school"),
            ("family", "We improved our dinner by adding fresh vegetables.", "我们加了新鲜蔬菜，让晚餐更好了。", "home"),
            ("news", "The school plans to improve the reading room.", "学校计划改善阅览室。", "news"),
            ("dialogue", "What can I do to improve my pronunciation?", "我能做什么来提高发音？", "dialogue"),
            ("cloze", "Reviewing mistakes can ___ your test score.", "复盘错误可以提高你的考试分数。", "cloze"),
            ("transfer", "To improve, notice one small thing and fix it.", "想要进步，就发现一个小问题并修正它。", "review"),
        ],
    },
    {
        "word": "support",
        "phonetic": "səˈpɔːt",
        "definitionCn": "支持；支撑",
        "priority": "A",
        "cards": [
            ("meaning", "A good friend will support you when you feel unsure.", "好朋友会在你不确定时支持你。", "definition"),
            ("campus", "The school will support students who want to start a club.", "学校会支持想创办社团的学生。", "school"),
            ("family", "My family support my dream of becoming a teacher.", "家人支持我成为老师的梦想。", "home"),
            ("science", "Strong roots support the tree during a storm.", "强壮的根在暴风雨中支撑树木。", "science"),
            ("dialogue", "Thank you for your support during the exam week.", "谢谢你在考试周给我的支持。", "dialogue"),
            ("cloze", "Facts can ___ your opinion in an essay.", "事实可以支持你在作文中的观点。", "cloze"),
            ("transfer", "Support can be emotional, practical, or logical.", "支持可以是情感上的、实际上的或逻辑上的。", "review"),
        ],
    },
    {
        "word": "challenge",
        "phonetic": "ˈtʃælɪndʒ",
        "definitionCn": "挑战；质疑",
        "priority": "A",
        "cards": [
            ("meaning", "A challenge is difficult, but it can make you stronger.", "挑战很难，但它能让你更强。", "definition"),
            ("campus", "The speech contest was a real challenge for me.", "演讲比赛对我来说是真正的挑战。", "school"),
            ("family", "Cooking dinner alone was my weekend challenge.", "独自做晚饭是我周末的挑战。", "home"),
            ("news", "Climate change is a challenge for every country.", "气候变化是每个国家面临的挑战。", "news"),
            ("dialogue", "Are you ready for the next challenge?", "你准备好迎接下一个挑战了吗？", "dialogue"),
            ("cloze", "Learning to listen without subtitles is a useful ___.", "学习不看字幕听英语是一个有用的挑战。", "cloze"),
            ("transfer", "The right challenge should be hard but possible.", "合适的挑战应该困难但可完成。", "review"),
        ],
    },
    {
        "word": "experience",
        "phonetic": "ɪkˈspɪəriəns",
        "definitionCn": "经历；经验；体验",
        "priority": "A",
        "cards": [
            ("meaning", "Experience teaches lessons that books cannot fully explain.", "经验会教会我们书本无法完全解释的东西。", "definition"),
            ("campus", "The science fair gave me my first experience of public speaking.", "科学展给了我第一次公开演讲的经历。", "school"),
            ("family", "Traveling with my family was a wonderful experience.", "和家人旅行是一次美好的经历。", "home"),
            ("news", "Volunteers with medical experience arrived after the storm.", "有医疗经验的志愿者在暴风雨后赶到。", "news"),
            ("dialogue", "Do you have any experience with this kind of work?", "你有这类工作的经验吗？", "dialogue"),
            ("cloze", "Reading stories gives learners a rich language ___.", "阅读故事给学习者丰富的语言体验。", "cloze"),
            ("transfer", "Each experience becomes useful when you reflect on it.", "每段经历在你反思之后都会变得有用。", "review"),
        ],
    },
]


def card_id(word: str, index: int) -> str:
    return f"mvp_{word}_{index:02d}"


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "wordpacks").mkdir(exist_ok=True)
    (OUT / "cardpacks").mkdir(exist_ok=True)

    words = []
    cards = []
    now = datetime.now(timezone.utc).isoformat()

    for word_index, item in enumerate(WORDS, 1):
        word = item["word"]
        word_cards = []
        for index, (card_type, sentence, translation, scenario) in enumerate(item["cards"], 1):
            cid = card_id(word, index)
            word_cards.append(cid)
            cards.append({
                "cardId": cid,
                "word": word,
                "exposureIndex": index,
                "cardType": card_type,
                "scenario": scenario,
                "sentence": sentence,
                "translation": translation,
                "target": word,
                "audioText": sentence,
                "audioUrl": "",
                "sourceType": "mvp_curated_original",
                "sourceNote": "Original MVP sentence for Gaokao listening and reading practice.",
                "difficulty": "gaokao_basic",
                "estimatedSeconds": 8,
            })

        words.append({
            "wordId": f"gk_{word}",
            "word": word,
            "rank": word_index,
            "phonetic": item["phonetic"],
            "definitionCn": item["definitionCn"],
            "priority": item["priority"],
            "masteryRule": {
                "requiredDistinctExposures": 7,
                "requiredActiveRecall": 2,
                "minimumDays": 3,
            },
            "cardIds": word_cards,
        })

    wordpack = {
        "packId": "gaokao_mvp_words_001",
        "version": "2026.06.19-mvp1",
        "createdAt": now,
        "description": "First 10 Gaokao MVP words, each with seven distinct exposure cards.",
        "words": words,
    }
    cardpack = {
        "packId": "gaokao_mvp_cards_001",
        "version": "2026.06.19-mvp1",
        "createdAt": now,
        "exposurePolicy": {
            "distinctExposuresPerWord": 7,
            "cardTypes": ["meaning", "campus", "family", "news/science", "dialogue", "cloze", "transfer"],
            "masteryNote": "A word is not considered mastered until the learner has seen it in seven contexts and completed at least two active recall cards.",
        },
        "cards": cards,
    }
    manifest = {
        "contentVersion": "2026.06.19-mvp1",
        "createdAt": now,
        "miniprogramMinVersion": "0.1.0",
        "baseUrl": "",
        "wordpacks": [{
            "packId": wordpack["packId"],
            "path": "wordpacks/gaokao_mvp_words_001.json",
            "wordCount": len(words),
        }],
        "cardpacks": [{
            "packId": cardpack["packId"],
            "path": "cardpacks/gaokao_mvp_cards_001.json",
            "cardCount": len(cards),
        }],
        "audio": {
            "mode": "tts_pending",
            "note": "audioUrl is empty in MVP1. Generate MP3 files in the next TTS batch and update card audioUrl fields.",
        },
    }

    (OUT / "wordpacks" / "gaokao_mvp_words_001.json").write_text(
        json.dumps(wordpack, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT / "cardpacks" / "gaokao_mvp_cards_001.json").write_text(
        json.dumps(cardpack, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT / "mvpContentData.js").write_text(
        "module.exports = "
        + json.dumps({
            "manifest": manifest,
            "wordpack": wordpack,
            "cardpack": cardpack,
        }, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "words": len(words),
        "cards": len(cards),
        "out": str(OUT),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
