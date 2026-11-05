#!/usr/bin/env python3
"""Second pass: translate remaining English table cells and lines in AGENTS_zh.md."""
import re
import time
from pathlib import Path

from deep_translator import MyMemoryTranslator

PATH = Path(__file__).with_name("AGENTS_zh.md")
translator = MyMemoryTranslator(source="english", target="chinese simplified")
INLINE = re.compile(r"(`[^`\n]+`)")


def protect(text: str) -> tuple[str, list[str]]:
    ph: list[str] = []

    def sub(m: re.Match) -> str:
        ph.append(m.group(1))
        return f"\0I{len(ph)-1}\0"

    return INLINE.sub(sub, text), ph


def restore(text: str, ph: list[str]) -> str:
    return re.sub(r"\0I(\d+)\0", lambda m: ph[int(m.group(1))], text)


def tr_once(text: str) -> str:
    text = text.strip()
    if not text or re.match(r"^[\|\s\-:$\.c0-9FLUX\[\]]+$", text):
        return text
    if len(text) > 480:
        return text
    for attempt in range(6):
        try:
            return translator.translate(text)
        except Exception:
            time.sleep(2 ** attempt)
    return text


def translate_cell(cell: str) -> str:
    cell = cell.strip()
    if not cell or cell.startswith("http"):
        return cell
    if re.match(r"^[\-\s\|:]+$", cell):
        return cell
    protected, ph = protect(cell)
    if not protected.strip() or "\0" in protected and protected.strip().startswith("\0"):
        return cell
    if not re.search(r"[A-Za-z]{4,}", protected):
        return cell
    out = tr_once(protected)
    time.sleep(0.5)
    return restore(out, ph)


def translate_table_row(line: str) -> str:
    if not line.strip().startswith("|"):
        return line
    if re.match(r"^\|[\s\-:|]+\|\s*$", line.strip()):
        return line
    parts = line.split("|")
    new_parts = []
    for i, p in enumerate(parts):
        if i == 0 or i == len(parts) - 1:
            new_parts.append(p)
            continue
        new_parts.append(" " + translate_cell(p) + " ")
    return "|".join(new_parts)


def main() -> None:
    lines = PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if line.strip().startswith("|"):
            out.append(translate_table_row(line.rstrip("\n")) + ("\n" if line.endswith("\n") else ""))
            continue
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("http"):
            out.append(line)
            continue
        if re.search(r"[A-Za-z]{5,}", line) and not stripped.startswith("#"):
            protected, ph = protect(line.rstrip("\n"))
            if re.search(r"[A-Za-z]{5,}", protected):
                tr = tr_once(protected)
                out.append(restore(tr, ph) + ("\n" if line.endswith("\n") else ""))
                continue
        out.append(line)
    PATH.write_text("".join(out), encoding="utf-8")
    print(len("".join(out)))


if __name__ == "__main__":
    main()
