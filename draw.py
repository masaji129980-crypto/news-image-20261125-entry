#!/usr/bin/env python3
"""Build-time script: draws the 25 November 2026 world-news front page.

Run once here to produce entry.png. The grader never runs this file:
main.py (stdlib only) simply copies the committed entry.png to /output.
All artwork is drawn in code with Pillow; no downloaded images.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (164, 30, 34)
BLUE = (30, 58, 95)
GREY = (110, 105, 95)
LIGHT = (232, 226, 214)
SKY = (183, 205, 224)
SEA = (46, 88, 130)
DARKSEA = (28, 60, 92)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit a pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, text, size=17):
    f = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + size + 6


def headline(draw, x, y, text, size, width, fill=INK, leading=None):
    f = font(SERIF_B, size)
    leading = leading or int(size * 1.08)
    yy = y
    for line in wrap(draw, text, f, width):
        draw.text((x, yy), line, font=f, fill=fill)
        yy += leading
    return yy


def draw_ship_scene(d, x0, y0, x1, y1):
    """Gulf of Finland: grey sea, cargo ship, drone above, blast plume."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.rectangle([x0, y0 + (y1 - y0) * 0.62, x1, y1], fill=SEA)
    # waves
    for i, wx in enumerate(range(x0 + 8, x1 - 8, 46)):
        wy = y0 + (y1 - y0) * 0.62 + 26 + (i % 3) * 14
        d.arc([wx, wy, wx + 34, wy + 12], 180, 360, fill=(210, 225, 238), width=3)
    # ship hull
    hx0, hx1 = x0 + 52, x1 - 70
    hy = y0 + (y1 - y0) * 0.70
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - 26, hy + 34), (hx0 + 18, hy + 34)],
              fill=(52, 52, 58))
    d.rectangle([hx0 + 60, hy - 34, hx0 + 150, hy], fill=(120, 40, 36))
    d.rectangle([hx0 + 170, hy - 22, hx0 + 205, hy], fill=(200, 200, 200))
    d.rectangle([hx0 + 186, hy - 52, hx0 + 194, hy - 22], fill=(60, 60, 60))
    # containers
    for i, cx in enumerate(range(hx0 + 8, hx0 + 58, 26)):
        d.rectangle([cx, hy - 16, cx + 22, hy - 2],
                    fill=[(196, 120, 40), (60, 110, 70)][i % 2])
    # explosion plume at the bow
    ex, ey = hx1 - 8, hy - 6
    for r, col in [(46, (255, 170, 60)), (34, (255, 110, 40)), (20, (120, 40, 30))]:
        d.ellipse([ex - r, ey - r - 18, ex + r, ey + r - 18], fill=col)
    # smoke
    for sx, sy, sr in [(ex - 40, ey - 70, 16), (ex - 18, ey - 88, 20),
                       (ex + 8, ey - 78, 15)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 92))
    # drone
    dx, dy = x0 + 150, y0 + 34
    d.ellipse([dx - 22, dy - 6, dx - 6, dy + 6], outline=INK, width=3)
    d.ellipse([dx + 6, dy - 6, dx + 22, dy + 6], outline=INK, width=3)
    d.rectangle([dx - 12, dy - 3, dx + 12, dy + 3], fill=INK)
    d.line([(dx, dy + 3), (dx + 34, dy + 26)], fill=INK, width=2)
    d.line([(dx + 34, dy + 26), (dx + 44, dy + 34)], fill=RED, width=3)
    d.text((x0 + 10, y1 - 26), "GULF OF FINLAND  •  DRONE STRIKE AT SEA",
           font=font(SANS_B, 14), fill=(255, 255, 255))


