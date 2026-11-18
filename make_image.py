#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a newspaper front page summing up
Wednesday 18 November 2026 in five verified stories.

Stories (each verified from a major outlet's 18 November 2026 coverage):
  1. APEC leaders' meeting opens in Shenzhen (Xi chairs; Trump arrives;
     first Xi-Trump-Putin trilateral set for Thursday).
  2. Cyclone Akvan nears India's east coast (IMD orange alert; landfall Friday).
  3. Huawei jury begins deliberations (trade-secrets criminal case, New York).
  4. UK MPs warn lax AI safety risks a 400bn-pound growth boost
     (BIST "Guardrails for growth" report, published 18 Nov 00:01).
  5. Britain "to miss climate goals" if EV sales targets are weakened
     (Climate Change Committee, said on Wednesday).

Everything is drawn by code with PIL: flat shapes, no photos, no copied art.
Deterministic: same input always renders the same PNG bytes.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1024, 1024
PAPER = (246, 241, 230)      # warm off-white newsprint
INK = (17, 17, 17)           # near-black
RED = (155, 28, 28)          # dark red accent (kickers, date)
GREY = (85, 85, 85)          # subline grey
SUB = (51, 51, 51)           # dark grey subline text
M = 28                        # side margin
CW = W - 2 * M                # content width = 968


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, start, max_w, floor=20):
    """Largest font size <= start whose rendering of text fits max_w."""
    for size in range(start, floor - 1, -1):
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
    return font(path, floor)


def star_points(cx, cy, r_out, r_in, n=5, rot_deg=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot_deg + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- pictures
def draw_apec(d, x0, y0, w, h):
    """Shenzhen skyline at dusk with three summit flags. Panel (x0,y0,w,h)."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(207, 227, 239))  # pale sky
    # sun, top right
    d.ellipse([x1 - 62, y0 + 18, x1 - 10, y0 + 70], fill=(242, 193, 78))
    # skyline (dark blue-grey towers), bases at y1
    towers = [
        (x0 + 2, y0 + 118, x0 + 62, y1),
        (x0 + 66, y0 + 78, x0 + 122, y1),
        (x0 + 126, y0 + 138, x0 + 182, y1),
        (x0 + 186, y0 + 66, x0 + 242, y1),
        (x0 + 246, y0 + 128, x0 + 302, y1),
        (x0 + 306, y0 + 96, x0 + 386, y1),
    ]
    for (bx0, by0, bx1, by1) in towers:
        d.rectangle([bx0, by0, bx1, by1], fill=(46, 74, 98))
    # tapered top on the tall tower
    d.polygon([(x0 + 198, y0 + 66), (x0 + 214, y0 + 44),
               (x0 + 230, y0 + 66)], fill=(46, 74, 98))
    # lit windows (fixed positions, deterministic)
    wins = [(x0 + 14, y0 + 140), (x0 + 34, y0 + 165), (x0 + 14, y0 + 190),
            (x0 + 80, y0 + 100), (x0 + 100, y0 + 130), (x0 + 80, y0 + 160),
            (x0 + 140, y0 + 160), (x0 + 160, y0 + 185), (x0 + 140, y0 + 205),
            (x0 + 200, y0 + 90), (x0 + 220, y0 + 120), (x0 + 200, y0 + 150),
            (x0 + 260, y0 + 150), (x0 + 280, y0 + 175), (x0 + 260, y0 + 200),
            (x0 + 320, y0 + 118), (x0 + 345, y0 + 145), (x0 + 320, y0 + 170),
            (x0 + 360, y0 + 195), (x0 + 100, y0 + 195)]
    for (wx, wy) in wins:
        d.rectangle([wx, wy, wx + 7, wy + 9], fill=(242, 193, 78))
    # dark foreground band
    d.rectangle([x0, y1 - 40, x1, y1], fill=(31, 42, 68))
    # three summit flags standing on the band: China, USA, Russia
    fw, fh = 46, 28
    fy0, fy1 = y1 - 36, y1 - 8
    fx = [x0 + 42, x0 + 171, x0 + 300]
    # China: red field, one yellow star
    d.rectangle([fx[0], fy0, fx[0] + fw, fy1], fill=(222, 41, 16))
    d.polygon(star_points(fx[0] + 12, fy0 + 13, 8, 3.4), fill=(255, 222, 0))
    # USA: stripes + blue canton
    for i in range(4):
        col = (179, 25, 34) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([fx[1], fy0 + i * 7, fx[1] + fw, fy0 + (i + 1) * 7],
                    fill=col)
    d.rectangle([fx[1], fy0, fx[1] + 19, fy0 + 14], fill=(60, 59, 110))
    # Russia: white / blue / red bands
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([fx[2], fy0 + i * 9, fx[2] + fw, fy0 + (i + 1) * 9 + 1],
                    fill=col)


def draw_cyclone(d, x0, y0, w, h):
    """Cyclone spiral over the sea, coastline below, warning triangle."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y0 + 42], fill=(223, 234, 242))   # sky
    d.rectangle([x0, y0 + 42, x1, y1], fill=(47, 111, 178))    # sea
    cx, cy = x0 + w // 2 - 50, y0 + 50
    # spiral: concentric arcs, staggered starts, white; kept inside the
    # panel (inner height is ~100px, so radius must stay <= 40)
    for r, start, end in [(40, 20, 300), (30, 140, 60), (20, 260, 180)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start, end,
              fill=(255, 255, 255), width=7)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 255),
              outline=(47, 111, 178), width=2)  # eye
    # coastline strip along the bottom
    d.polygon([(x0, y1), (x0, y1 - 16), (x0 + 120, y1 - 20),
               (x0 + 260, y1 - 14), (x0 + 380, y1 - 20), (x1, y1 - 15),
               (x1, y1)], fill=(201, 168, 106))
    # warning triangle, top right
    tx, ty = x1 - 46, y0 + 8
    d.polygon([(tx + 17, ty), (tx + 36, ty + 32), (tx, ty + 32)],
              fill=(217, 79, 4))
    f = font(SANS_BOLD, 24)
    d.text((tx + 17, ty + 18), "!", font=f, fill=(255, 255, 255),
           anchor="mm")


