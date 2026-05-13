#!/usr/bin/env python3
"""
Generate a 1400x1400 podcast cover image — black background, white text,
SF-style heavy/light pairing. Apple Podcasts spec is 1400–3000 px square,
JPG or PNG, RGB.

Usage:  python3 scripts/make-cover.py
Output: cover.jpg in repo root
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "cover.jpg"
SIZE = 1400
BG = (10, 10, 14)              # near-black
ACCENT = (220, 80, 50)          # warm red dot
TITLE = "Morning"
TITLE2 = "Brief"
SUBTITLE = "geopolitics · economy · ai · arts"

def best_font(name_candidates, size):
    for name in name_candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def main():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    title_font = best_font([
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ], 360)
    subtitle_font = best_font([
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ], 44)

    def text_size(text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    t1_w, t1_h = text_size(TITLE, title_font)
    t2_w, t2_h = text_size(TITLE2, title_font)
    sub_w, sub_h = text_size(SUBTITLE, subtitle_font)

    block_h = t1_h + t2_h + 40 + sub_h + 80
    y0 = (SIZE - block_h) // 2

    draw.text(((SIZE - t1_w) / 2, y0), TITLE, font=title_font, fill=(245, 245, 240))
    draw.text(((SIZE - t2_w) / 2, y0 + t1_h + 20), TITLE2, font=title_font, fill=(245, 245, 240))

    # accent dot
    dot_r = 18
    dot_x = SIZE / 2
    dot_y = y0 + t1_h + 20 + t2_h + 70
    draw.ellipse(
        (dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r),
        fill=ACCENT,
    )

    draw.text(((SIZE - sub_w) / 2, dot_y + dot_r + 30), SUBTITLE, font=subtitle_font, fill=(160, 160, 165))

    img.save(OUT, "JPEG", quality=92, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
