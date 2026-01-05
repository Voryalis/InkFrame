#!/usr/bin/env python3
"""
InkPress — InkFrame image preparation tool for Kindle 4

Outputs:
- 600x800 PNG
- 8-bit grayscale (mode 'L')
Optional:
- --allow-resize with --resize-mode fit|crop|pad
- --autocontrast
- --shades16 (limit to 16 gray levels)
"""

import argparse
from pathlib import Path
from PIL import Image, ImageOps

KINDLE_W, KINDLE_H = 600, 800
VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def to_kindle_gray(img: Image.Image, autocontrast: bool, shades16: bool) -> Image.Image:
    g = img.convert("L")  # 8-bit grayscale
    if autocontrast:
        g = ImageOps.autocontrast(g)
    if shades16:
        g = ImageOps.posterize(g, 4)  # 16 levels
    return g


def resize_strategy(img: Image.Image, mode: str) -> Image.Image:
    if mode == "fit":
        img2 = ImageOps.contain(img, (KINDLE_W, KINDLE_H), method=Image.Resampling.LANCZOS)
        canvas = Image.new(img2.mode, (KINDLE_W, KINDLE_H), color=255)
        x = (KINDLE_W - img2.width) // 2
        y = (KINDLE_H - img2.height) // 2
        canvas.paste(img2, (x, y))
        return canvas

    if mode == "crop":
        return ImageOps.fit(img, (KINDLE_W, KINDLE_H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    if mode == "pad":
        canvas = Image.new(img.mode, (KINDLE_W, KINDLE_H), color=255)
        x = (KINDLE_W - img.width) // 2
        y = (KINDLE_H - img.height) // 2
        canvas.paste(img, (x, y))
        return canvas

    raise ValueError(f"Unknown resize mode: {mode}")


def collect_images(inputs):
    files = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            files.extend([f for f in p.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXTS])
        else:
            files.append(p)
    # de-dup while preserving order
    seen = set()
    out = []
    for f in files:
        fp = str(f.resolve())
        if fp not in seen:
            seen.add(fp)
            out.append(f)
    return out


def main():
    ap = argparse.ArgumentParser(description="InkPress: convert images to Kindle 4 (600x800, grayscale PNG).")
    ap.add_argument("inputs", nargs="+", help="One or more image files OR directories")
    ap.add_argument("-o", "--output", help="Output directory (default: alongside each input)")
    ap.add_argument("--allow-resize", action="store_true",
                    help="Allow resizing/cropping/padding if input isn't 600x800 (otherwise skip).")
    ap.add_argument("--resize-mode", choices=["fit", "crop", "pad"], default="fit",
                    help="When resizing is allowed: how to reach 600x800 (default: fit).")
    ap.add_argument("--autocontrast", action="store_true", help="Apply autocontrast after grayscale conversion.")
    ap.add_argument("--shades16", action="store_true", help="Reduce to 16 gray shades.")
    args = ap.parse_args()

    images = collect_images(args.inputs)
    if not images:
        raise SystemExit("No image files found in given inputs.")

    out_dir = Path(args.output) if args.output else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0

    for inp in images:
        if not inp.exists():
            print(f"✖ Missing: {inp}")
            skipped += 1
            continue

        out_path = (out_dir / f"{inp.stem}_k4.png") if out_dir else inp.with_name(inp.stem + "_k4.png")

        try:
            with Image.open(inp) as img:
                img.load()

                if (img.width, img.height) != (KINDLE_W, KINDLE_H):
                    if not args.allow_resize:
                        print(f"↷ Skipped (wrong size {img.width}x{img.height}): {inp.name}")
                        skipped += 1
                        continue
                    img = resize_strategy(img, args.resize_mode)

                g = to_kindle_gray(img, autocontrast=args.autocontrast, shades16=args.shades16)
                g.save(out_path, format="PNG", optimize=True)

            print(f"✔ {inp.name} → {out_path}")
            converted += 1

        except Exception as e:
            print(f"✖ Failed: {inp.name} ({e})")
            skipped += 1

    print(f"\nDone. Converted: {converted} | Skipped/Failed: {skipped}")


if __name__ == "__main__":
    main()
