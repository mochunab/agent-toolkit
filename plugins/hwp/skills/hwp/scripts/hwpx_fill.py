#!/usr/bin/env python3
"""기존 HWPX 양식에 값 주입. 원본 서식·이미지·표 구조 전부 보존.

usage:
  hwpx_fill.py spec.json            # dry-run (before→after 표시, 저장 안 함)
  hwpx_fill.py spec.json --apply    # 실제 저장

spec.json:
{
  "source": "양식.hwpx",
  "output": "작성본.hwpx",
  "labels":     {"상      호>right": "주식회사 예시", "대  표  자>right": "홍길동"},
  "cells":      [{"table": 5, "row": 1, "col": 1, "text": "주식회사 예시"}],
  "replace":    [{"find": "○○○", "with": "예시", "limit": 0}],
  "paragraphs": [{"index": 12, "text": "새 문단 내용"}]
}
- labels 권장 (좌표보다 안전). 라벨은 hwpx_read.py --labels 출력을 그대로 복사
  — 내부 공백까지 정확히. 방향: right | left | below | above, '>'로 체이닝
- limit 0 또는 생략 = 전체 치환
"""
import argparse, json, sys
from pathlib import Path
from hwpx.document import HwpxDocument


def _in_table(para, tables):
    """표 셀 안의 문단인지 — 본문 치환 중복 카운트 방지."""
    try:
        el = para.element
        for t in tables:
            for sub in t.element.iter():
                if sub is el:
                    return True
    except Exception:
        pass
    return False


def cell_text(t, r, c):
    try:
        v = t.cell(r, c)
        return (v.text or "").strip() if v is not None else ""
    except Exception:
        return "<셀 없음>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--apply", action="store_true", help="실제 저장 (없으면 dry-run)")
    a = ap.parse_args()

    spec_path = Path(a.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    def _resolve(v):
        # spec 의 상대경로는 spec 파일 위치 기준 (CWD 아님)
        if not v:
            return v
        q = Path(v)
        return str(q if q.is_absolute() else (spec_path.parent / q))

    src, out = _resolve(spec["source"]), _resolve(spec.get("output"))
    if a.apply and not out:
        print("output 경로 필요", file=sys.stderr)
        return 1

    d = HwpxDocument.open(src)
    tables = list(d.tables)
    paras = list(d.paragraphs)
    changes = 0

    for path, val in (spec.get("labels") or {}).items():
        try:
            probe = d.tables.find_cell_by_label(path.split(">")[0])
            n = probe.get("count", 0)
        except Exception:
            n = -1
        mark = "  " if n == 1 else " ⚠️"
        cur = probe["matches"][0]["target_cell"]["text"].strip()[:40] if n == 1 else "?"
        print(f"{mark} 라벨 {path!r}: 매칭 {n}건, 현재 {cur!r} → {val!r}")
        changes += 1
    if spec.get("labels") and a.apply:
        res = d.tables.fill_by_path(spec["labels"])
        for f in res.get("failed", []):
            print(f"  ❌ 라벨 실패: {f}")
        if res.get("failed_count"):
            print("라벨 채우기 실패 — 라벨 문자열을 --labels 출력과 대조하라", file=sys.stderr)
            return 1

    for c in spec.get("cells", []):
        ti, r, col = c["table"], c["row"], c["col"]
        if ti >= len(tables):
            print(f"  ⚠️ 표{ti} 없음 (총 {len(tables)}개)")
            continue
        t = tables[ti]
        before = cell_text(t, r, col)
        print(f"  표{ti} r{r}c{col}: {before!r} → {c['text']!r}")
        if a.apply:
            t.set_cell_text(r, col, c["text"])
        changes += 1

    for rp in spec.get("replace", []):
        find, to = rp["find"], rp["with"]
        # 표 셀은 d.text.replace 가 닿지 않는다 → 셀은 직접 치환
        cell_hits = []
        for ti, t in enumerate(tables):
            for r in range(t.row_count):
                for col in range(t.column_count):
                    cur = cell_text(t, r, col)
                    if find in cur:
                        cell_hits.append((ti, t, r, col, cur))
        body_hits = sum(1 for p in paras if find in (p.text or "") and not _in_table(p, tables))
        print(f"  치환 {find!r} → {to!r} : 본문 {body_hits}곳 + 표셀 {len(cell_hits)}곳")
        if a.apply:
            if body_hits:
                d.text.replace(find, to, limit=rp.get("limit") or None)
            for _ti, t, r, col, cur in cell_hits:
                t.set_cell_text(r, col, cur.replace(find, to))
        changes += body_hits + len(cell_hits)

    for pp in spec.get("paragraphs", []):
        i = pp["index"]
        if i >= len(paras):
            print(f"  ⚠️ 문단{i} 없음 (총 {len(paras)}개)")
            continue
        print(f"  문단{i}: {(paras[i].text or '')[:40]!r} → {pp['text'][:40]!r}")
        if a.apply:
            paras[i].text = pp["text"]
        changes += 1

    if not a.apply:
        print(f"\n[dry-run] {changes}건 변경 예정. 확인 후 --apply")
        return 0

    d.save_to_path(out)

    # 저장 후 자기검증 — 무손실 확인
    r = HwpxDocument.open(out)
    rep = r.validate()
    ok = (len(list(r.tables)) == len(tables) and len(list(r.paragraphs)) == len(paras) and not rep.issues)
    print(f"\n저장: {out}")
    print(f"검증: 표 {len(list(r.tables))}/{len(tables)} · 문단 {len(list(r.paragraphs))}/{len(paras)} · 스키마 {'OK' if not rep.issues else rep.issues}")
    if not ok:
        print("⚠️ 구조 불일치 — 원본과 대조 필요", file=sys.stderr)
        return 1
    # 치환 잔존 검사 — "넣었다"의 실제 증거
    resid = 0
    for rp in spec.get("replace", []):
        find = rp["find"]
        left = sum(1 for p in r.paragraphs if find in (p.text or ""))
        for t in list(r.tables):
            for rr in range(t.row_count):
                for cc in range(t.column_count):
                    if find in cell_text(t, rr, cc):
                        left += 1
        if left:
            print(f"⚠️ 치환 잔존 {find!r}: {left}곳 (limit 설정 또는 매칭 실패 확인)")
            resid += left
    if resid:
        return 1
    print(f"✅ {changes}건 반영, 무손실")
    return 0


if __name__ == "__main__":
    sys.exit(main())
