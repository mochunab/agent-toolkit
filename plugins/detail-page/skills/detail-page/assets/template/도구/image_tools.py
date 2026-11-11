"""상세페이지 사진 작업 도구.

  python3 image_tools.py split   <긴 이미지> [--step 950]
      긴 상세 이미지를 조각으로 나눠 저장. 파일명에 조각 시작 y좌표가 들어감(조각_y01900.jpg)
  python3 image_tools.py grid    <이미지> [--step 64] [--y0 0]
      좌표 격자를 그린 사본 저장(주석 위치 잡기). 조각에 그릴 때는 --y0 에 조각 시작 y좌표
  python3 image_tools.py crop    <원본> <x1> <y1> <x2> <y2> <저장 경로>
      원본 좌표로 잘라 저장
  python3 image_tools.py upscale <이미지> [--scale 2]
      확대 + 선명화 사본 저장(이름@2x.jpg)
  python3 image_tools.py sheet   <저장 경로> <이미지...>
      여러 장을 한 장에 모아 저장(잘라 낸 결과 확인용)
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def split(src: Path, step: int) -> None:
    im = Image.open(src).convert("RGB")
    out_dir = src.parent / f"{src.stem}_조각"
    out_dir.mkdir(exist_ok=True)
    for y in range(0, im.height, step):
        piece = im.crop((0, y, im.width, min(im.height, y + step)))
        path = out_dir / f"조각_y{y:05d}.jpg"
        piece.save(path, quality=92)
        print(f"{path.name}: y {y}~{min(im.height, y + step)}")


def grid(src: Path, step: int, y0: int) -> None:
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)
    for x in range(0, im.width, step):
        draw.line([(x, 0), (x, im.height)], fill=(255, 0, 0), width=1)
        draw.text((x + 2, 2), str(x), fill=(255, 0, 0))
    for y in range(0, im.height, step):
        draw.line([(0, y), (im.width, y)], fill=(0, 0, 255), width=1)
        draw.text((2, y + 2), str(y + y0), fill=(0, 0, 255))
    path = src.with_name(f"{src.stem}_격자.jpg")
    im.save(path, quality=92)
    print(path)


def crop(src: Path, box: tuple, dst: Path) -> None:
    im = Image.open(src).convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.crop(box).save(dst, quality=95)
    print(f"{dst}: {box[2] - box[0]}x{box[3] - box[1]}")


def upscale(src: Path, scale: int) -> None:
    im = Image.open(src).convert("RGB")
    big = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    path = src.with_name(f"{src.stem}@{scale}x.jpg")
    big.save(path, quality=92)
    print(f"{path}: {big.width}x{big.height}")


def sheet(dst: Path, sources: list, height: int = 600) -> None:
    ims = []
    for s in sources:
        im = Image.open(s).convert("RGB")
        ims.append(im.resize((round(im.width * height / im.height), height), Image.LANCZOS))
    canvas = Image.new("RGB", (sum(i.width for i in ims) + 12 * (len(ims) - 1), height), "white")
    draw = ImageDraw.Draw(canvas)
    x = 0
    for n, im in enumerate(ims, 1):
        canvas.paste(im, (x, 0))
        draw.rectangle([x, 0, x + 28, 22], fill=(0, 0, 0))
        draw.text((x + 6, 5), str(n), fill=(255, 255, 255))
        x += im.width + 12
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, quality=90)
    print(f"{dst}: {', '.join(f'{n}={Path(s).name}' for n, s in enumerate(sources, 1))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="상세페이지 사진 작업 도구")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("split"); p.add_argument("src", type=Path); p.add_argument("--step", type=int, default=950)
    p = sub.add_parser("grid"); p.add_argument("src", type=Path); p.add_argument("--step", type=int, default=64); p.add_argument("--y0", type=int, default=0)
    p = sub.add_parser("crop"); p.add_argument("src", type=Path); p.add_argument("box", type=int, nargs=4); p.add_argument("dst", type=Path)
    p = sub.add_parser("upscale"); p.add_argument("src", type=Path); p.add_argument("--scale", type=int, default=2)
    p = sub.add_parser("sheet"); p.add_argument("dst", type=Path); p.add_argument("sources", nargs="+")
    args = parser.parse_args()

    if args.cmd == "split":
        split(args.src, args.step)
    elif args.cmd == "grid":
        grid(args.src, args.step, args.y0)
    elif args.cmd == "crop":
        crop(args.src, tuple(args.box), args.dst)
    elif args.cmd == "upscale":
        upscale(args.src, args.scale)
    else:
        sheet(args.dst, args.sources)


if __name__ == "__main__":
    main()
