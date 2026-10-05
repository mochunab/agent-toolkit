"""영상.html → 프레임 → mp4.  cd 하지 말고 절대경로로 실행.

  python3 render.py stills 0.5,1.2,3.4 <출력폴더>          # 확인용 정지 화면
  python3 render.py video <출력.mp4> [--audio a.wav] [--clean] [--frames-dir <폴더>]

화면은 시간의 순수 함수(window.renderAt(t))라서 프레임마다 같은 결과가 나온다.
브라우저 하나로 순서대로 찍는다(메모리 8GB 기준).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import timing  # noqa: E402

POSTER_T = 3.4  # 첫 화면이 다 자리 잡은 순간 → 0번 프레임·포스터


def open_page(p, clean: bool):
    browser = p.chromium.launch(channel="chrome")
    page = browser.new_page(viewport={"width": timing.W, "height": timing.H}, device_scale_factor=1)
    page.add_init_script("window.TIMING = %s;" % json.dumps(timing.payload()))
    page.goto((HERE / "영상.html").as_uri(), wait_until="networkidle")
    ok = page.evaluate(
        """async () => {
          await document.fonts.load('700 40px Gmarket'); await document.fonts.load('500 40px Gmarket');
          await document.fonts.ready;
          await Promise.all([...document.images].map(i => i.decode()));
          return [document.fonts.check('700 40px Gmarket'), document.fonts.check('500 40px Gmarket'), !!window.__ready];
        }"""
    )
    if not all(ok):
        raise SystemExit(f"글꼴·스크립트 준비 실패: {ok}")
    if clean:
        page.evaluate("document.body.classList.add('clean')")
    return browser, page


def shot(page, t: float, quality: int = 95) -> bytes:
    page.evaluate(f"window.renderAt({t})")
    return page.screenshot(type="jpeg", quality=quality)


def cmd_stills(args) -> None:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser, page = open_page(p, args.clean)
        for t in [float(x) for x in args.times.split(",")]:
            path = out / f"t{t:05.2f}.jpg"
            path.write_bytes(shot(page, t))
            print(path)
        browser.close()


def cmd_video(args) -> None:
    out = Path(args.out)
    n = int(round(timing.END * timing.FPS))
    silent = out.with_suffix(".silent.mp4")
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(timing.FPS), "-c:v", "mjpeg", "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent)],
        stdin=subprocess.PIPE,
    )
    with sync_playwright() as p:
        browser, page = open_page(p, args.clean)
        poster = shot(page, POSTER_T)
        (out.parent / "poster.jpg").write_bytes(poster)
        for i in range(n):
            ff.stdin.write(poster if i == 0 else shot(page, i / timing.FPS))
            if i % 90 == 0:
                print(f"frame {i}/{n}", flush=True)
        browser.close()
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit("ffmpeg 실패")
    if args.audio:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", args.audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             "-shortest", "-movflags", "+faststart", str(out)],
            check=True,
        )
        silent.unlink()
    else:
        silent.rename(out)
    print("done", out)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stills")
    s.add_argument("times")
    s.add_argument("out")
    s.add_argument("--clean", action="store_true")
    v = sub.add_parser("video")
    v.add_argument("out")
    v.add_argument("--audio")
    v.add_argument("--clean", action="store_true")
    args = ap.parse_args()
    {"stills": cmd_stills, "video": cmd_video}[args.cmd](args)


if __name__ == "__main__":
    main()