def draw_tower_scene(d, x0, y0, x1, y1):
    """Riyadh: night sky, tall tower, smoke and sparks from a drone hit."""
    d.rectangle([x0, y0, x1, y1], fill=(24, 28, 44))
    # stars
    for sx, sy in [(x0 + 20, y0 + 16), (x0 + 90, y0 + 30), (x1 - 30, y0 + 14),
                   (x1 - 90, y0 + 44), (x0 + 150, y0 + 12)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # skyline
    for bx, bw, bh in [(x0 + 8, 34, 60), (x0 + 48, 26, 44), (x1 - 78, 40, 74),
                       (x1 - 32, 24, 50)]:
        d.rectangle([bx, y1 - bh, bx + bw, y1], fill=(48, 54, 74))
    # tower
    tx = (x0 + x1) // 2
    d.polygon([(tx - 34, y1), (tx - 16, y0 + 26), (tx + 16, y0 + 26),
               (tx + 34, y1)], fill=(150, 160, 190))
    for wy in range(y0 + 40, y1 - 12, 18):
        d.line([(tx - 26, wy), (tx + 26, wy)], fill=(200, 205, 220), width=2)
    # blast at tower top
    bx, by = tx + 6, y0 + 34
    for r, col in [(30, (255, 180, 70)), (20, (255, 120, 50)), (11, (255, 240, 180))]:
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for sx, sy in [(bx - 34, by + 26), (bx + 30, by + 40), (bx - 8, by + 52)]:
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 200, 90))
    # smoke drifting
    d.ellipse([bx - 46, by - 34, bx - 6, by - 6], fill=(120, 120, 128))
    d.ellipse([bx - 20, by - 48, bx + 22, by - 18], fill=(150, 150, 158))
    d.text((x0 + 10, y1 - 26), "RIYADH  •  DRONE HITS TOWER",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def draw_gavel(d, x0, y0, x1, y1):
    """Courtroom: gavel resting horizontally above its sound block."""
    d.rectangle([x0, y0, x1, y1], fill=(238, 228, 205))
    d.rectangle([x0, y1 - 30, x1, y1], fill=(122, 82, 52))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 12
    # handle
    d.line([(cx - 78, cy), (cx + 34, cy)], fill=(90, 58, 32), width=10)
    d.ellipse([cx - 82, cy - 5, cx - 72, cy + 5], fill=(70, 44, 24))
    # head (two blocks either side of the handle end)
    d.rectangle([cx + 34, cy - 26, cx + 72, cy - 4], fill=(70, 44, 24))
    d.rectangle([cx + 34, cy + 4, cx + 72, cy + 26], fill=(70, 44, 24))
    # sound block
    d.ellipse([cx - 46, cy + 32, cx + 6, cy + 54], fill=(150, 110, 66))
    d.ellipse([cx - 36, cy + 36, cx - 4, cy + 50], fill=(178, 138, 90))


def draw_medal(d, x0, y0, x1, y1):
    """Medal of Freedom: ribbon and gold star medal."""
    d.rectangle([x0, y0, x1, y1], fill=(226, 234, 244))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 12
    d.polygon([(cx - 34, y0 + 10), (cx - 8, y0 + 10), (cx, cy - 46),
               (cx + 8, y0 + 10), (cx + 34, y0 + 10), (cx + 18, cy - 34),
               (cx, cy - 46), (cx - 18, cy - 34)], fill=(196, 40, 48))
    d.polygon([(cx - 34, y0 + 10), (cx - 8, y0 + 10), (cx, cy - 46),
               (cx - 18, cy - 34)], fill=(150, 26, 34))
    # star
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = 52 if i % 2 == 0 else 22
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(212, 160, 40), outline=(150, 110, 20))
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(240, 200, 90),
              outline=(150, 110, 20))


