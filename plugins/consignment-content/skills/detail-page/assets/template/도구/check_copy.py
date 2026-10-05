"""상세페이지 문구 검사: 근거 없는 효과 표현 · 남은 [대괄호] · 확인 필요 표시.

  python3 check_copy.py <상세페이지.html> [--extra 단어,단어]

확인 필요 표시(<span class="todo">) 안의 글자는 효과 표현 검사에서 뺀다.
효과 표현이 하나라도 걸리면 종료 코드 1. 대괄호·확인 필요 표시는 개수만 알려 준다(등록 전 0이어야 함).
"""
import argparse
import re
import sys
from pathlib import Path

# 상세페이지_디자인_가이드.md 6장 금지어. 상품군에 따라 --extra 로 더한다(예: 식품은 질병 이름)
WORDS = ["외풍", "차단", "절약", "절감", "난방비", "최고", "최초", "유일", "1위", "완벽", "100%", "보장",
         "방음", "소음", "냄새", "내구", "복원", "인증", "특허", "효과", "품절", "부작용"]


def visible_text(html: str) -> str:
    html = re.sub(r"<(style|script)\b.*?</\1>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", html)
    return " ".join(text.split())


def main() -> int:
    parser = argparse.ArgumentParser(description="상세페이지 문구 검사")
    parser.add_argument("html", type=Path)
    parser.add_argument("--extra", default="", help="쉼표로 구분한 추가 금지어")
    args = parser.parse_args()

    html = args.html.read_text(encoding="utf-8")
    todos = re.findall(r'<span class="todo">(.*?)</span>', html, flags=re.S)
    without_todo = re.sub(r'<span class="todo">.*?</span>', " ", html, flags=re.S)
    text = visible_text(without_todo)
    words = WORDS + [w.strip() for w in args.extra.split(",") if w.strip()]

    hits = []
    for w in words:
        for m in re.finditer(re.escape(w), text):
            hits.append(f"  {w} → …{text[max(0, m.start() - 30):m.end() + 30]}…")
    brackets = sorted(set(re.findall(r"\[[^\[\]]{1,40}\]", text)))

    print(f"효과 표현: {len(hits)}건")
    print("\n".join(hits) if hits else "  없음")
    print(f"남은 [대괄호]: {len(brackets)}종" + (f" — {', '.join(brackets[:12])}{' …' if len(brackets) > 12 else ''}" if brackets else ""))
    print(f"확인 필요 표시: {len(todos)}개")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
