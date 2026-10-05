#!/usr/bin/env python3
"""새 상품 작업 폴더 만들기 — 상세페이지 시안(detail) / 홍보영상 소스(video).

  python3 new_product.py detail <상품명> [--root <콘텐츠 폴더>] [--template <템플릿 폴더>]
  python3 new_product.py video  <상품명> [--root <콘텐츠 폴더>] [--template <템플릿 폴더>]

만드는 위치(--root 기준, 기본은 현재 폴더):
  detail → <root>/상세페이지/상품별초안/<상품명>/상세페이지_디자인/  (+ 원본이미지/ 이미지/)
  video  → <root>/홍보영상/상품별/<상품명>/소스/

템플릿은 --template > <root>의 기존 템플릿 폴더 > 이 스킬에 들어 있는 assets/template 순서로 고른다.
이미 있는 폴더는 덮어쓰지 않고 멈춘다. 경로에 띄어쓰기가 있어도 되며, cd 없이 절대경로로 실행한다.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
KINDS = {
    "detail": dict(
        existing=("상세페이지", "디자인_템플릿"),
        dest=("상세페이지", "상품별초안", "{name}", "상세페이지_디자인"),
        extra_dirs=("원본이미지", "이미지"),
        form=("초안_양식.md", "상세페이지_초안.md"),
    ),
    "video": dict(
        existing=("홍보영상", "영상_템플릿"),
        dest=("홍보영상", "상품별", "{name}", "소스"),
        extra_dirs=(),
        form=("계획_양식.md", "홍보영상_계획.md"),
    ),
}


def pick_template(kind: str, root: Path, given: str):
    if given:
        return Path(given).expanduser().resolve()
    existing = root.joinpath(*KINDS[kind]["existing"])
    if existing.is_dir():
        return existing
    return SKILL / "assets" / "template"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=KINDS)
    ap.add_argument("name", help="상품 폴더 이름 (예: 현관문고무패킹_6.3M)")
    ap.add_argument("--root", default=".", help="콘텐츠 작업 폴더 (기본: 현재 폴더)")
    ap.add_argument("--template", default="", help="템플릿 폴더를 직접 지정")
    args = ap.parse_args()

    spec = KINDS[args.kind]
    root = Path(args.root).expanduser().resolve()
    template = pick_template(args.kind, root, args.template)
    dest = root.joinpath(*[p.format(name=args.name) for p in spec["dest"]])

    if not template.is_dir():
        print(f"템플릿 폴더가 없음: {template}", file=sys.stderr)
        return 2
    if dest.exists():
        print(f"이미 있음 — 덮어쓰지 않고 멈춤: {dest}", file=sys.stderr)
        return 2

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, dest, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "출력", "README.md"))
    for d in spec["extra_dirs"]:
        (dest / d).mkdir(exist_ok=True)
    # 템플릿에 문서 양식이 들어 있으면 상품 폴더 바로 아래로 옮긴다(이미 있으면 덮어쓰지 않음)
    form, doc = spec["form"]
    if (dest / form).is_file():
        target = dest.parent / doc
        if target.exists():
            (dest / form).unlink()
        else:
            (dest / form).replace(target)
            print(f"문서 양식: {target}")

    print(f"템플릿: {template}")
    print(f"만든 곳: {dest}")
    if args.kind == "video":
        scan = SKILL / "scripts" / "check_leftovers.py"
        if scan.is_file():
            print("\n── 템플릿에 남아 있는 이전 상품 흔적(바꿀 곳 목록) ──", flush=True)
            subprocess.run([sys.executable, str(scan), str(dest / "영상.html")], check=False)
        print("\n다음: assets/ 사진 교체 → 장면별 문구·근거 표 → timing.py 시간표 → 영상.html → render.py stills")
    else:
        print("\n다음: 원본이미지/ 에 공급처 사진 저장 → 도구/image_tools.py split·crop → 상세페이지.html 의 [대괄호] 채우기 → render.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