def draw_court(d, x0, y0, w, h):
    """A courthouse: pediment, columns, steps, door."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(232, 228, 216))
    cx = x0 + w // 2
    # pediment (triangle roof)
    d.polygon([(cx - 92, y0 + 34), (cx + 92, y0 + 34), (cx, y0 + 10)],
              fill=(107, 112, 120))
    # entablature
    d.rectangle([cx - 96, y0 + 34, cx + 96, y0 + 42], fill=(85, 90, 97))
    # four columns
    for cxx in (cx - 78, cx - 30, cx + 16, cx + 64):
        d.rectangle([cxx, y0 + 42, cxx + 14, y0 + 88], fill=(125, 131, 140))
    # door between the middle columns
    d.rectangle([cx - 8, y0 + 58, cx + 8, y0 + 88], fill=(58, 63, 70))
    # steps
    d.rectangle([cx - 100, y0 + 88, cx + 100, y0 + 96], fill=(85, 90, 97))
    d.rectangle([cx - 108, y0 + 96, cx + 108, y0 + 104], fill=(85, 90, 97))


def draw_chip(d, x0, y0, w, h):
    """A microchip with pins, overlapped by a red safety shield."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(230, 235, 242))
    cx, cy = x0 + w // 2 - 30, y0 + h // 2
    # pins
    for i in range(4):
        py = cy - 30 + i * 20
        d.rectangle([cx - 56, py, cx - 44, py + 6], fill=(185, 192, 204))
        d.rectangle([cx + 44, py, cx + 56, py + 6], fill=(185, 192, 204))
        px = cx - 30 + i * 20
        d.rectangle([px, cy - 56, px + 6, cy - 44], fill=(185, 192, 204))
        d.rectangle([px, cy + 44, px + 6, cy + 56], fill=(185, 192, 204))
    # chip body + inner die
    d.rectangle([cx - 44, cy - 44, cx + 44, cy + 44], fill=(31, 42, 68))
    d.rectangle([cx - 24, cy - 24, cx + 24, cy + 24], fill=(46, 61, 92))
    d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=(185, 192, 204))
    # red shield, bottom right of the chip
    sx, sy = cx + 62, cy + 26
    d.polygon([(sx - 26, sy - 30), (sx + 26, sy - 30), (sx + 26, sy + 4),
               (sx, sy + 32), (sx - 26, sy + 4)], fill=(155, 28, 28))
    d.line([(sx - 13, sy - 2), (sx - 3, sy + 8), (sx + 15, sy - 12)],
           fill=(255, 255, 255), width=5, joint="curve")


def draw_car(d, x0, y0, w, h):
    """An electric car with a green leaf above it."""
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0, y0, x1, y1], fill=(230, 240, 230))
    # ground line
    d.line([x0 + 20, y0 + 96, x1 - 20, y0 + 96], fill=(120, 120, 120),
           width=2)
    # cabin + windows
    d.polygon([(x0 + 160, y0 + 60), (x0 + 192, y0 + 36), (x0 + 288, y0 + 36),
               (x0 + 318, y0 + 60)], fill=(37, 107, 42))
    d.polygon([(x0 + 198, y0 + 54), (x0 + 216, y0 + 42), (x0 + 238, y0 + 42),
               (x0 + 238, y0 + 54)], fill=(191, 227, 242))
    d.polygon([(x0 + 246, y0 + 54), (x0 + 246, y0 + 42), (x0 + 272, y0 + 42),
               (x0 + 288, y0 + 54)], fill=(191, 227, 242))
    # body
    d.rounded_rectangle([x0 + 110, y0 + 58, x0 + 362, y0 + 94], radius=12,
                        fill=(46, 125, 50))
    # headlight / taillight
    d.ellipse([x0 + 348, y0 + 66, x0 + 358, y0 + 74], fill=(242, 193, 78))
    d.rectangle([x0 + 114, y0 + 66, x0 + 122, y0 + 74], fill=(179, 25, 34))
    # wheels
    for wx in (x0 + 160, x0 + 312):
        d.ellipse([wx - 15, y0 + 82, wx + 15, y0 + 112], fill=(34, 34, 34))
        d.ellipse([wx - 6, y0 + 91, wx + 6, y0 + 103], fill=(207, 212, 218))
    # green leaf above the car, right side
    lx, ly = x0 + 396, y0 + 32
    d.polygon([(lx, ly + 14), (lx + 16, ly - 10), (lx + 36, ly + 4),
               (lx + 16, ly + 20)], fill=(58, 157, 79))
    d.line([lx, ly + 14, lx - 9, ly + 23], fill=(58, 157, 79), width=3)


