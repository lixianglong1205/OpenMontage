#!/usr/bin/env python3
"""Translate AGENTS.md prose to Chinese while preserving code blocks."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

SRC = Path(__file__).with_name("AGENTS.md")
DST = Path(__file__).with_name("AGENTS_zh.md")
CACHE_PATH = Path(__file__).with_name("_agents_zh_cache.json")

CHUNK_MAX = 4800
SLEEP = 0.08


def gtx_translate(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    q = urllib.parse.quote(text[:5000])
    url = (
        "https://translate.googleapis.com/translate_a/single"
        f"?client=at&dt=t&sl=en&tl=zh-CN&q={q}"
    )
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    )
                },
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return "".join(p[0] for p in data[0] if p[0])
        except Exception:
            time.sleep(min(2**attempt, 15))
    return text


def split_blocks(text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for part in re.split(r"(```[\s\S]*?```)", text):
        if not part:
            continue
        blocks.append(("code" if part.startswith("```") else "prose", part))
    return blocks


def split_chunks(prose: str) -> list[str]:
    if len(prose) <= CHUNK_MAX:
        return [prose]
    lines = prose.splitlines(keepends=True)
    chunks: list[str] = []
    buf = ""
    for line in lines:
        if len(buf) + len(line) > CHUNK_MAX and buf:
            chunks.append(buf)
            buf = line
        else:
            buf += line
    if buf:
        chunks.append(buf)
    return chunks


def apply_labels(s: str) -> str:
    repl = {
        "**Note:**": "**注意：**",
        "**Incorrect:": "**错误：",
        "**Correct:": "**正确：",
        "# React Best Practices": "# React 最佳实践",
        "## Abstract": "## 摘要",
        "## Table of Contents": "## 目录",
        "## References": "## 参考",
        "**Impact: CRITICAL**": "**影响：关键**",
        "**Impact: HIGH**": "**影响：高**",
        "**Impact: MEDIUM**": "**影响：中**",
        "**Impact: LOW**": "**影响：低**",
        "**Impact: MEDIUM-HIGH**": "**影响：中高**",
        "**Impact: LOW-MEDIUM**": "**影响：低中**",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    for level, zh in (
        ("CRITICAL", "关键"),
        ("HIGH", "高"),
        ("MEDIUM-HIGH", "中高"),
        ("MEDIUM", "中"),
        ("LOW-MEDIUM", "低中"),
        ("LOW", "低"),
    ):
        s = re.sub(
            rf"\*\*Impact: {level} \(([^)]+)\)\*\*",
            rf"**影响：{zh}（\1）**",
            s,
        )
    return s


def needs_translation(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]{4,}", text))


def translate_text(text: str, cache: dict[str, str]) -> str:
    if not needs_translation(text):
        return text
    if text in cache:
        return cache[text]
    out: list[str] = []
    for chunk in split_chunks(text):
        if not needs_translation(chunk):
            out.append(chunk)
            continue
        if chunk not in cache:
            cache[chunk] = gtx_translate(chunk)
            time.sleep(SLEEP)
            if len(cache) % 15 == 0:
                CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        out.append(cache[chunk])
    joined = "".join(out)
    cache[text] = joined
    return joined


def main() -> int:
    if not SRC.is_file():
        print("FAIL reason=missing source", file=sys.stderr)
        return 1
    cache: dict[str, str] = {}
    if CACHE_PATH.is_file():
        try:
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}

    source = SRC.read_text(encoding="utf-8")
    blocks = split_blocks(source)
    result: list[str] = []
    for i, (kind, content) in enumerate(blocks):
        if kind == "code":
            result.append(content)
        else:
            result.append(translate_text(content, cache))
        if (i + 1) % 10 == 0:
            print(f"block {i+1}/{len(blocks)} cache={len(cache)}", flush=True)

    text = apply_labels("".join(result))
    DST.write_text(text, encoding="utf-8")
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    print(f"SUCCESS path={DST} chars={len(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