def draw_shield(d, x0, y0, x1, y1):
    """Cyber breach: shield with a crack and warning bars."""
    d.rectangle([x0, y0, x1, y1], fill=(222, 228, 236))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    d.polygon([(cx - 52, cy - 44), (cx + 52, cy - 44), (cx + 52, cy + 4),
               (cx, cy + 46), (cx - 52, cy + 4)], fill=BLUE,
              outline=(18, 36, 60))
    d.polygon([(cx - 38, cy - 32), (cx + 38, cy - 32), (cx + 38, cy + 2),
               (cx, cy + 34), (cx - 38, cy + 2)], fill=(70, 110, 160))
    # crack
    d.line([(cx + 5, cy - 32), (cx - 7, cy - 7), (cx + 8, cy + 8),
            (cx - 3, cy + 32)], fill=(255, 255, 255), width=4)
    d.text((cx - 11, cy - 18), "!", font=font(SANS_B, 36), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---------- Masthead ----------
    d.text((M, 22), "THE WORLD", font=font(SERIF_B, 92), fill=INK)
    d.text((M, 118), "ONE DAY  •  ONE PAGE  •  ALL THE NEWS",
           font=font(SANS_B, 19), fill=RED)
    d.text((W - M - 250, 30), "No. 329", font=font(SANS, 18), fill=GREY)
    d.text((W - M - 250, 56), "Price: free", font=font(SANS, 18), fill=GREY)
    rule(d, M, 152, W - M, 4)
    rule(d, M, 160, W - M, 1)

    # ---------- Date line ----------
    d.text((M, 172), "WEDNESDAY, 25 NOVEMBER 2026",
           font=font(SERIF_B, 34), fill=INK)
    d.text((M, 214), "The day's world news, summed up in one picture.",
           font=font(SANS, 20), fill=GREY)
    rule(d, M, 246, W - M, 2)

    # ---------- Lead story: Ukraine strikes Russian ships ----------
    y = 262
    y = kicker(d, M, y, "Lead story — Ukraine • Russia")
    y = headline(d, M, y, "Kyiv confirms drone strikes on Russian ships", 40, 620)
    y = para(d, (M, y + 4),
             "President Zelenskyy says Ukraine hit a Russian cargo ship in the "
             "Gulf of Finland and sank a Russian warship off Libya. Norway urges caution.",
             font(SANS, 19), 620)
    draw_ship_scene(d, M, 452, M + 620, 700)

    # ---------- Right column: Riyadh ----------
    rx = M + 652
    y2 = 262
    y2 = kicker(d, rx, y2, "Middle East")
    y2 = headline(d, rx, y2, "Houthi drone hits Riyadh's tallest tower", 30, 300)
    y2 = para(d, (rx, y2 + 4),
              "Eleven people are wounded in the strike on the Saudi capital.",
              font(SANS, 18), 300)
    draw_tower_scene(d, rx, 452, W - M, 700)

    rule(d, M, 716, W - M, 2)

    # ---------- Second row: three short stories ----------
    col_w, gap = 300, 16
    y3 = 732
    # Huawei
    x = M
    y3a = kicker(d, x, y3, "United States • China")
    y3a = headline(d, x, y3a, "Huawei convicted in US trial", 24, col_w)
    y3a = para(d, (x, y3a + 2),
               "A US jury finds the Chinese telecoms giant guilty over its Iran business.",
               font(SANS, 16), col_w)
    draw_gavel(d, x, 880, x + col_w, 968)
    # Giuliani
    x = M + col_w + gap
    y3b = kicker(d, x, y3, "Washington")
    y3b = headline(d, x, y3b, "Trump gives Giuliani Medal of Freedom", 24, col_w)
    y3b = para(d, (x, y3b + 2),
               "The former New York mayor receives the highest US civilian honour.",
               font(SANS, 16), col_w)
    draw_medal(d, x, 880, x + col_w, 968)
    # CIA breach
    x = M + 2 * (col_w + gap)
    y3c = kicker(d, x, y3, "Washington • Cyber")
    y3c = headline(d, x, y3c, "CIA and spy chief's office hit by cyber breach", 24, col_w)
    y3c = para(d, (x, y3c + 2),
               "Unclassified information is caught up in the breach, US officials say.",
               font(SANS, 16), col_w)
    draw_shield(d, x, 880, x + col_w, 968)

    # ---------- Bottom briefs strip ----------
    rule(d, M, 984, W - M, 2)
    strip = ("ALSO TODAY:  NATO planes to Poland  •  "
             "Tankers mined in Hormuz  •  "
             "England beat Australia")
    d.text((M, 992), strip, font=font(SANS_B, 14), fill=INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
