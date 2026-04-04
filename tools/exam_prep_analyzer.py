#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Breaking Bad S01 备考词汇筛选系统 v3.0
=====================================
目标：为英语学习者筛选最有价值的学习片段

筛选标准：
1. 高中词汇优先（高考/CET-4核心）
2. 高频场景词（日常、学术、职场）
3. 实用句型（可复用表达）
4. 适中难度（适合听写练习）

输出：
- 精选片段列表（含时间戳）
- 词汇-片段映射
- 学习脚本
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re
import os
import json
from collections import Counter, defaultdict

# ─────────────────────────────────────────────
# 高考/CET-4 核心词汇表（按重要性分级）
# ─────────────────────────────────────────────

# 一级核心词：高考必考，出现频率最高
TIER1_VOCAB = set("""
know think say tell talk speak hear listen see look watch
come go get take give make put bring send let want need
have has had do does did will would can could may might must
should shall am is are was were be been being
time year day week month way thing man woman child people person
work job money business home house family school class student teacher
good bad great new old big small long short high low right wrong
ask answer help start end begin finish open close
question problem idea fact reason result example
believe hope feel love like want try use
word sentence language English Chinese
read write learn study teach understand know
morning afternoon evening night today tomorrow yesterday
hand head face eye ear mouth nose arm leg foot body
food water tea coffee breakfast lunch dinner
car bus train plane bike road street
friend brother sister father mother son daughter
one two three four five six seven eight nine ten
first second third next last
here there where when why how what which who
""".split())

# 二级重要词：高频场景词
TIER2_VOCAB = set("""
actually probably really certainly maybe perhaps
something anything nothing everything someone anyone
always usually often sometimes never ever already yet still just
again before after while during since until because although
through without against between among around across along
different important difficult possible necessary
experience understand remember forget believe
change become continue remain leave arrive return
receive accept refuse agree disagree
decision choice chance opportunity
attention care concern interest
success failure effort purpose
example case situation condition
message information news notice
price cost value money cash
health disease doctor hospital medicine
legal illegal law police crime
danger safe risk trouble problem
happy sad angry worried excited surprised
sure clear free ready available
public private personal general common
develop improve increase reduce grow rise fall
""".split())

# 三级扩展词：学术/专业场景
TIER3_VOCAB = set("""
chemistry chemical reaction element compound
science scientific scientist experiment laboratory
analysis method process system structure
theory principle concept definition explanation
evidence proof argument debate discussion
education educational college university degree
professional career position salary income
political economic social cultural historical
environment environmental nature natural
technology technological computer internet
international national local regional
production product market industry trade
management manager director department
responsibility responsible quality standard
performance achievement goal target
communication communicate express impression
""".split())

# ─────────────────────────────────────────────
# 实用句型模式（可复用表达）
# ─────────────────────────────────────────────
USEFUL_PATTERNS = [
    # 打招呼/告别
    (r"\b(hey|hi|hello|goodbye|bye|see you)\b", "打招呼"),
    (r"\b(how are you|how's it going|what's up)\b", "问候"),
    # 表达观点
    (r"\b(i think|i believe|i guess|i suppose)\b", "表达观点"),
    (r"\b(you know|i mean|i see)\b", "口语填充"),
    # 请求/建议
    (r"\b(can you|could you|would you|will you)\b", "请求"),
    (r"\b(why don't|let's|we should|you should)\b", "建议"),
    # 同意/不同意
    (r"\b(i agree|that's right|exactly|absolutely)\b", "同意"),
    (r"\b(i don't think|i disagree|not really)\b", "不同意"),
    # 情感表达
    (r"\b(i'm sorry|i apologize|excuse me)\b", "道歉"),
    (r"\b(thank you|thanks|i appreciate)\b", "感谢"),
    (r"\b(i'm happy|i'm glad|i'm worried)\b", "情感"),
    # 时间表达
    (r"\b(right now|at the moment|currently)\b", "现在"),
    (r"\b(in the future|someday|eventually)\b", "未来"),
    (r"\b(in the past|before|previously)\b", "过去"),
    # 程度/频率
    (r"\b(very|really|quite|pretty|fairly)\b", "程度"),
    (r"\b(always|usually|often|sometimes|never)\b", "频率"),
]

