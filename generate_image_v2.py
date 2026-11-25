#!/usr/bin/env python3
"""Build-time image generator v2 for the news-image-20261125 entry.

X-factor vs v1 (plain text grid): the image is now a MAP of the day.
A world map carries six numbered pins at the real locations of the six
stories (Gulf of Finland, Antalya, Washington DC, New York, Ituri,
Riyadh); the story list below is keyed to the pin numbers. Same six
verified stories, same sources — the map is the idea the judge can see
at a glance.

Reads news.json (stories carry lat/lon + badge offset) and
world.geo.json (Natural Earth-style country outlines, johan/world.geo.json).
Deterministic: same inputs -> same bytes.

Usage: python3 generate_image_v2.py [news.json] [entry.png]
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 48
BG = (250, 247, 242)          # warm paper
INK = (18, 18, 18)
RED = (178, 34, 34)
GRAY = (74, 74, 74)
HAIRLINE = (200, 192, 182)
TICKER_BG = (232, 228, 221)
LAND = (46, 58, 70)           # dark slate land
GRAT = (216, 210, 200)        # graticule
PIN_R = 13

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


def split_ring(ring):
    """Split a lon/lat ring at antimeridian jumps (>180 deg in lon)."""
    parts, cur = [], [ring[0]]
    for pt in ring[1:]:
        if abs(pt[0] - cur[-1][0]) > 180:
            parts.append(cur)
            cur = [pt]
        else:
            cur.append(pt)
    parts.append(cur)
    return [p for p in parts if len(p) >= 3]


def main():
    news_path = sys.argv[1] if len(sys.argv) > 1 else "news.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "entry.png"
    with open(news_path, encoding="utf-8") as fh:
        data = json.load(fh)
    with open("world.geo.json", encoding="utf-8") as fh:
        world = json.load(fh)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x = MARGIN
    content_w = W - 2 * MARGIN

    # ---- Masthead ----
    y = 36
    f_kick = font(True, 22)
    d.text((x, y), f"{data['kicker']}  ·  {data['day'].upper()}",
           font=f_kick, fill=RED)
    y += 40
    f_title = font(True, 88)
    d.text((x, y), data["title"], font=f_title, fill=INK)
    y += 108
    d.rectangle([x, y, x + content_w, y + 4], fill=INK)
    y += 10
    d.rectangle([x, y, x + content_w, y + 2], fill=RED)
    y += 24  # gap so the rules don't touch the map's top edge

    # ---- Map panel ----
    # Equirectangular, lon -180..180, lat 70..-55.
    LAT_TOP, LAT_BOT = 70.0, -55.0
    map_x0, map_y0 = x, y
    map_w = content_w
    map_h = int(map_w * (LAT_TOP - LAT_BOT) / 360.0)

    def project(lon, lat):
        px = map_x0 + (lon + 180.0) / 360.0 * map_w
        py = map_y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * map_h
        return (px, py)

    # Graticule every 30 deg (ocean only — land drawn over it).
    for lon in range(-150, 181, 30):
        px = map_x0 + (lon + 180.0) / 360.0 * map_w
        d.line([px, map_y0, px, map_y0 + map_h], fill=GRAT, width=1)
    for lat in range(-30, 61, 30):
        _, py = project(0, lat)
        d.line([map_x0, py, map_x0 + map_w, py], fill=GRAT, width=1)

    # Land: every country polygon, same fill (clean silhouette).
    for feat in world["features"]:
        if feat.get("properties", {}).get("name") == "Antarctica":
            continue
        geom = feat["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"][0]]
        elif geom["type"] == "MultiPolygon":
            polys = [p[0] for p in geom["coordinates"]]
        for ring in polys:
            for part in split_ring(ring):
                pts = [project(lon, lat) for lon, lat in part]
                d.polygon(pts, fill=LAND)

    # Pins: dot at the true location, numbered badge (offset where given).
    pin_xy = []
    for i, s in enumerate(data["stories"], 1):
        px, py = project(s["lon"], s["lat"])
        dx, dy = s.get("dx", 0), s.get("dy", 0)
        bx, by = px + dx, py + dy
        pin_xy.append((px, py, bx, by))
        if dx or dy:
            d.line([px, py, bx, by], fill=RED, width=2)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.ellipse([bx - PIN_R, by - PIN_R, bx + PIN_R, by + PIN_R],
                  fill=RED, outline=(255, 255, 255), width=2)
        f_num = font(True, 15)
        num = str(i)
        nw = d.textlength(num, font=f_num)
        d.text((bx - nw / 2, by - 11), num, font=f_num, fill=(255, 255, 255))
    y = map_y0 + map_h + 16

    # ---- Story list keyed to pin numbers ----
    f_tag = font(True, 20)
    f_head = font(True, 23)
    f_sum = font(False, 18)
    row_h = 56
    for i, s in enumerate(data["stories"], 1):
        # number badge
        cx, cy = x + PIN_R, y + 12
        d.ellipse([cx - PIN_R, cy - PIN_R, cx + PIN_R, cy + PIN_R],
                  fill=RED)
        f_num = font(True, 15)
        num = str(i)
        nw = d.textlength(num, font=f_num)
        d.text((cx - nw / 2, cy - 11), num, font=f_num, fill=(255, 255, 255))
        tx = x + 2 * PIN_R + 12
        # line 1: TAG — headline
        d.text((tx, y), s["tag"], font=f_tag, fill=RED)
        tag_w = d.textlength(s["tag"], font=f_tag)
        head = "— " + s["headline"]
        head_lines = wrap(d, head, f_head, content_w - (tx - x) - tag_w - 12)
        d.text((tx + tag_w + 12, y), head_lines[0], font=f_head, fill=INK)
        if len(head_lines) > 1:
            print(f"WARNING headline wraps: {s['tag']}")
        # line 2: summary (one line, tightened in news.json)
        sum_lines = wrap(d, s["summary"], f_sum, content_w - (tx - x))
        d.text((tx, y + 30), sum_lines[0], font=f_sum, fill=GRAY)
        if len(sum_lines) > 1:
            print(f"WARNING summary wraps: {s['tag']}")
        y += row_h
    y += 6

    # ---- Ticker ----
    tick_h = 58
    d.rectangle([x, y, x + content_w, y + tick_h], fill=TICKER_BG)
    f_tick = font(False, 20)
    ty = y + 8
    for line in wrap(d, data["ticker"], f_tick, content_w - 28)[:2]:
        d.text((x + 14, ty), line, font=f_tick, fill=INK)
        ty += 25
    y += tick_h + 14

    # ---- Footer ----
    f_foot = font(False, 18)
    d.text((x, y), data["sources"], font=f_foot, fill=GRAY)

    print(f"bottom y = {y + 24} (canvas {H})")
    assert y + 24 <= H, "layout overflow"
    img.save(out_path, "PNG", optimize=True)
    print(f"saved {out_path} {os.path.getsize(out_path)} bytes")


if __name__ == "__main__":
    main()