# ------------------------------------------------------------------- layout
def rule(d, y, width=1, x0=M, x1=W - M):
    d.line([x0, y, x1, y], fill=INK, width=width)


def grid_block(d, bx, by, kicker, headline_lines, subline, draw_pic):
    """One 472x240 story block: picture on top, kicker, 2-line headline,
    subline. Headlines are two lines: one line cannot hold a full headline
    at a legible size in a 472px column (DejaVu Serif Bold is wide)."""
    bw, bh = 472, 240
    ph = 104  # picture height
    # picture panel with border
    d.rectangle([bx, by, bx + bw, by + ph], outline=INK, width=2)
    draw_pic(d, bx + 2, by + 2, bw - 4, ph - 4)
    # kicker
    d.text((bx, by + 112), kicker, font=font(SANS_BOLD, 18), fill=RED,
           anchor="la")
    # headline, two lines, each fitted with a margin
    y = by + 134
    for ln in headline_lines:
        hf = fit(SERIF_BOLD, ln, 32, bw - 8, floor=26)
        d.text((bx, y), ln, font=hf, fill=INK, anchor="la")
        y += 32
    # subline (one line, fitted)
    sf = fit(SANS, subline, 26, bw - 8, floor=21)
    d.text((bx, by + 202), subline, font=sf, fill=SUB, anchor="la")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WORLD TODAY"
    tf = fit(SERIF_BOLD, title, 92, CW, floor=60)
    d.text((W // 2, 70), title, font=tf, fill=INK, anchor="mm")
    rule(d, 126, width=3)
    rule(d, 132, width=1)

    # ---- date, named prominently
    date = "WEDNESDAY 18 NOVEMBER 2026"
    df = fit(SANS_BOLD, date, 42, 820, floor=30)
    d.text((W // 2, 160), date, font=df, fill=RED, anchor="mm")
    d.text((W // 2, 192), "FIVE STORIES FROM ONE DAY",
           font=font(SANS, 19), fill=GREY, anchor="mm")
    rule(d, 212, width=1)

    # ---- lead story: APEC (picture left, text right)
    ly0, ly1 = 222, 478
    d.rectangle([M, ly0, M + 388, ly1], outline=INK, width=2)
    draw_apec(d, M + 2, ly0 + 2, 384, ly1 - ly0 - 4)
    tx = M + 408
    d.text((tx, 246), "DIPLOMACY", font=font(SANS_BOLD, 20), fill=RED,
           anchor="la")
    lead_head = ["APEC OPENS", "IN SHENZHEN"]
    lh = [fit(SERIF_BOLD, ln, 56, W - M - tx, floor=44) for ln in lead_head]
    d.text((tx, 274), lead_head[0], font=lh[0], fill=INK, anchor="la")
    d.text((tx, 338), lead_head[1], font=lh[1], fill=INK, anchor="la")
    d.text((tx, 410), "Xi chairs; Trump arrives.",
           font=font(SANS, 27), fill=SUB, anchor="la")
    d.text((tx, 444), "Xi-Trump-Putin talks Thursday.",
           font=font(SANS, 27), fill=SUB, anchor="la")

    # ---- divider
    rule(d, 492, width=2)

    # ---- 2x2 grid of the other four stories
    grid_block(d, M, 504, "WEATHER", ["CYCLONE AKVAN", "NEARS INDIA"],
               "Orange alert; landfall Friday.", draw_cyclone)
    grid_block(d, 524, 504, "COURTS", ["HUAWEI JURY", "DELIBERATES"],
               "Trade-secrets case in New York.", draw_court)
    grid_block(d, M, 756, "TECHNOLOGY", ["LAX AI SAFETY", "RISKS \u00a3400BN"],
               "MPs demand rules and a regulator.", draw_chip)
    grid_block(d, 524, 756, "CLIMATE", ["BRITAIN 'TO MISS'", "CLIMATE GOALS"],
               "If EV sales targets are weakened.", draw_car)

    img.save(OUT, format="PNG")
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {size} bytes, {W}x{H}")
    return size


if __name__ == "__main__":
    build()
