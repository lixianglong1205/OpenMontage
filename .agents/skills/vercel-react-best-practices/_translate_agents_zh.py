#!/usr/bin/env python3
"""Line-preserving translation of AGENTS.md to AGENTS_zh.md."""
from __future__ import annotations

import json
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SRC = Path(__file__).with_name("AGENTS.md")
DST = Path(__file__).with_name("AGENTS_zh.md")
CACHE_PATH = Path(__file__).with_name("_agents_zh_line_cache.json")
WORKERS = 10
_lock = threading.Lock()


def gtx_translate(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return text
    q = urllib.parse.quote(stripped[:4800])
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
            time.sleep(min(2**attempt, 12))
    return text


def apply_labels(line: str) -> str:
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
    out = line
    for k, v in repl.items():
        out = out.replace(k, v)
    for level, zh in (
        ("CRITICAL", "关键"),
        ("HIGH", "高"),
        ("MEDIUM-HIGH", "中高"),
        ("MEDIUM", "中"),
        ("LOW-MEDIUM", "低中"),
        ("LOW", "低"),
    ):
        out = re.sub(
            rf"\*\*Impact: {level} \(([^)]+)\)\*\*",
            rf"**影响：{zh}（\1）**",
            out,
        )
    return out


def needs_translation(line: str) -> bool:
    s = line.strip()
    if not s or s == "---":
        return False
    if s.startswith("```"):
        return False
    if re.match(r"^Reference:\s*\[https?://", s):
        return False
    if re.match(r"^\d+\.\s+\[https?://", s):
        return False
    if s.startswith("|") and re.match(r"^\|[\s\-:|]+\|\s*$", s):
        return False
    return bool(re.search(r"[A-Za-z]{3,}", line))


def translate_table_line(line: str, cache: dict[str, str]) -> str:
    if not line.strip().startswith("|"):
        return translate_line(line, cache)
    if re.match(r"^\|[\s\-:|]+\|\s*$", line.strip()):
        return line
    parts = line.split("|")
    new: list[str] = []
    for i, part in enumerate(parts):
        if i in (0, len(parts) - 1):
            new.append(part)
            continue
        cell = part.strip()
        if not needs_translation(part):
            new.append(part)
            continue
        prefix, suffix = part[: len(part) - len(part.lstrip())], part[len(part.rstrip()) :]
        inner = translate_line(cell + ("\n" if cell.endswith("\n") else ""), cache).strip()
        new.append(f"{prefix}{inner}{suffix if suffix else ' '}")
    return "|".join(new)


def translate_line(line: str, cache: dict[str, str]) -> str:
    line = apply_labels(line)
    if not needs_translation(line):
        return line
    nl = "\n" if line.endswith("\n") else ""
    core = line.rstrip("\n")
    if core in cache:
        return cache[core] + nl
    return core + nl  # placeholder; filled in batch


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

    lines = SRC.read_text(encoding="utf-8").splitlines(keepends=True)
    in_code = False
    pending: list[str] = []
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.strip().startswith("|"):
            if needs_translation(line):
                pending.append(line.rstrip("\n"))
        elif needs_translation(line):
            pending.append(line.rstrip("\n"))

    unique = list(dict.fromkeys(pending))
    missing = [u for u in unique if u not in cache]
    print(f"lines to translate: {len(unique)} missing: {len(missing)}", flush=True)

    def work(s: str) -> tuple[str, str]:
        return s, apply_labels(gtx_translate(s))

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = [pool.submit(work, s) for s in missing]
        done = 0
        for fut in as_completed(futs):
            src, dst = fut.result()
            with _lock:
                cache[src] = dst
                done += 1
                if done % 25 == 0:
                    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
                    print(f"translated {done}/{len(missing)}", flush=True)

    out: list[str] = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        if line.strip().startswith("|") and needs_translation(line):
            out.append(translate_table_line(line, cache))
        elif needs_translation(line):
            core = apply_labels(line.rstrip("\n"))
            nl = "\n" if line.endswith("\n") else ""
            out.append(cache.get(core, core) + nl)
        else:
            out.append(apply_labels(line))

    text = "".join(out)
    DST.write_text(text, encoding="utf-8")
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    print(f"SUCCESS path={DST} chars={len(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
