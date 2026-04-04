#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Breaking Bad S01 完整词汇分析工具 v2.0
- 全7集详细统计
- 每集词汇对比
- 场景主题词汇分析
- 学习路线规划
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re
import os
import json
from collections import Counter, defaultdict

# 高中英语核心词汇
HIGH_SCHOOL_VOCAB = set("""
a able about above accept according account across act action activity actually add address
admit affect after again against age ago agree ahead air all allow almost alone along already
also although always among amount and another answer any anyone anything appear apply area
argue around arrive ask at away back bad base be because become before begin behind believe
below best better between big black body book both break bring build but buy by call can
care carry cause change character check child choose city claim clear close come common
community compare complete consider continue control cost could country cover create cut
dark data day dead deal decide deep describe develop different difficult direct discuss do
down draw drive during each early easy effect either else end enough enter even ever every
example exist expect experience explain face fact fall family far feel few field fight fill
find first follow food force form free friend from full future get give go good great group
grow hand happen hard have he head hear heart help here high him his history hold home hope
hour house how human idea if important include increase indeed information instead interest
into issue it its job just keep kind know large last late lead learn leave less let level
life light like likely line list little live long look lose lot love low make man many may
mean meet member might mind miss model money more most move much must name national need
never new next night no not nothing now number of off offer often old on once only open or
order other our out over own part past pay people per place plan play point policy political
possible power present problem produce program provide public put question quite raise reach
read real reason receive recent relate remain report require result return right rise run
same say school seem set several show side since small so social some something sometimes
soon speak stand start state stay still stop story strong student study such support sure
system take talk tell than that the their them then there these they thing think though
through time to today together too top toward turn under until up use very view want war
water way we well what when where which while who why will with within without word work
world would write year yes yet you young your
able abroad absence absolute accept access accident account accurate achieve action active
activity actual add address admire admit adult advance advantage adventure advertise advice
affect afford afraid after afternoon again age agree ahead aim air alarm allow almost alone
along already although always amaze amount ancient anger announce another answer anxious
apart apologize appear apply appreciate approach area argue arrange arrive article ask
assist astonish atmosphere attach attack attempt attend attitude attract audience available
avoid award aware awful balance basic battle beauty become behave believe belong benefit
beside besides between beyond blame bless block board bother brave break breathe bright
bring broad build burn busy calculate calm campaign capable capital capture care career
carry cause celebrate certain challenge chance change character charge chase cheap check
cheerful choice choose citizen claim clear clever climate close collect combine comfort
command common communicate community compare compete complete concentrate concern condition
confident confuse connect consider contain continue control convenient correct cost courage
create crime culture curious current custom damage danger deal decide declare deep defeat
defend delay deliver depend describe design desire destroy develop difference difficult
direct discover discuss distance divide doubt dream drive during duty eager earn education
effect effort either embarrass emotion encourage energy enjoy enough enter environment equal
escape event examine example excellent exchange exercise exist expect experience explain
express extra fail fair familiar famous fantastic far fashion fear feature feel festival
fight figure final find finish fit focus follow force foreign forget formal forward freedom
fresh friendly frighten full function future gain general gentle gift global goal grateful
great grow guard guide habit handle happen happy hard harm hate health heart heavy helpful
honest hope huge human humor hungry hurry ideal ignore imagine important improve include
increase independent influence inform injure innocent inspire instead interest introduce
involve issue jealous join journey judge keep kind knowledge lack language large laugh lead
learn leave legal level limit listen local lonely lose lucky manage manner material mean
measure memory mention method mind mistake modern moment moral move natural necessary
nervous notice object observe offer opinion opportunity organize original overcome own
patient peace perform permit personal plan pleasant polite popular possible practice prefer
prepare present prevent pride problem produce progress promise protect prove provide public
purpose quality question quick quiet realize reason receive recognize reduce refuse relate
relax rely remember remind repeat replace require respect responsible result review reward
risk role safe satisfy save search secret seem select serious share simple situation skill
solve special spend spirit spread standard strength struggle success suggest support
surprise survive system talent task teach technology tend terrible thankful therefore
though threat tidy together tradition treat trust truth typical understand unique unless
until useful value variety various view village violent visit volunteer warn waste wealth
welcome wise wonder worry worth
""".split())

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
s t d ll re ve m
""".split())

# 场景主题关键词
THEMES = {
    "日常对话": ["hey", "morning", "night", "home", "family", "dinner", "breakfast", "sleep", "wake"],
    "学校教育": ["school", "class", "teacher", "student", "chemistry", "learn", "teach", "grade", "exam"],
    "犯罪交易": ["money", "deal", "sell", "buy", "business", "partner", "drug", "meth", "cook", "lab"],
    "家庭关系": ["wife", "husband", "son", "daughter", "brother", "sister", "mother", "father", "family", "love"],
    "医疗健康": ["doctor", "hospital", "cancer", "sick", "treatment", "medicine", "die", "dead", "health", "lung"],
    "法律执法": ["police", "dea", "arrest", "jail", "prison", "lawyer", "legal", "crime", "guilty", "innocent"],
    "情绪表达": ["sorry", "thank", "please", "hell", "damn", "shit", "god", "jesus", "fuck", "crazy"],
}

def parse_srt(filepath):
    """解析SRT字幕"""
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return lines, []

    subtitles = []
    blocks = re.split(r'\n\n+', content.strip())
    
    for block in blocks:
        block_lines = block.strip().split('\n')
        text_lines = []
        timestamp = ""
        
        for line in block_lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r'^\d+$', line):
                continue
            if re.match(r'^\d{2}:\d{2}:\d{2}', line):
                timestamp = line
                continue
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                text_lines.append(line)
        
        if text_lines:
            full_text = ' '.join(text_lines)
            subtitles.append({'text': full_text, 'time': timestamp})
            lines.append(full_text)
    
    return lines, subtitles

def extract_words(text_lines):
    """提取单词"""
    words = []
    for line in text_lines:
        line = line.lower()
        line = re.sub(r"n't", " not", line)
        line = re.sub(r"'re", " are", line)
        line = re.sub(r"'ve", " have", line)
        line = re.sub(r"'ll", " will", line)
        line = re.sub(r"'d", " would", line)
        line = re.sub(r"'m", " am", line)
        tokens = re.findall(r"[a-z]+", line)
        for w in tokens:
            if len(w) >= 2 and w not in STOP_WORDS:
                words.append(w)
    return words

def analyze_full_season(srt_dir):
    """完整季度分析"""
    all_words = []
    all_subtitles = []
    episode_data = {}
    
    srt_files = sorted([f for f in os.listdir(srt_dir) if f.endswith('.srt')])
    
    print("\n" + "="*70)
    print("  📺 Breaking Bad Season 1 - 完整词汇分析")
    print("="*70)
    print(f"\n  📂 目录: {srt_dir}")
    print(f"  🎬 集数: {len(srt_files)} 集\n")
    print("  " + "-"*66)
    
    for fname in srt_files:
        fpath = os.path.join(srt_dir, fname)
        lines, subtitles = parse_srt(fpath)
        words = extract_words(lines)
        all_words.extend(words)
        all_subtitles.extend(subtitles)
        
        ep_match = re.search(r's01e0?(\d+)', fname.lower())
        ep_num = int(ep_match.group(1)) if ep_match else 0
        
        word_counter = Counter(words)
        
        episode_data[ep_num] = {
            'filename': fname,
            'total_words': len(words),
            'unique_words': len(word_counter),
            'subtitles': subtitles,
            'word_list': words,
            'top20': word_counter.most_common(20),
            'hs_words': [(w, c) for w, c in word_counter.most_common() if w in HIGH_SCHOOL_VOCAB][:30],
            'new_words': [],  # 稍后计算
            'avg_sentence_len': sum(len(s['text'].split()) for s in subtitles) / len(subtitles) if subtitles else 0
        }
        
        print(f"  E{ep_num:02d} | {len(words):>5} 词次 | {len(word_counter):>4} 不重复 | 平均句长: {episode_data[ep_num]['avg_sentence_len']:.1f}")
    
    print("  " + "-"*66)
    
    return all_words, episode_data, all_subtitles

def generate_comprehensive_report(all_words, episode_data, all_subtitles, output_dir):
    """生成综合报告"""
    total_counter = Counter(all_words)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # ── 统计概览 ─────────────────────────────
    total_count = len(all_words)
    total_unique = len(total_counter)
    hs_overlap = [(w, c) for w, c in total_counter.most_common() if w in HIGH_SCHOOL_VOCAB]
    
    # 新词分析（每集首次出现的词）
    seen_words = set()
    for ep in sorted(episode_data.keys()):
        ep_words = set(episode_data[ep]['word_list'])
        new_words = ep_words - seen_words
        episode_data[ep]['new_words'] = list(new_words)[:50]
        seen_words.update(ep_words)
    
    # ── 控制台输出 ───────────────────────────
    print("\n" + "="*70)
    print("  📊 统计概览")
    print("="*70)
    print(f"  总词次:          {total_count:,}")
    print(f"  不重复词:        {total_unique:,}")
    print(f"  高中词汇重叠:    {len(hs_overlap)} 词")
    print(f"  平均每集词次:    {total_count // len(episode_data):,}")
    print(f"  总字幕条数:      {len(all_subtitles):,}")
    
    # ── 每集详细对比 ─────────────────────────
    print("\n" + "="*70)
    print("  📈 每集词汇对比")
    print("="*70)
    print(f"\n  {'集':<4} {'总词次':>8} {'不重复':>8} {'新词':>8} {'高中词':>8} {'Top 5'}")
    print("  " + "-"*66)
    
    for ep in sorted(episode_data.keys()):
        data = episode_data[ep]
        hs_count = len([w for w in data['word_list'] if w in HIGH_SCHOOL_VOCAB])
        top5 = ', '.join(w for w, c in data['top20'][:5])
        print(f"  E{ep:02d} {data['total_words']:>8} {data['unique_words']:>8} {len(data['new_words']):>8} {hs_count:>8}  {top5}")
    
    # ── 词汇增长曲线 ─────────────────────────
    print("\n" + "="*70)
    print("  📉 词汇增长分析")
    print("="*70)
    cumulative_words = set()
    growth_data = []
    
    for ep in sorted(episode_data.keys()):
        ep_new = len(episode_data[ep]['new_words'])
        cumulative_words.update(episode_data[ep]['word_list'])
        growth_data.append((ep, len(cumulative_words), ep_new))
        print(f"  E{ep:02d} | 累计词汇: {len(cumulative_words):>5} | 本集新词: {ep_new:>4}")
    
    # ── 场景主题分析 ─────────────────────────
    print("\n" + "="*70)
    print("  🎭 场景主题词汇分布")
    print("="*70)
    
    theme_stats = {}
    for theme, keywords in THEMES.items():
        theme_count = sum(total_counter.get(kw, 0) for kw in keywords)
        theme_stats[theme] = theme_count
    
    for theme, count in sorted(theme_stats.items(), key=lambda x: -x[1]):
        bar = "█" * (count // 10) + "░" * (20 - count // 10)
        print(f"  {theme:<10} | {count:>4}次 | {bar}")
    
    # ── 文件输出 ─────────────────────────────
    
    # 1. 完整词频表
    freq_file = os.path.join(output_dir, 'FULL_FREQUENCY.txt')
    with open(freq_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 完整词频表\n")
        f.write("="*60 + "\n\n")
        f.write(f"{'排名':<6} {'单词':<20} {'频次':<8} {'高中'}\n")
        f.write("-"*60 + "\n")
        for rank, (word, count) in enumerate(total_counter.most_common(2000), 1):
            hs = "★" if word in HIGH_SCHOOL_VOCAB else ""
            f.write(f"{rank:<6} {word:<20} {count:<8} {hs}\n")
    print(f"\n  ✅ 词频表 → {freq_file}")
    
    # 2. 每集详细报告
    ep_file = os.path.join(output_dir, 'EPISODE_DETAILS.txt')
    with open(ep_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 每集详细词汇分析\n")
        f.write("="*70 + "\n\n")
        
        for ep in sorted(episode_data.keys()):
            data = episode_data[ep]
            f.write(f"\n{'='*70}\n")
            f.write(f"  Episode {ep:02d}\n")
            f.write(f"{'='*70}\n\n")
            f.write(f"  统计数据:\n")
            f.write(f"    - 总词次: {data['total_words']}\n")
            f.write(f"    - 不重复词: {data['unique_words']}\n")
            f.write(f"    - 新词数: {len(data['new_words'])}\n")
            f.write(f"    - 平均句长: {data['avg_sentence_len']:.1f}\n\n")
            
            f.write(f"  Top 20 高频词:\n")
            for i, (w, c) in enumerate(data['top20'], 1):
                hs = " ★" if w in HIGH_SCHOOL_VOCAB else ""
                f.write(f"    {i:2d}. {w:<15} {c:>4}{hs}\n")
            
            f.write(f"\n  高中词汇 Top 20:\n")
            for i, (w, c) in enumerate(data['hs_words'][:20], 1):
                f.write(f"    {i:2d}. {w:<15} {c:>4}\n")
            
            f.write(f"\n  本集新词 (前30):\n")
            new_words_str = ', '.join(data['new_words'][:30])
            f.write(f"    {new_words_str}\n")
    
    print(f"  ✅ 每集详情 → {ep_file}")
    
    # 3. 高中词汇学习清单
    hs_file = os.path.join(output_dir, 'HIGH_SCHOOL_VOCAB.txt')
    with open(hs_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 × 高中词汇 学习清单\n")
        f.write("="*60 + "\n\n")
        f.write(f"共 {len(hs_overlap)} 个高中词汇出现在剧中\n\n")
        
        # 按频率分级
        a_level = [(w, c) for w, c in hs_overlap if c >= 20]
        b_level = [(w, c) for w, c in hs_overlap if 10 <= c < 20]
        c_level = [(w, c) for w, c in hs_overlap if 5 <= c < 10]
        d_level = [(w, c) for w, c in hs_overlap if c < 5]
        
        f.write(f"  A级 (≥20次): {len(a_level)} 词 - 核心必背\n")
        f.write(f"  B级 (10-19次): {len(b_level)} 词 - 重点掌握\n")
        f.write(f"  C级 (5-9次): {len(c_level)} 词 - 扩展学习\n")
        f.write(f"  D级 (<5次): {len(d_level)} 词 - 了解即可\n\n")
        
        for level_name, words in [("A级 核心必背", a_level), ("B级 重点掌握", b_level), 
                                   ("C级 扩展学习", c_level), ("D级 了解即可", d_level)]:
            f.write(f"\n{'─'*60}\n")
            f.write(f"  {level_name} ({len(words)}词)\n")
            f.write(f"{'─'*60}\n")
            row_words = [w for w, c in words]
            for i in range(0, len(row_words), 6):
                row = row_words[i:i+6]
                f.write("  " + "  ".join(f"{w:<12}" for w in row) + "\n")
    
    print(f"  ✅ 高中词汇 → {hs_file}")
    
    # 4. 学习路线图
    plan_file = os.path.join(output_dir, 'STUDY_ROADMAP.txt')
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 词汇学习路线图\n")
        f.write("="*70 + "\n\n")
        f.write("建议学习周期: 4周\n")
        f.write("每周学习: 5天新词 + 2天复习\n\n")
        
        # 按主题分配
        f.write("第1周: 日常对话与家庭场景\n")
        f.write("  - 重点词汇: know, think, say, tell, talk, listen\n")
        f.write("  - 剧集参考: E01, E02\n")
        f.write("  - 学习目标: 掌握基础对话表达\n\n")
        
        f.write("第2周: 学校与工作场景\n")
        f.write("  - 重点词汇: school, work, job, money, business, deal\n")
        f.write("  - 剧集参考: E03, E04\n")
        f.write("  - 学习目标: 理解职场和学术表达\n\n")
        
        f.write("第3周: 情绪与关系表达\n")
        f.write("  - 重点词汇: feel, love, family, friend, believe, trust\n")
        f.write("  - 剧集参考: E05, E06\n")
        f.write("  - 学习目标: 表达情感和观点\n\n")
        
        f.write("第4周: 综合应用与复习\n")
        f.write("  - 重点词汇: change, life, world, hope, start, end\n")
        f.write("  - 剧集参考: E07 + 全季复习\n")
        f.write("  - 学习目标: 综合运用所学词汇\n\n")
        
        f.write("="*70 + "\n")
        f.write("每日学习计划:\n")
        f.write("  1. 观看对应剧集片段 (10分钟)\n")
        f.write("  2. 学习当日词汇 (15分钟)\n")
        f.write("  3. 听写练习 (10分钟)\n")
        f.write("  4. 复习巩固 (5分钟)\n")
    
    print(f"  ✅ 学习路线 → {plan_file}")
    
    # 5. JSON数据
    json_file = os.path.join(output_dir, 'VOCAB_DATA.json')
    json_data = {
        "meta": {
            "total_words": total_count,
            "unique_words": total_unique,
            "hs_overlap": len(hs_overlap),
            "episodes": len(episode_data),
            "subtitles": len(all_subtitles)
        },
        "frequency": [
            {"rank": i, "word": w, "count": c, "hs": w in HIGH_SCHOOL_VOCAB}
            for i, (w, c) in enumerate(total_counter.most_common(500), 1)
        ],
        "episodes": {
            str(ep): {
                "total": data['total_words'],
                "unique": data['unique_words'],
                "new_words": len(data['new_words']),
                "top20": data['top20'],
                "hs_top20": data['hs_words'][:20]
            }
            for ep, data in episode_data.items()
        },
        "growth": [
            {"episode": ep, "cumulative": cum, "new": new}
            for ep, cum, new in growth_data
        ]
    }
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON数据 → {json_file}")
    
    # ── 控制台预览 ────────────────────────────
    print("\n" + "="*70)
    print("  🏆 Top 30 高频词")
    print("="*70)
    print(f"  {'排名':<5} {'单词':<18} {'频次':<7} {'高中词汇'}")
    print("  " + "-"*50)
    for rank, (word, count) in enumerate(total_counter.most_common(30), 1):
        hs = "★ 高中词" if word in HIGH_SCHOOL_VOCAB else ""
        print(f"  {rank:<5} {word:<18} {count:<7} {hs}")
    
    print("\n" + "="*70)
    print("  📚 高中词汇 Top 30")
    print("="*70)
    print(f"  {'排名':<5} {'单词':<18} {'频次':<7} {'级别'}")
    print("  " + "-"*50)
    for rank, (word, count) in enumerate(hs_overlap[:30], 1):
        level = "A" if count >= 20 else ("B" if count >= 10 else "C")
        print(f"  {rank:<5} {word:<18} {count:<7} {level}级")
    
    print("\n" + "="*70)
    print(f"  ✅ 所有报告已保存: {output_dir}")
    print("="*70 + "\n")
    
    return json_data

if __name__ == '__main__':
    SRT_DIR = r"E:\moive\Breaking Bad 01"
    OUTPUT_DIR = r"D:\EnglishPracticeMiniProgram\docs\vocab_analysis"
    
    all_words, episode_data, subtitles = analyze_full_season(SRT_DIR)
    generate_comprehensive_report(all_words, episode_data, subtitles, OUTPUT_DIR)
