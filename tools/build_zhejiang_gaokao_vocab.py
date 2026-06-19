#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Zhejiang Gaokao-oriented vocabulary tables.

Source policy:
- Zhejiang's English Gaokao vocabulary scope is treated as the national
  high-school/Gaokao vocabulary scope for this data build.
- The machine-readable base list is extracted from ECDICT rows tagged `gk`.
- Frequency is reported from ECDICT BNC/FRQ ranks and the local corpus
  frequency report already produced in docs/vocab_analysis.
"""

from __future__ import annotations

import csv
import json
import re
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ECDICT_CSV = ROOT / "data_sources" / "ecdict.csv"
VOCAB_FREQ_TXT = ROOT / "docs" / "vocab_analysis" / "FULL_FREQUENCY.txt"
OUT_DIR = ROOT / "docs" / "zhejiang_gaokao_vocab"


def normalize_translation(text: str) -> str:
    text = (text or "").replace("\r\n", "\n").replace("\\n", "\n")
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("[网络]"):
            continue
        lines.append(line)
    return "；".join(lines)


def to_int(value: str) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def load_local_corpus_frequency() -> dict[str, dict[str, int]]:
    """Parse the existing corpus frequency report.

    The text file format is:
    rank word count high_school_marker
    """
    freq: dict[str, dict[str, int]] = {}
    if not VOCAB_FREQ_TXT.exists():
        return freq

    pattern = re.compile(r"^\s*(\d+)\s+([A-Za-z][A-Za-z'-]*)\s+(\d+)\b")
    with VOCAB_FREQ_TXT.open("r", encoding="utf-8") as f:
        for line in f:
            match = pattern.match(line)
            if not match:
                continue
            rank, word, count = match.groups()
            freq[word.lower()] = {"local_rank": int(rank), "local_count": int(count)}
    return freq


def priority_from(row: dict[str, str], local_count: int) -> str:
    frq = to_int(row.get("frq", "0"))
    bnc = to_int(row.get("bnc", "0"))
    collins = to_int(row.get("collins", "0"))
    oxford = row.get("oxford") == "1"

    if local_count >= 20 or collins >= 5 or (frq and frq <= 1000) or oxford:
        return "A"
    if local_count >= 5 or collins >= 3 or (frq and frq <= 3000) or (bnc and bnc <= 3000):
        return "B"
    if local_count > 0 or collins >= 1 or (frq and frq <= 8000) or (bnc and bnc <= 8000):
        return "C"
    return "D"


def load_gaokao_words(ecdict_csv: Path) -> list[dict[str, str]]:
    if not ecdict_csv.exists():
        raise FileNotFoundError(
            "Missing ECDICT CSV. Download ecdict.csv from "
            "https://github.com/skywind3000/ECDICT and run: "
            "python tools/build_zhejiang_gaokao_vocab.py --ecdict path/to/ecdict.csv"
        )

    local_freq = load_local_corpus_frequency()
    rows: list[dict[str, str]] = []
    seen: set[str] = set()

    with ecdict_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            word = (raw.get("word") or "").strip()
            word_key = word.lower()
            tags = (raw.get("tag") or "").split()

            if "gk" not in tags:
                continue
            if not word or word_key in seen:
                continue

            seen.add(word_key)
            local = local_freq.get(word_key, {"local_rank": 0, "local_count": 0})
            item = {
                "word": word,
                "word_lower": word_key,
                "phonetic": raw.get("phonetic", ""),
                "translation": normalize_translation(raw.get("translation", "")),
                "definition": (raw.get("definition") or "").replace("\\n", " ").strip(),
                "tags": raw.get("tag", ""),
                "collins": raw.get("collins", ""),
                "oxford": raw.get("oxford", ""),
                "bnc_rank": str(to_int(raw.get("bnc", "0"))),
                "frq_rank": str(to_int(raw.get("frq", "0"))),
                "exchange": raw.get("exchange", ""),
                "local_corpus_rank": str(local["local_rank"]),
                "local_corpus_count": str(local["local_count"]),
                "priority": priority_from(raw, local["local_count"]),
            }
            rows.append(item)

    rows.sort(key=lambda r: (
        r["priority"],
        -int(r["local_corpus_count"]),
        int(r["frq_rank"] or "0") if int(r["frq_rank"] or "0") > 0 else 999999,
        r["word_lower"],
    ))
    for i, row in enumerate(rows, 1):
        row["gaokao_rank"] = str(i)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    fieldnames = [
        "gaokao_rank",
        "word",
        "phonetic",
        "translation",
        "priority",
        "local_corpus_count",
        "local_corpus_rank",
        "frq_rank",
        "bnc_rank",
        "collins",
        "oxford",
        "tags",
        "exchange",
        "definition",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def write_json(path: Path, rows: list[dict[str, str]]) -> None:
    payload = {
        "meta": {
            "name": "Zhejiang Gaokao English Vocabulary",
            "scope": "Gaokao-tagged words from ECDICT, used as Zhejiang Gaokao-oriented baseline",
            "source": "ECDICT ecdict.csv tag=gk",
            "total_words": len(rows),
            "local_corpus": "docs/vocab_analysis/FULL_FREQUENCY.txt",
        },
        "words": rows,
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_readme(path: Path, rows: list[dict[str, str]]) -> None:
    covered = [r for r in rows if int(r["local_corpus_count"]) > 0]
    missing = [r for r in rows if int(r["local_corpus_count"]) == 0]
    priorities = {p: sum(1 for r in rows if r["priority"] == p) for p in "ABCD"}

    top_local = sorted(
        covered,
        key=lambda r: (-int(r["local_corpus_count"]), int(r["local_corpus_rank"] or "999999")),
    )[:30]
    top_lines = "\n".join(
        f"| {i} | {r['word']} | {r['translation'][:36]} | {r['local_corpus_count']} | {r['priority']} |"
        for i, r in enumerate(top_local, 1)
    )

    text = f"""# 浙江高考英语词汇表与词频

