"""상세페이지.html → 출력/ 섹션별 PNG + 전체 미리보기.

  python3 "<이 파일의 절대경로>" [--width 860]

디자인은 가로 860px 기준으로 짠다(스마트스토어 상세 권장 폭). --width 를 주면 레이아웃은 그대로 두고
이미지만 그 폭에 맞춰 비율대로 확대·축소해 저장한다. 채널마다 권장 폭이 다르면 그 채널 판매자 안내를 확인한다.
cd 한 뒤 && 로 이어 실행하면 동기화 폴더에서 출력 없이 실패한 적이 있어 절대경로로 실행한다.
"""
import argparse
import struct
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SRC = HERE / "상세페이지.html"
OUT = HERE / "출력"
DESIGN_WIDTH = 860  # style.css 의 body 폭과 같아야 한다


def png_size(data: bytes) -> tuple:
    return struct.unpack(">II", data[16:24])


def main() -> None:
    ap = argparse.ArgumentParser(description="상세페이지 섹션별 PNG 저장")
    ap.add_argument("--width", type=int, default=DESIGN_WIDTH, help=f"저장할 이미지 가로 폭(px). 기본 {DESIGN_WIDTH}")
    args = ap.parse_args()
    if not 200 <= args.width <= 3000:
        ap.error("--width 는 200~3000 사이")

    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": DESIGN_WIDTH, "height": 1200},
                                device_scale_factor=args.width / DESIGN_WIDTH)
        page.goto(SRC.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")

        sections = page.locator("section.slice")
        for i in range(sections.count()):
            sec = sections.nth(i)
            name = sec.get_attribute("id") or f"s{i + 1:02d}"
            path = OUT / f"{name}.png"
            w, h = png_size(sec.screenshot(path=str(path)))
            print(f"{path.name}: {w}x{h}")

        page.screenshot(path=str(OUT / "00_전체_미리보기.png"), full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
