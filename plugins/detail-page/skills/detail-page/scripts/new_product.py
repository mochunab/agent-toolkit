#!/usr/bin/env python3
"""새 상품 상세페이지 작업 폴더 만들기.

  python3 new_product.py detail <상품명> [--root <작업폴더>] [--template <템플릿 폴더>]

만드는 것(--root 기준, 기본은 현재 폴더):
  <root>/상세페이지/상품별초안/<상품명>/상세페이지_디자인/   템플릿 복사본 + 원본이미지/ 이미지/
  <root>/상세페이지/상품별초안/<상품명>/상세페이지_초안.md   초안 양식
  <root>/상세페이지/결정기록.md                             결정 기록 양식(없을 때만)

템플릿은 --template > <root>/상세페이지/디자인_템플릿/(직접 고친 템플릿) > 이 스킬의 assets/template 순서로 고른다.
이미 있는 상품 폴더는 덮어쓰지 않고 멈춘다. 경로에 띄어쓰기가 있어도 되며, cd 없이 절대경로로 실행한다.
"""
import argparse
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
FORM, DRAFT = "초안_양식.md", "상세페이지_초안.md"
LOG_TEMPLATE = SKILL / "references" / "decision-log-template.md"


def pick_template(root: Path, given: str) -> Path:
    if given:
        return Path(given).expanduser().resolve()
    custom = root / "상세페이지" / "디자인_템플릿"
    if custom.is_dir():
        return custom
    return SKILL / "assets" / "template"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["detail"], help="항상 detail")
    ap.add_argument("name", help="상품 폴더 이름 (예: 현관문고무패킹_6.3M)")
    ap.add_argument("--root", default=".", help="콘텐츠 작업 폴더 (기본: 현재 폴더)")
    ap.add_argument("--template", default="", help="템플릿 폴더를 직접 지정")
    args = ap.parse_args()

    name = args.name.strip()
    if not name or name in {".", ".."} or "/" in name or "\\" in name:
        print(f"상품명에 경로 문자를 쓸 수 없음: {args.name!r}", file=sys.stderr)
        return 2

    root = Path(args.root).expanduser().resolve()
    template = pick_template(root, args.template)
    product = root / "상세페이지" / "상품별초안" / name
    dest = product / "상세페이지_디자인"

    if not template.is_dir():
        print(f"템플릿 폴더가 없음: {template}", file=sys.stderr)
        return 2
    if dest.exists():
        print(f"이미 있음 — 덮어쓰지 않고 멈춤: {dest}", file=sys.stderr)
        return 2

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, dest, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "출력", "README.md"))
    for d in ("원본이미지", "이미지"):
        (dest / d).mkdir(exist_ok=True)

    # 초안 양식은 상품 폴더 바로 아래로 옮긴다(이미 있으면 덮어쓰지 않음)
    if (dest / FORM).is_file():
        target = product / DRAFT
        if target.exists():
            (dest / FORM).unlink()
        else:
            (dest / FORM).replace(target)
            print(f"초안 양식: {target}")

    log = root / "상세페이지" / "결정기록.md"
    if not log.exists() and LOG_TEMPLATE.is_file():
        shutil.copyfile(LOG_TEMPLATE, log)
        print(f"결정 기록 양식: {log}")

    print(f"템플릿: {template}")
    print(f"만든 곳: {dest}")
    print("\n다음: 초안 md 결정 네 줄·증거 단계 채우기 → 원본이미지/ 에 사진 저장 → 도구/image_tools.py split·crop"
          " → 상세페이지.html 의 [대괄호] 채우기 → render.py → 도구/check_copy.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
