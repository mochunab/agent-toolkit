#!/usr/bin/env python3
"""HWPX 구조·본문 덤프. 양식 파악 → 채울 좌표 결정용.

usage:
  hwpx_read.py FILE.hwpx                 # 요약 + 표 인덱스
  hwpx_read.py FILE.hwpx --md            # 본문 마크다운 전문
  hwpx_read.py FILE.hwpx --table 3       # 표 3번 격자 전체
  hwpx_read.py FILE.hwpx --grep 사업자  # 텍스트 검색 (표 좌표 포함)
  hwpx_read.py FILE.hwpx --labels       # 채울 수 있는 라벨 목록 (fill 스펙용)
"""
import argparse, sys
from hwpx.document import HwpxDocument


def cell_text(t, r, c):
    try:
        v = t.cell(r, c)
        return (v.text or "").strip() if v is not None else ""
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--md", action="store_true", help="본문 마크다운 전문")
    ap.add_argument("--table", type=int, help="표 N번 격자 덤프")
    ap.add_argument("--grep", help="텍스트 검색")
    ap.add_argument("--labels", action="store_true", help="채울 수 있는 라벨 목록")
    ap.add_argument("--limit", type=int, default=60, help="셀 미리보기 길이")
    a = ap.parse_args()

    d = HwpxDocument.open(a.file)
    tables = list(d.tables)

    if a.md:
        print(d.text.markdown())
        return

    if a.table is not None:
        t = tables[a.table]
        print(f"[표 {a.table}] {t.row_count}행 x {t.column_count}열")
        for r in range(t.row_count):
            cells = [cell_text(t, r, c)[: a.limit].replace("\n", "⏎") for c in range(t.column_count)]
            print(f"  r{r}: " + " | ".join(cells))
        return

    if a.labels:
        print("-- 라벨 후보 (fill 스펙의 labels 키에 '라벨>right' 형태로 그대로 복사) --")
        print("   ⚠️ 내부 공백까지 원문 그대로. '상      호' ≠ '상호'\n")
        for i, t in enumerate(tables):
            for r in range(t.row_count):
                label = cell_text(t, r, 0)
                if not label or len(label) > 30:
                    continue
                right = cell_text(t, r, 1) if t.column_count > 1 else ""
                below = cell_text(t, r + 1, 0) if r + 1 < t.row_count else ""
                tgt, direction = (right, "right") if right else (below, "below")
                if not tgt:
                    continue
                print(f"  표{i:>2} | {label!r}>{direction}  →  현재값 {tgt[:40]!r}")
        return

    if a.grep:
        hits = 0
        for i, t in enumerate(tables):
            for r in range(t.row_count):
                for c in range(t.column_count):
                    txt = cell_text(t, r, c)
                    if a.grep in txt:
                        print(f"표{i} r{r} c{c}: {txt[: a.limit]}")
                        hits += 1
        for i, p in enumerate(d.paragraphs):
            txt = (p.text or "").strip()
            if a.grep in txt:
                print(f"문단{i}: {txt[: a.limit]}")
                hits += 1
        print(f"-- {hits}건")
        return

    rep = d.validate()
    print(f"파일      : {a.file}")
    print(f"섹션      : {len(d.sections)}")
    print(f"문단      : {len(list(d.paragraphs))}")
    print(f"표        : {len(tables)}")
    print(f"스키마검증: {'OK' if not rep.issues else rep.issues}")
    try:
        fields = d.fields.all()
        if fields:
            print(f"양식필드  : {len(fields)}개 {[getattr(f, 'name', '?') for f in fields[:10]]}")
    except Exception:
        pass
    print("\n-- 표 인덱스 (첫 행 미리보기) --")
    for i, t in enumerate(tables):
        head = " | ".join(cell_text(t, 0, c)[:20] for c in range(min(t.column_count, 4)))
        print(f"  [{i:>2}] {t.row_count}x{t.column_count}  {head}")


if __name__ == "__main__":
    sys.exit(main())