生成日期：2026-06-13

## 数据口径

本目录把“浙江高考英语词汇”按高考英语通用词汇口径整理。机器可处理底表来自 ECDICT `ecdict.csv` 中带 `gk` 标签的词条，共 {len(rows)} 个 headword。浙江新高考英语没有在本仓库中附带一份单独、机器可读且可核验的官方专属词表；因此本版作为“浙江高考可用基线词表”，后续如果拿到学校/考试院指定词表，可用同一脚本替换或校准。

## 输出文件

- `zhejiang_gaokao_vocab_full.csv`：完整词汇主表，适合 Excel 查看。
- `zhejiang_gaokao_vocab_full.json`：完整词汇 JSON，适合小程序或后端使用。
- `zhejiang_gaokao_frequency.csv`：按优先级、当前语料出现频次、通用词频排序。
- `zhejiang_gaokao_covered_by_current_corpus.csv`：已在当前 Breaking Bad 语料中出现的高考词。
- `zhejiang_gaokao_missing_in_current_corpus.csv`：当前语料未覆盖的高考词，后续应补充语料或例句。

## 总览

| 指标 | 数值 |
|---|---:|
| 高考词条总数 | {len(rows)} |
| 当前语料已覆盖 | {len(covered)} |
| 当前语料未覆盖 | {len(missing)} |
| 当前语料覆盖率 | {len(covered) / len(rows):.2%} |
| A 级优先词 | {priorities['A']} |
| B 级优先词 | {priorities['B']} |
| C 级优先词 | {priorities['C']} |
| D 级补充词 | {priorities['D']} |

## 优先级规则

- A：当前语料高频、Collins 高频、Oxford 核心词或 ECDICT 高频排名靠前。
- B：当前语料有一定出现，或通用词频较高。
- C：当前语料出现过但频次低，或通用词频中等。
- D：高考标签内的补充词，当前语料未覆盖且通用频率较低。

## 当前语料 Top 30 高考词

| 排名 | 单词 | 释义摘录 | 当前语料频次 | 优先级 |
|---:|---|---|---:|---|
{top_lines}

## 使用建议

第一阶段先把 A/B 级词做成小程序词包和复习队列；第二阶段补齐 `missing` 文件中未覆盖的高考词，为每个词至少准备 3 条真实或准真实语料；第三阶段再把用户错词、浙江高考真题/模拟题语料加入词频统计。
"""
    path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Zhejiang Gaokao vocabulary tables.")
    parser.add_argument(
        "--ecdict",
        type=Path,
        default=DEFAULT_ECDICT_CSV,
        help="Path to ECDICT ecdict.csv. Default: data_sources/ecdict.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_gaokao_words(args.ecdict)
    covered = [r for r in rows if int(r["local_corpus_count"]) > 0]
    missing = [r for r in rows if int(r["local_corpus_count"]) == 0]
    frequency = sorted(
        rows,
        key=lambda r: (
            r["priority"],
            -int(r["local_corpus_count"]),
            int(r["frq_rank"] or "0") if int(r["frq_rank"] or "0") > 0 else 999999,
            int(r["bnc_rank"] or "0") if int(r["bnc_rank"] or "0") > 0 else 999999,
            r["word_lower"],
        ),
    )

    write_csv(OUT_DIR / "zhejiang_gaokao_vocab_full.csv", rows)
    write_json(OUT_DIR / "zhejiang_gaokao_vocab_full.json", rows)
    write_csv(OUT_DIR / "zhejiang_gaokao_frequency.csv", frequency)
    write_csv(OUT_DIR / "zhejiang_gaokao_covered_by_current_corpus.csv", covered)
    write_csv(OUT_DIR / "zhejiang_gaokao_missing_in_current_corpus.csv", missing)
    write_readme(OUT_DIR / "README.md", rows)

    print(json.dumps({
        "total": len(rows),
        "covered": len(covered),
        "missing": len(missing),
        "out_dir": str(OUT_DIR),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
