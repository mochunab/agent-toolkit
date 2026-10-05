"""상세페이지.html → 출력/ 섹션별 PNG + 전체 미리보기.

실행: python3 "<이 파일의 절대경로>"
(Google Drive 폴더로 cd 한 뒤 && 로 이어 실행하면 출력 없이 실패한 적이 있어 절대경로로 실행한다)
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SRC = HERE / "상세페이지.html"
OUT = HERE / "출력"
WIDTH = 860  # 스마트스토어 상세 권장 폭


def main() -> None:
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": WIDTH, "height": 1200}, device_scale_factor=1)
        page.goto(SRC.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")

        sections = page.locator("section.slice")
        for i in range(sections.count()):
            sec = sections.nth(i)
            name = sec.get_attribute("id") or f"s{i + 1:02d}"
            path = OUT / f"{name}.png"
            sec.screenshot(path=str(path))
            box = sec.bounding_box()
            print(f"{path.name}: {WIDTH}x{round(box['height'])}")

        page.screenshot(path=str(OUT / "00_전체_미리보기.png"), full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
