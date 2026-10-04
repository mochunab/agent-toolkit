#!/usr/bin/env python3
"""마크다운 → HWPX 신규 문서 생성.

usage:
  hwpx_build.py input.md -o out.hwpx [--title "문서 제목"]
  cat doc.md | hwpx_build.py - -o out.hwpx

지원: # 제목(1~6) · 문단 · | 표 | · - 목록 · 1. 번호목록 · > 인용 · --- 구분선
인라인 **굵게** `코드` [링크](url) 마커는 텍스트만 남김(HWPX 서식 미적용).
"""
import argparse, re, sys
from hwpx.document import HwpxDocument

INLINE = [
    (re.compile(r"\*\*(.+?)\*\*"), r"\1"),
    (re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)"), r"\1"),
    (re.compile(r"`(.+?)`"), r"\1"),
    (re.compile(r"~~(.+?)~~"), r"\1"),
    (re.compile(r"\[(.+?)\]\((.+?)\)"), r"\1(\2)"),
]


def clean(s):
    s = s.strip()
    for pat, rep in INLINE:
        s = pat.sub(rep, s)
    return s


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [clean(c) for c in line.split("|")]


def is_sep(line):
    return bool(re.fullmatch(r"\|?[\s:|-]*-[\s:|-]*\|?", line.strip())) and "-" in line


def parse(md):
    """마크다운 → 블록 리스트."""
    blocks, lines, i = [], md.splitlines(), 0
    buf = []

    def flush():
        if buf:
            blocks.append(("para", clean(" ".join(buf))))
            buf.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if not s:
            flush(); i += 1; continue

        if s.startswith("```"):                      # 코드펜스: 내용만 문단으로
            flush(); i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            for c in code:
                blocks.append(("para", c))
            continue

        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if m:
            flush(); blocks.append(("head", len(m.group(1)), clean(m.group(2)))); i += 1; continue

        if s.startswith("|") and i + 1 < len(lines) and is_sep(lines[i + 1]):
            flush()
            rows = [split_row(s)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i])); i += 1
            blocks.append(("table", rows)); continue

        if re.fullmatch(r"[-*_]{3,}", s):
            flush(); i += 1; continue

        m = re.match(r"^\s*([-*+])\s+(.*)", ln)
        if m:
            flush(); blocks.append(("para", "· " + clean(m.group(2)))); i += 1; continue

        m = re.match(r"^\s*(\d+)[.)]\s+(.*)", ln)
        if m:
            flush(); blocks.append(("para", f"{m.group(1)}. " + clean(m.group(2)))); i += 1; continue

        if s.startswith(">"):
            flush(); blocks.append(("para", clean(s.lstrip("> ")))); i += 1; continue

        buf.append(s); i += 1

    flush()
    return blocks


def build(blocks, title=None):
    d = HwpxDocument.new()
    if title:
        d.add_heading(title, level=1)
    for b in blocks:
        if b[0] == "head":
            d.add_heading(b[2], level=min(b[1], 6))
        elif b[0] == "para":
            d.add_paragraph(b[1])
        elif b[0] == "table":
            rows = b[1]
            ncol = max(len(r) for r in rows)
            t = d.add_table(rows=len(rows), cols=ncol)
            for ri, row in enumerate(rows):
                for ci in range(ncol):
                    t.set_cell_text(ri, ci, row[ci] if ci < len(row) else "")
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="마크다운 파일 (- = stdin)")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--title")
    a = ap.parse_args()

    md = sys.stdin.read() if a.input == "-" else open(a.input, encoding="utf-8").read()
    blocks = parse(md)
    d = build(blocks, a.title)
    d.save_to_path(a.output)

    r = HwpxDocument.open(a.output)
    rep = r.validate()
    kinds = {}
    for b in blocks:
        kinds[b[0]] = kinds.get(b[0], 0) + 1
    print(f"저장: {a.output}")
    print(f"블록: {kinds}")
    print(f"검증: 표 {len(list(r.tables))} · 문단 {len(list(r.paragraphs))} · 스키마 {'OK' if not rep.issues else rep.issues}")
    return 0 if not rep.issues else 1


if __name__ == "__main__":
    sys.exit(main())