# 停用词
STOP_WORDS = set("""
a an the is are was were be been being am
i me my myself we our ours ourselves you your yours yourself yourselves
he him his himself she her hers herself it its itself they them their theirs themselves
what which who whom this that these those
do does did doing have has had having will would shall should may might must can could
not no nor so yet both either neither once here there when where why how all each every
few more most other some such than too very just because if while although though
oh ah uh um er hmm hm mm yeah yep nope hey hi bye ok okay
s t d ll re ve m n
""".split())

def parse_srt_with_timestamps(filepath):
    """解析SRT字幕，保留时间戳"""
    subtitles = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return subtitles

    blocks = re.split(r'\n\n+', content.strip())
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
            
        # 解析时间戳
        time_line = None
        text_lines = []
        index = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r'^\d+$', line):
                index = int(line)
                continue
            if re.match(r'^\d{2}:\d{2}:\d{2}', line):
                time_line = line
                continue
            # 清理HTML标签
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                text_lines.append(line)
        
        if time_line and text_lines:
            # 解析开始和结束时间
            times = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3})', time_line)
            if len(times) >= 2:
                start_time = times[0]
                end_time = times[1]
                subtitles.append({
                    'index': index,
                    'start': start_time,
                    'end': end_time,
                    'text': ' '.join(text_lines),
                    'text_lines': text_lines
                })
    
    return subtitles

def extract_words(text):
    """提取单词"""
    text = text.lower()
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"'re", " are", text)
    text = re.sub(r"'ve", " have", text)
    text = re.sub(r"'ll", " will", text)
    text = re.sub(r"'d", " would", text)
    text = re.sub(r"'m", " am", text)
    tokens = re.findall(r"[a-z]+", text)
    return [w for w in tokens if len(w) >= 2 and w not in STOP_WORDS]

def calculate_subtitle_score(subtitle, vocab_counter):
    """计算字幕片段的学习价值分数"""
    text = subtitle['text'].lower()
    words = extract_words(text)
    
    score = 0
    tier1_count = 0
    tier2_count = 0
    tier3_count = 0
    
    for word in words:
        if word in TIER1_VOCAB:
            score += 10
            tier1_count += 1
        elif word in TIER2_VOCAB:
            score += 5
            tier2_count += 1
        elif word in TIER3_VOCAB:
            score += 3
            tier3_count += 1
        else:
            # 出现在剧中的高频词也加分
            freq = vocab_counter.get(word, 0)
            if freq >= 20:
                score += 4
            elif freq >= 10:
                score += 2
            elif freq >= 5:
                score += 1
    
    # 句型加分
    pattern_bonus = 0
    matched_patterns = []
    for pattern, pattern_name in USEFUL_PATTERNS:
        if re.search(pattern, text):
            pattern_bonus += 5
            matched_patterns.append(pattern_name)
    
    # 长度适中加分（适合听写）
    word_count = len(words)
    if 5 <= word_count <= 15:
        score += 5  # 理想长度
    elif 3 <= word_count <= 20:
        score += 2  # 可接受长度
    
    return {
        'score': score + pattern_bonus,
        'tier1_count': tier1_count,
        'tier2_count': tier2_count,
        'tier3_count': tier3_count,
        'patterns': matched_patterns,
        'word_count': word_count,
        'words': words
    }

def format_time_to_seconds(time_str):
    """将 SRT 时间格式转换为秒"""
    match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', time_str)
    if match:
        h, m, s, ms = map(int, match.groups())
        return h * 3600 + m * 60 + s + ms / 1000
    return 0

