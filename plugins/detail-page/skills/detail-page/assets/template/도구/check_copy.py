"""상세페이지 문구 검사: 근거 없는 효과 표현 · 남은 [대괄호] · 확인 필요 표시.

  python3 check_copy.py <상세페이지.html> [--extra 단어,단어] [--allow 단어,단어]

기본 금지어는 상품군에 상관없이 근거 없이 쓰기 쉬운 최상급·보장·효과 표현이다.
상품군 표현은 --extra 로 더한다(예: 문·창호 외풍,난방비,방음 / 식품 질병 이름 / 화장품 치료,재생).
인증서·시험성적서처럼 근거 자료가 있는 단어만 --allow 로 뺀다(근거 위치는 초안에 적는다).
확인 필요 표시(<span class="todo">) 안의 글자는 효과 표현 검사에서 뺀다.
효과 표현이 하나라도 걸리면 종료 코드 1. 대괄호·확인 필요 표시는 개수만 알려 준다(등록 전 0이어야 함).
이 검사는 광고 심의·표시 의무·법률 판단을 대신하지 않는다.
"""
import argparse
import re
import sys
from pathlib import Path

# 디자인 가이드 3장 '쓰지 않는 것' 기준의 기본 금지어
WORDS = ["최고", "최초", "유일", "1위", "완벽", "100%", "보장", "효과", "효능", "부작용", "인증", "특허",
         "품절", "차단", "절약", "절감", "소음", "냄새", "내구"]


def visible_text(html: str) -> str:
    html = re.sub(r"<(style|script)\b.*?</\1>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", html)
    return " ".join(text.split())


def split_words(value: str) -> list:
    return [w.strip() for w in value.split(",") if w.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="상세페이지 문구 검사")
    parser.add_argument("html", type=Path)
    parser.add_argument("--extra", default="", help="쉼표로 구분한 추가 금지어")
    parser.add_argument("--allow", default="", help="근거 자료가 있어 검사에서 뺄 단어(쉼표로 구분)")
    args = parser.parse_args()

    html = args.html.read_text(encoding="utf-8")
    todos = re.findall(r'<span class="todo">(.*?)</span>', html, flags=re.S)
    without_todo = re.sub(r'<span class="todo">.*?</span>', " ", html, flags=re.S)
    text = visible_text(without_todo)
    allow = set(split_words(args.allow))
    words = [w for w in dict.fromkeys(WORDS + split_words(args.extra)) if w not in allow]

    hits = []
    for w in words:
        for m in re.finditer(re.escape(w), text):
            hits.append(f"  {w} → …{text[max(0, m.start() - 30):m.end() + 30]}…")
    brackets = sorted(set(re.findall(r"\[[^\[\]]{1,40}\]", text)))

    print(f"효과 표현: {len(hits)}건")
    print("\n".join(hits) if hits else "  없음")
    if allow:
        print(f"검사에서 뺀 단어(근거 확인 필요): {', '.join(sorted(allow))}")
    print(f"남은 [대괄호]: {len(brackets)}종" + (f" — {', '.join(brackets[:12])}{' …' if len(brackets) > 12 else ''}" if brackets else ""))
    print(f"확인 필요 표시: {len(todos)}개")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
