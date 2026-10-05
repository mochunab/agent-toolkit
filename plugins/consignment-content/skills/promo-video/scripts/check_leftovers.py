#!/usr/bin/env python3
"""템플릿에 남은 이전 상품 흔적 검사 — 보이는 글자(스타일·스크립트·태그 제외)에서 줄 번호와 함께 찾는다.

  python3 check_leftovers.py <영상.html> [--words 단어,단어]

기본 단어는 현관문 고무패킹 템플릿의 흔적이다. 숫자는 앞뒤가 숫자·소수점이 아닐 때만 센다.
하나라도 남으면 종료 코드 1. 새 상품에 맞게 문구를 바꾼 뒤 0건이 될 때까지 반복한다.
"""
import argparse
import re
import sys
from pathlib import Path

DEFAULT_WORDS = ["현관문", "패킹", "6.3", "2.1m", "18", "14mm", "32", "58", "난연"]


def visible_lines(html: str):
    """(줄 번호, 보이는 글자) 목록. style·script·주석은 줄 수를 유지한 채 비운다."""
    def blank(m):
        return "\n" * m.group(0).count("\n")

    html = re.sub(r"<(style|script)\b.*?</\1>", blank, html, flags=re.S)
    html = re.sub(r"<!--.*?-->", blank, html, flags=re.S)
    for no, line in enumerate(html.splitlines(), 1):
        text = " ".join(re.sub(r"<[^>]+>", " ", line).split())
        if text:
            yield no, text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path)
    ap.add_argument("--words", default="", help="쉼표로 구분한 검사 단어(기본값을 대체)")
    args = ap.parse_args()

    words = [w.strip() for w in args.words.split(",") if w.strip()] or DEFAULT_WORDS
    patterns = []
    for w in words:
        if re.fullmatch(r"[\d.]+", w):
            patterns.append((w, re.compile(r"(?<![\d.])" + re.escape(w) + r"(?![\d])")))
        else:
            patterns.append((w, re.compile(re.escape(w))))

    hits = []
    for no, text in visible_lines(args.html.read_text(encoding="utf-8")):
        for w, pat in patterns:
            if pat.search(text):
                hits.append(f"  {args.html.name}:{no}  [{w}]  {text[:70]}")
    print(f"이전 상품 흔적: {len(hits)}건")
    print("\n".join(hits) if hits else "  없음")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