def format_seconds_to_time(seconds):
    """将秒转换为 mm:ss 格式"""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def analyze_for_exam_prep(srt_dir):
    """备考导向分析"""
    all_subtitles = []
    all_words = []
    episode_subtitles = {}
    
    srt_files = sorted([f for f in os.listdir(srt_dir) if f.endswith('.srt')])
    
    print("\n" + "="*70)
    print("  📚 Breaking Bad S01 - 备考词汇筛选系统")
    print("="*70)
    print(f"\n  分析目标：筛选最有备考价值的字幕片段\n")
    
    for fname in srt_files:
        fpath = os.path.join(srt_dir, fname)
        subtitles = parse_srt_with_timestamps(fpath)
        
        ep_match = re.search(r's01e0?(\d+)', fname.lower())
        ep_num = int(ep_match.group(1)) if ep_match else 0
        
        for sub in subtitles:
            words = extract_words(sub['text'])
            all_words.extend(words)
            sub['episode'] = ep_num
            sub['words'] = words
        
        all_subtitles.extend(subtitles)
        episode_subtitles[ep_num] = subtitles
        
        print(f"  ✅ E{ep_num:02d}: {len(subtitles)} 条字幕")
    
    print("\n" + "-"*70)
    
    # 计算全局词频
    vocab_counter = Counter(all_words)
    
    return all_subtitles, vocab_counter, episode_subtitles

