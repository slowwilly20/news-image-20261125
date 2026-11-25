#!/usr/bin/env python3
"""Build-time image generator for the news-image-20261125 entry.

Reads news.json (the day's verified news, with sources) and renders a
1024x1024 PNG summary. Run-time entry program is main.py (stdlib only,
copies the image the repo holds) — this script is the provenance of the
image, kept in the repo so anyone can reproduce it.

Usage: python3 generate_image.py [news.json] [entry.png]
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 48
BG = (250, 247, 242)          # warm paper
INK = (18, 18, 18)            # near-black
RED = (178, 34, 34)           # news red
GRAY = (74, 74, 74)
HAIRLINE = (200, 192, 182)
TICKER_BG = (232, 228, 221)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
BOLD_PATHS = [p for p in FONT_CANDIDATES if "Bold" in p]
REG_PATHS = [p for p in FONT_CANDIDATES if "Bold" not in p]


def font(bold, size):
    for p in (BOLD_PATHS if bold else REG_PATHS):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    news_path = sys.argv[1] if len(sys.argv) > 1 else "news.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "entry.png"
    with open(news_path, encoding="utf-8") as fh:
        data = json.load(fh)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x = MARGIN
    content_w = W - 2 * MARGIN
    y = 44

    # Kicker
    f_kick = font(True, 25)
    d.text((x, y), f"{data['kicker']}  ·  {data['day'].upper()}",
           font=f_kick, fill=RED)
    y += 46

    # Title
    f_title = font(True, 104)
    d.text((x, y), data["title"], font=f_title, fill=INK)
    y += 132

    # Rules
    d.rectangle([x, y, x + content_w, y + 4], fill=INK)
    y += 10
    d.rectangle([x, y, x + content_w, y + 2], fill=RED)
    y += 26

    # Stories — two columns, three rows (newspaper front page)
    f_tag = font(True, 21)
    f_head = font(True, 27)
    f_sum = font(False, 20)
    gutter = 28
    col_w = (content_w - gutter) // 2
    col_x = [x, x + col_w + gutter]
    row_y = y
    row_h = 0
    for i, s in enumerate(data["stories"]):
        cx = col_x[i % 2]
        cy = row_y
        d.text((cx, cy), s["tag"], font=f_tag, fill=RED)
        cy += 30
        head_lines = wrap(d, s["headline"], f_head, col_w)[:2]
        if len(wrap(d, s["headline"], f_head, col_w)) > 2:
            print(f"WARNING truncated headline: {s['tag']}")
        for line in head_lines:
            d.text((cx, cy), line, font=f_head, fill=INK)
            cy += 34
        sum_lines = wrap(d, s["summary"], f_sum, col_w)[:3]
        if len(wrap(d, s["summary"], f_sum, col_w)) > 3:
            print(f"WARNING truncated summary: {s['tag']}")
        for line in sum_lines:
            d.text((cx, cy), line, font=f_sum, fill=GRAY)
            cy += 26
        block_h = cy - row_y
        row_h = max(row_h, block_h)
        if i % 2 == 1 or i == len(data["stories"]) - 1:
            # hairline under the finished row (except the last row)
            if i < len(data["stories"]) - 2:
                d.line([x, row_y + row_h + 8, x + content_w,
                        row_y + row_h + 8], fill=HAIRLINE, width=1)
            row_y += row_h + 26
            row_h = 0
    y = row_y + 2

    # Ticker band
    tick_h = 74
    d.rectangle([x, y, x + content_w, y + tick_h], fill=TICKER_BG)
    f_tick = font(False, 22)
    ty = y + 10
    for line in wrap(d, data["ticker"], f_tick, content_w - 28)[:2]:
        d.text((x + 14, ty), line, font=f_tick, fill=INK)
        ty += 28
    y += tick_h + 18

    # Footer
    f_foot = font(False, 20)
    d.text((x, y), data["sources"], font=f_foot, fill=GRAY)
    d.text((x, y + 26), data["note"], font=f_foot, fill=GRAY)

    print(f"bottom y = {y + 52} (canvas {H})")
    assert y + 52 <= H, "layout overflow"
    img.save(out_path, "PNG", optimize=True)
    print(f"saved {out_path} {os.path.getsize(out_path)} bytes")


if __name__ == "__main__":
    main()
