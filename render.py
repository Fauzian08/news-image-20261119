#!/usr/bin/env python3
"""Render the front page for Thursday 19 November 2026 as entry.png.

Editorial poster, 1024x1024, drawn with PIL only so every word is crisp.
Run:  python3 render.py   (writes entry.png next to this script)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (251, 248, 241)
INK = (20, 20, 20)
RED = (166, 27, 27)
BLUE = (29, 78, 137)
TEAL = (13, 110, 110)
AMBER = (140, 88, 16)
GREEN = (46, 110, 60)
GRAY = (96, 94, 88)
LIGHT_RULE = (205, 200, 190)
SKYLINE = (43, 58, 74)
BAND = (24, 24, 24)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def center(draw, text, fnt, y, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y


def skyline(draw, x0, y0, x1, y1):
    """Simple Shenzhen-style tower silhouette."""
    draw.rectangle([x0, y0, x1, y1], fill=PAPER)
    # deterministic pseudo-random heights
    heights = [0.55, 0.72, 0.48, 0.9, 0.62, 1.0, 0.58, 0.78, 0.5, 0.85,
               0.66, 0.95, 0.6, 0.74, 0.52, 0.88, 0.64, 0.7, 0.58, 0.8]
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx0 = x0 + i * bw + 2
        bx1 = x0 + (i + 1) * bw - 2
        top = y1 - h * (y1 - y0)
        draw.rectangle([bx0, top, bx1, y1], fill=SKYLINE)
        # antenna on the tallest tower
        if h == 1.0:
            draw.line([ (bx0 + bx1) / 2, top - 14, (bx0 + bx1) / 2, top],
                      fill=SKYLINE, width=3)
            draw.ellipse([(bx0 + bx1) / 2 - 3, top - 18, (bx0 + bx1) / 2 + 3,
                          top - 12], fill=RED)
        # a few lit windows
        for wy in range(int(top) + 10, y1 - 8, 16):
            for wx in range(int(bx0) + 6, int(bx1) - 4, 12):
                if (wx * 7 + wy * 13) % 11 < 3:
                    draw.rectangle([wx, wy, wx + 4, wy + 5],
                                   fill=(232, 196, 106))
    draw.line([x0, y1, x1, y1], fill=RED, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    y = 26
    center(d, "THE WORLD TODAY", SERIF_B(58), y, INK)
    y = 100
    d.line([MARGIN, y, W - MARGIN, y], fill=RED, width=4)
    d.line([MARGIN, y + 7, W - MARGIN, y + 7], fill=INK, width=1)
    y = 118
    center(d, "THURSDAY 19 NOVEMBER 2026", SANS_B(30), y, RED)
    y = 156
    center(d, "One day's world news \u2014 the stories that mattered most",
           SANS(18), y, GRAY)

    # ---------- lead story ----------
    y = 196
    d.text((MARGIN, y), "DIPLOMACY  \u00b7  SHENZHEN, CHINA", font=SANS_B(16),
           fill=RED)
    y = 222
    y = draw_lines(d, ["TRUMP, XI AND PUTIN", "MEET IN SHENZHEN"],
                   SERIF_B(44), MARGIN, y, INK, 52)
    y = 330
    lead = ("First-ever trilateral of the US, Chinese and Russian leaders, "
            "on the APEC sidelines. Nuclear arms control tops the agenda; "
            "Ukraine and Iran also raised. No deal expected.")
    y = draw_lines(d, wrap(d, lead, SANS(22), W - 2 * MARGIN), SANS(22),
                   MARGIN, y, INK, 29)
    skyline(d, MARGIN, 414, W - MARGIN, 462)

    # ---------- divider ----------
    d.line([MARGIN, 478, W - MARGIN, 478], fill=INK, width=2)

    # ---------- grid: 5 stories + by-the-numbers ----------
    col_w = (W - 2 * MARGIN - 2 * 24) // 3
    row_h = 196
    grid_top = 494
    cells = [
        ("JUSTICE  \u00b7  THE HAGUE", TEAL,
         "UN court: Myanmar committed genocide",
         "ICJ finds genocidal intent in the 2017 crackdown on the Rohingya; "
         "about 10,000 killed, 730,000+ fled."),
        ("WAR IN UKRAINE", BLUE,
         "Crimea bridge hit a third time in a week",
         "Road arch already down; overnight strike reported to hit the rail "
         "section. Traffic across the Kerch Strait halted."),
        ("MIDDLE EAST  \u00b7  RIYADH", AMBER,
         "Houthi missile damages Riyadh's tallest tower",
         "Windows blown out across 7\u20138 floors of the PIF Tower, HQ of "
         "the Saudi wealth fund. No casualties reported."),
        ("SOUTH ASIA", GREEN,
         "Yunus home torched as unrest spreads",
         "Violence in 28 districts amid an Awami League lockdown ahead of "
         "Hasina's planned December return."),
        ("MIDDLE EAST  \u00b7  GAZA", RED,
         "Israeli tanks cross Gaza ceasefire line",
         "First ground raid across the Yellow Line since the October 2025 "
         "truce, to destroy a tunnel; the army says the raid is over."),
    ]
    for idx, (tag, color, head, body) in enumerate(cells):
        r, c = divmod(idx, 3)
        x = MARGIN + c * (col_w + 24)
        y = grid_top + r * (row_h + 14)
        d.text((x, y), tag, font=SANS_B(14), fill=color)
        y += 24
        y = draw_lines(d, wrap(d, head, SANS_B(24), col_w), SANS_B(24),
                       x, y, INK, 29)
        y += 4
        draw_lines(d, wrap(d, body, SANS(18), col_w), SANS(18), x, y, INK, 23)

    # by-the-numbers cell (bottom right)
    x = MARGIN + 2 * (col_w + 24)
    y = grid_top + 1 * (row_h + 14)
    d.text((x, y), "BY THE NUMBERS", font=SANS_B(14), fill=RED)
    y += 26
    stats = [("730,000+", "Rohingya fled to Bangladesh, 2017"),
             ("227 m", "Crimea bridge roadway destroyed"),
             ("80 floors", "PIF Tower, Riyadh's tallest, hit")]
    for num, label in stats:
        d.text((x, y), num, font=SANS_B(20), fill=INK)
        y += 26
        d.text((x, y), label, font=SANS(16), fill=GRAY)
        y += 22

    # column separators
    for c in (1, 2):
        sx = MARGIN + c * col_w + (c - 1) * 24 + 12
        d.line([sx, grid_top, sx, grid_top + 2 * row_h + 14],
               fill=LIGHT_RULE, width=1)

    # ---------- also today band ----------
    band_top = 900
    d.rectangle([0, band_top, W, 976], fill=BAND)
    d.text((MARGIN, band_top + 10), "ALSO TODAY", font=SANS_B(17), fill=(232, 120, 90))
    items = ("COP31 ministers split on fossil-fuel phaseout in Antalya"
             "   \u00b7   Anthropic debuts on Nasdaq after record $81.3B IPO"
             "   \u00b7   Cyclone Akvan: Odisha evacuates 50,000+"
             "   \u00b7   GTA VI launches after a 13-year wait")
    lines = wrap(d, items, SANS(17), W - 2 * MARGIN)
    y = band_top + 32
    for ln in lines:
        d.text((MARGIN, y), ln, font=SANS(17), fill=(245, 242, 235))
        y += 20

    # ---------- footer ----------
    center(d, "Sources: Reuters, AP, BBC, Al Jazeera, The Guardian  \u00b7  "
              "All events 19 November 2026", SANS(13), 988, GRAY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