def generate_exam_prep_report(all_subtitles, vocab_counter, episode_subtitles, output_dir):
    """生成备考报告"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 为每条字幕评分
    scored_subtitles = []
    for sub in all_subtitles:
        score_info = calculate_subtitle_score(sub, vocab_counter)
        sub.update(score_info)
        scored_subtitles.append(sub)
    
    # 按分数排序
    scored_subtitles.sort(key=lambda x: -x['score'])
    
    # ── 输出1：精选片段清单 ─────────────────────
    clips_file = os.path.join(output_dir, 'EXAM_CLIPS.txt')
    with open(clips_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 备考精选片段清单\n")
        f.write("="*70 + "\n\n")
        f.write("筛选标准：\n")
        f.write("  1. 包含高考/CET-4核心词汇\n")
        f.write("  2. 句型实用、可复用\n")
        f.write("  3. 长度适中（5-15词），适合听写\n")
        f.write("  4. 难度适中，语速清晰\n\n")
        f.write("共筛选出 " + str(len([s for s in scored_subtitles if s['score'] >= 15])) + " 条高价值片段\n\n")
        
        # 按集数分组
        for ep in sorted(set(s['episode'] for s in scored_subtitles)):
            ep_subs = [s for s in scored_subtitles if s['episode'] == ep and s['score'] >= 15]
            if not ep_subs:
                continue
            
            f.write(f"\n{'='*70}\n")
            f.write(f"  Episode {ep:02d} - 精选片段 ({len(ep_subs)}条)\n")
            f.write(f"{'='*70}\n\n")
            
            for i, sub in enumerate(ep_subs[:30], 1):  # 每集最多30条
                start_sec = format_time_to_seconds(sub['start'])
                end_sec = format_time_to_seconds(sub['end'])
                duration = end_sec - start_sec
                
                f.write(f"  [{i:02d}] {sub['start']} → {sub['end']} ({duration:.1f}s)\n")
                f.write(f"      {sub['text']}\n")
                f.write(f"      分数: {sub['score']} | 核心词: {sub['tier1_count']} | 句型: {', '.join(sub['patterns']) or '-'}\n\n")
    
    print(f"\n  ✅ 精选片段 → {clips_file}")
    
    # ── 输出2：词汇-片段索引 ─────────────────────
    vocab_index_file = os.path.join(output_dir, 'VOCAB_CLIP_INDEX.txt')
    
    # 建立词汇到片段的映射
    vocab_to_clips = defaultdict(list)
    for sub in scored_subtitles:
        if sub['score'] >= 15:
            for word in set(sub['words']):
                if word in TIER1_VOCAB or word in TIER2_VOCAB:
                    vocab_to_clips[word].append(sub)
    
    with open(vocab_index_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 词汇-片段索引\n")
        f.write("="*70 + "\n\n")
        f.write("说明：每个核心词汇对应的最佳学习片段\n\n")
        
        # 按词汇重要性排序
        for vocab in sorted(TIER1_VOCAB):
            if vocab in vocab_to_clips:
                clips = sorted(vocab_to_clips[vocab], key=lambda x: -x['score'])[:3]
                f.write(f"\n  {vocab.upper()}\n")
                f.write(f"  {'-'*40}\n")
                for clip in clips:
                    f.write(f"  E{clip['episode']:02d} {clip['start']} | {clip['text'][:50]}...\n")
        
        f.write(f"\n\n  {'='*70}\n")
        f.write(f"  二级重要词汇\n")
        f.write(f"  {'='*70}\n")
        
        for vocab in sorted(TIER2_VOCAB):
            if vocab in vocab_to_clips:
                clips = sorted(vocab_to_clips[vocab], key=lambda x: -x['score'])[:2]
                f.write(f"\n  {vocab.upper()}\n")
                for clip in clips:
                    f.write(f"    E{clip['episode']:02d} {clip['start']} | {clip['text'][:45]}...\n")
    
    print(f"  ✅ 词汇索引 → {vocab_index_file}")
    
    # ── 输出3：听写练习脚本 ─────────────────────
    script_file = os.path.join(output_dir, 'DICTATION_SCRIPT.txt')
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 听写练习脚本\n")
        f.write("="*70 + "\n\n")
        f.write("使用方法：\n")
        f.write("  1. 播放对应时间段的视频\n")
        f.write("  2. 听写字幕内容\n")
        f.write("  3. 对照原文检查\n")
        f.write("  4. 重点学习核心词汇和句型\n\n")
        
        for ep in sorted(set(s['episode'] for s in scored_subtitles)):
            ep_subs = [s for s in scored_subtitles if s['episode'] == ep and s['score'] >= 20]
            if not ep_subs:
                continue
            
            f.write(f"\n{'='*70}\n")
            f.write(f"  Episode {ep:02d}\n")
            f.write(f"{'='*70}\n\n")
            
            for i, sub in enumerate(ep_subs[:15], 1):
                f.write(f"  练习 {i:02d}\n")
                f.write(f"  时间: {sub['start']} - {sub['end']}\n")
                f.write(f"  核心词: {', '.join([w for w in sub['words'] if w in TIER1_VOCAB][:5])}\n")
                f.write(f"  {'─'*50}\n")
                f.write(f"  [原文]\n")
                f.write(f"  {sub['text']}\n")
                f.write(f"\n")
                f.write(f"  [你的听写]\n")
                f.write(f"  _{'_'*50}\n")
                f.write(f"  _{'_'*50}\n")
                f.write(f"\n\n")
    
    print(f"  ✅ 听写脚本 → {script_file}")
    
    # ── 输出4：音频截取清单 ─────────────────────
    audio_list_file = os.path.join(output_dir, 'AUDIO_EXTRACTION_LIST.txt')
    with open(audio_list_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 音频截取清单\n")
        f.write("="*70 + "\n\n")
        f.write("FFmpeg 命令格式：\n")
        f.write("  ffmpeg -i input.mkv -ss START -t DURATION -c:a libmp3lame -b:a 64k output.mp3\n\n")
        
        for ep in sorted(set(s['episode'] for s in scored_subtitles)):
            ep_subs = [s for s in scored_subtitles if s['episode'] == ep and s['score'] >= 20]
            if not ep_subs:
                continue
            
            f.write(f"\n{'='*70}\n")
            f.write(f"  Episode {ep:02d}\n")
            f.write(f"{'='*70}\n\n")
            
            for i, sub in enumerate(ep_subs[:20], 1):
                start_sec = format_time_to_seconds(sub['start'])
                end_sec = format_time_to_seconds(sub['end'])
                duration = end_sec - start_sec
                
                # FFmpeg 命令
                output_name = f"ep{ep:02d}_clip{i:02d}.mp3"
                f.write(f"  # Clip {i:02d}: {sub['text'][:40]}...\n")
                f.write(f"  ffmpeg -i \"Breaking.Bad.S01E{ep:02d}.mkv\" ")
                f.write(f"-ss {sub['start'].replace(',', '.')} -t {duration:.1f} ")
                f.write(f"-c:a libmp3lame -b:a 64k \"{output_name}\"\n\n")
    
    print(f"  ✅ 截取清单 → {audio_list_file}")
    
    # ── 输出5：JSON数据 ─────────────────────
    json_file = os.path.join(output_dir, 'EXAM_PREP_DATA.json')
    json_data = {
        "meta": {
            "total_subtitles": len(all_subtitles),
            "high_value_clips": len([s for s in scored_subtitles if s['score'] >= 15]),
            "tier1_vocab_count": len(TIER1_VOCAB),
            "tier2_vocab_count": len(TIER2_VOCAB)
        },
        "top_clips": [
            {
                "episode": s['episode'],
                "start": s['start'],
                "end": s['end'],
                "text": s['text'],
                "score": s['score'],
                "tier1_words": [w for w in s['words'] if w in TIER1_VOCAB],
                "patterns": s['patterns']
            }
            for s in scored_subtitles[:100]
        ],
        "clips_by_episode": {
            str(ep): [
                {
                    "start": s['start'],
                    "end": s['end'],
                    "text": s['text'],
                    "score": s['score']
                }
                for s in sorted(
                    [sub for sub in scored_subtitles if sub['episode'] == ep and sub['score'] >= 15],
                    key=lambda x: -x['score']
                )[:30]
            ]
            for ep in sorted(set(s['episode'] for s in scored_subtitles))
        }
    }
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON数据 → {json_file}")
    
    # ── 控制台统计 ─────────────────────────────
    print("\n" + "="*70)
    print("  📊 筛选统计")
    print("="*70)
    print(f"  总字幕数:       {len(all_subtitles):,}")
    print(f"  高价值片段:     {len([s for s in scored_subtitles if s['score'] >= 15]):,}")
    print(f"  核心片段:       {len([s for s in scored_subtitles if s['score'] >= 20]):,}")
    print(f"  精华片段:       {len([s for s in scored_subtitles if s['score'] >= 30]):,}")
    
    # 按集数统计
    print(f"\n  各集高价值片段分布:")
    for ep in sorted(set(s['episode'] for s in scored_subtitles)):
        count = len([s for s in scored_subtitles if s['episode'] == ep and s['score'] >= 15])
        bar = "█" * (count // 2) + "░" * (20 - count // 2)
        print(f"    E{ep:02d} | {count:>3}条 | {bar}")
    
    # Top 10 精华片段
    print("\n" + "="*70)
    print("  🏆 Top 10 精华片段")
    print("="*70)
    for i, sub in enumerate(scored_subtitles[:10], 1):
        print(f"\n  {i:2d}. E{sub['episode']:02d} | 分数: {sub['score']} | {sub['start']}")
        print(f"      {sub['text']}")
        print(f"      核心词: {', '.join([w for w in sub['words'] if w in TIER1_VOCAB][:5])}")
        if sub['patterns']:
            print(f"      句型: {', '.join(sub['patterns'])}")
    
    print("\n" + "="*70)
    print(f"  ✅ 所有报告已保存: {output_dir}")
    print("="*70 + "\n")
    
    return json_data

if __name__ == '__main__':
    SRT_DIR = r"E:\moive\Breaking Bad 01"
    OUTPUT_DIR = r"D:\EnglishPracticeMiniProgram\docs\exam_prep"
    
    all_subtitles, vocab_counter, episode_subtitles = analyze_for_exam_prep(SRT_DIR)
    generate_exam_prep_report(all_subtitles, vocab_counter, episode_subtitles, OUTPUT_DIR)
