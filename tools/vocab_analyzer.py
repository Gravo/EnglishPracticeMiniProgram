#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
Breaking Bad S01 词汇频率分析工具
分析所有 SRT 字幕文件，输出：
  1. 全词频表（前2000）
  2. 与高中词汇重叠部分
  3. 按频率分级的学习计划
"""

import re
import os
import json
from collections import Counter

# ─────────────────────────────────────────────
# 高中英语核心词汇表（3500词精简版）
# 来源：人教版高中英语词汇表 + CET-4 核心词
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# 停用词（不计入有效词汇）
# ─────────────────────────────────────────────
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

def parse_srt(filepath):
    """解析 SRT 字幕文件，返回纯文本列表"""
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return lines

    # 去掉序号行和时间戳行
    blocks = re.split(r'\n\n+', content.strip())
    for block in blocks:
        block_lines = block.strip().split('\n')
        for line in block_lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r'^\d+$', line):
                continue
            if re.match(r'^\d{2}:\d{2}:\d{2}', line):
                continue
            # 去掉 HTML 标签
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                lines.append(line)
    return lines

def extract_words(text_lines):
    """从文本行中提取单词（小写，去标点）"""
    words = []
    for line in text_lines:
        # 只保留字母和撇号（处理缩写）
        line = line.lower()
        # 展开常见缩写
        line = re.sub(r"n't", " not", line)
        line = re.sub(r"'re", " are", line)
        line = re.sub(r"'ve", " have", line)
        line = re.sub(r"'ll", " will", line)
        line = re.sub(r"'d", " would", line)
        line = re.sub(r"'m", " am", line)
        # 提取单词
        tokens = re.findall(r"[a-z]+", line)
        for w in tokens:
            if len(w) >= 2 and w not in STOP_WORDS:
                words.append(w)
    return words

def analyze_vocab(srt_dir):
    """主分析函数"""
    all_words = []
    episode_stats = {}

    srt_files = sorted([
        f for f in os.listdir(srt_dir) if f.endswith('.srt')
    ])

    print(f"\n{'='*60}")
    print(f"  Breaking Bad S01 词汇分析")
    print(f"{'='*60}")
    print(f"\n📂 字幕目录: {srt_dir}")
    print(f"📺 集数: {len(srt_files)} 集\n")

    for fname in srt_files:
        fpath = os.path.join(srt_dir, fname)
        lines = parse_srt(fpath)
        words = extract_words(lines)
        all_words.extend(words)

        ep_counter = Counter(words)
        ep_name = re.search(r's01e0?(\d+)', fname.lower())
        ep_num = ep_name.group(1) if ep_name else fname
        episode_stats[f"E{ep_num.zfill(2)}"] = {
            'total_words': len(words),
            'unique_words': len(ep_counter),
            'top10': ep_counter.most_common(10)
        }
        print(f"  ✅ E{ep_num.zfill(2)}: {len(words)} 词次 / {len(ep_counter)} 不重复词")

    return all_words, episode_stats

def generate_report(all_words, episode_stats, output_dir):
    """生成完整分析报告"""
    total_counter = Counter(all_words)
    total_unique = len(total_counter)
    total_count = len(all_words)

    # ── 1. 全词频表（前2000）──────────────────
    top2000 = total_counter.most_common(2000)

    # ── 2. 高中词汇重叠 ──────────────────────
    hs_overlap = [
        (w, c) for w, c in total_counter.most_common()
        if w in HIGH_SCHOOL_VOCAB
    ]

    # ── 3. 分级词汇（按频率）─────────────────
    # A级：出现≥20次（核心高频）
    # B级：出现10-19次（重要词汇）
    # C级：出现5-9次（常用词汇）
    # D级：出现2-4次（低频词汇）
    level_a = [(w, c) for w, c in top2000 if c >= 20]
    level_b = [(w, c) for w, c in top2000 if 10 <= c < 20]
    level_c = [(w, c) for w, c in top2000 if 5 <= c < 10]
    level_d = [(w, c) for w, c in top2000 if 2 <= c < 5]

    # ── 4. 学习周期规划 ──────────────────────
    # 每天学习20个词，按频率优先
    hs_sorted = sorted(hs_overlap, key=lambda x: -x[1])
    study_plan = []
    for i in range(0, min(len(hs_sorted), 200), 20):
        day = i // 20 + 1
        batch = hs_sorted[i:i+20]
        study_plan.append({
            'day': day,
            'words': batch,
            'focus': get_day_focus(day)
        })

    # ── 输出报告 ─────────────────────────────
    os.makedirs(output_dir, exist_ok=True)

    # 控制台摘要
    print(f"\n{'='*60}")
    print(f"  📊 分析结果摘要")
    print(f"{'='*60}")
    print(f"  总词次:        {total_count:,}")
    print(f"  不重复词:      {total_unique:,}")
    print(f"  高中词汇重叠:  {len(hs_overlap)} 词")
    print(f"  A级词(≥20次): {len(level_a)} 词")
    print(f"  B级词(10-19): {len(level_b)} 词")
    print(f"  C级词(5-9次): {len(level_c)} 词")
    print(f"  D级词(2-4次): {len(level_d)} 词")

    # ── 文件1: 完整词频表（前2000）────────────
    freq_path = os.path.join(output_dir, '01_full_frequency.txt')
    with open(freq_path, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 完整词频表（前2000）\n")
        f.write("=" * 50 + "\n")
        f.write(f"{'排名':<6} {'单词':<20} {'频次':<8} {'高中词汇'}\n")
        f.write("-" * 50 + "\n")
        for rank, (word, count) in enumerate(top2000, 1):
            hs_mark = "★" if word in HIGH_SCHOOL_VOCAB else ""
            f.write(f"{rank:<6} {word:<20} {count:<8} {hs_mark}\n")
    print(f"\n  📄 词频表 → {freq_path}")

    # ── 文件2: 高中词汇重叠 ───────────────────
    hs_path = os.path.join(output_dir, '02_highschool_overlap.txt')
    with open(hs_path, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 × 高中词汇 重叠分析\n")
        f.write("=" * 50 + "\n")
        f.write(f"共 {len(hs_overlap)} 个高中词汇出现在剧中\n\n")
        f.write(f"{'排名':<6} {'单词':<20} {'频次':<8} {'级别'}\n")
        f.write("-" * 50 + "\n")
        for rank, (word, count) in enumerate(hs_sorted, 1):
            if count >= 20:
                level = "A级 ★★★"
            elif count >= 10:
                level = "B级 ★★"
            elif count >= 5:
                level = "C级 ★"
            else:
                level = "D级"
            f.write(f"{rank:<6} {word:<20} {count:<8} {level}\n")
    print(f"  📄 高中词汇 → {hs_path}")

    # ── 文件3: 分级词汇表 ─────────────────────
    level_path = os.path.join(output_dir, '03_leveled_vocab.txt')
    with open(level_path, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 分级词汇表\n")
        f.write("=" * 50 + "\n\n")

        for level_name, level_words, desc in [
            ("A级 核心高频词（≥20次）", level_a, "必须掌握，剧中反复出现"),
            ("B级 重要词汇（10-19次）", level_b, "重点学习，高频场景词"),
            ("C级 常用词汇（5-9次）", level_c, "扩展词汇，情景理解"),
            ("D级 低频词汇（2-4次）", level_d, "了解即可，语境词"),
        ]:
            f.write(f"\n{'─'*50}\n")
            f.write(f"  {level_name}\n")
            f.write(f"  {desc}  共 {len(level_words)} 词\n")
            f.write(f"{'─'*50}\n")
            # 每行8个词
            words_only = [w for w, c in level_words]
            for i in range(0, len(words_only), 8):
                row = words_only[i:i+8]
                f.write("  " + "  ".join(f"{w:<14}" for w in row) + "\n")
    print(f"  📄 分级词汇 → {level_path}")

    # ── 文件4: 学习计划（10天）───────────────
    plan_path = os.path.join(output_dir, '04_study_plan.txt')
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 × 高中词汇 - 10天学习计划\n")
        f.write("=" * 60 + "\n")
        f.write("策略：优先学习剧中高频出现的高中词汇\n")
        f.write("每天：20个词 + 对应剧集场景复习\n\n")

        for plan in study_plan:
            f.write(f"\n{'─'*60}\n")
            f.write(f"  第 {plan['day']:02d} 天  |  {plan['focus']}\n")
            f.write(f"{'─'*60}\n")
            f.write(f"  {'单词':<18} {'频次':<8} {'记忆提示'}\n")
            f.write(f"  {'-'*50}\n")
            for word, count in plan['words']:
                hint = get_memory_hint(word)
                f.write(f"  {word:<18} {count:<8} {hint}\n")
    print(f"  📄 学习计划 → {plan_path}")

    # ── 文件5: 每集词汇统计 ───────────────────
    ep_path = os.path.join(output_dir, '05_episode_stats.txt')
    with open(ep_path, 'w', encoding='utf-8') as f:
        f.write("Breaking Bad S01 - 每集词汇统计\n")
        f.write("=" * 50 + "\n\n")
        for ep, stats in episode_stats.items():
            f.write(f"  {ep}  总词次: {stats['total_words']:>5}  不重复: {stats['unique_words']:>4}\n")
            f.write(f"       Top10: {', '.join(w for w, c in stats['top10'])}\n\n")
    print(f"  📄 每集统计 → {ep_path}")

    # ── 文件6: JSON 数据（供小程序使用）────────
    json_data = {
        "meta": {
            "total_words": total_count,
            "unique_words": total_unique,
            "hs_overlap_count": len(hs_overlap),
            "episodes": len(episode_stats)
        },
        "top200": [{"word": w, "count": c, "hs": w in HIGH_SCHOOL_VOCAB}
                   for w, c in top2000[:200]],
        "hs_overlap": [{"word": w, "count": c} for w, c in hs_sorted[:300]],
        "levels": {
            "A": [{"word": w, "count": c} for w, c in level_a],
            "B": [{"word": w, "count": c} for w, c in level_b],
            "C": [{"word": w, "count": c} for w, c in level_c],
        }
    }
    json_path = os.path.join(output_dir, '06_vocab_data.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  📄 JSON数据 → {json_path}")

    # ── 控制台：Top50 预览 ────────────────────
    print(f"\n{'='*60}")
    print(f"  🏆 Top 50 高频词（含高中词汇标记）")
    print(f"{'='*60}")
    print(f"  {'排名':<5} {'单词':<18} {'频次':<7} {'高中词汇'}")
    print(f"  {'-'*45}")
    for rank, (word, count) in enumerate(top2000[:50], 1):
        hs = "★ 高中词" if word in HIGH_SCHOOL_VOCAB else ""
        print(f"  {rank:<5} {word:<18} {count:<7} {hs}")

    print(f"\n{'='*60}")
    print(f"  📚 高中词汇 Top 30（按剧中频率）")
    print(f"{'='*60}")
    print(f"  {'排名':<5} {'单词':<18} {'频次':<7} {'级别'}")
    print(f"  {'-'*45}")
    for rank, (word, count) in enumerate(hs_sorted[:30], 1):
        if count >= 20:
            lv = "A ★★★"
        elif count >= 10:
            lv = "B ★★"
        else:
            lv = "C ★"
        print(f"  {rank:<5} {word:<18} {count:<7} {lv}")

    print(f"\n{'='*60}")
    print(f"  ✅ 所有报告已保存到: {output_dir}")
    print(f"{'='*60}\n")

    return json_data

def get_day_focus(day):
    focuses = {
        1: "日常对话 - 打招呼/家庭场景",
        2: "情绪表达 - 愤怒/惊讶/担忧",
        3: "化学课堂 - 学科词汇",
        4: "犯罪场景 - 执法/逃跑",
        5: "人际关系 - 家庭/朋友",
        6: "商业谈判 - 交易/金钱",
        7: "医疗场景 - 疾病/诊断",
        8: "日常生活 - 工作/购物",
        9: "心理描写 - 思考/决定",
        10: "综合复习 - 高频核心词"
    }
    return focuses.get(day, f"第{day}天学习")

def get_memory_hint(word):
    hints = {
        'know': '→ I know / You know (口头禅)',
        'right': '→ right? / all right (确认语气)',
        'look': '→ look at this / look (引起注意)',
        'think': '→ I think / just think (思考)',
        'want': '→ I want / you want (欲望)',
        'need': '→ I need / we need (需求)',
        'come': '→ come on / come here (催促)',
        'good': '→ good / pretty good (评价)',
        'money': '→ easy money / lot of money',
        'work': '→ work here / it works',
        'tell': '→ tell me / I tell you',
        'talk': '→ talk to me / we talked',
        'back': '→ come back / get back',
        'little': '→ a little / little bit',
        'man': '→ man! / come on man (感叹)',
        'time': '→ what time / first time',
        'place': '→ this place / take place',
        'house': '→ in the house / my house',
        'life': '→ my life / all of life',
        'change': '→ change into / things change',
    }
    return hints.get(word, '→ 结合剧情场景记忆')

if __name__ == '__main__':
    SRT_DIR = r"E:\moive\Breaking Bad 01"
    OUTPUT_DIR = r"D:\EnglishPracticeMiniProgram\docs\vocab_analysis"

    all_words, episode_stats = analyze_vocab(SRT_DIR)
    generate_report(all_words, episode_stats, OUTPUT_DIR)
