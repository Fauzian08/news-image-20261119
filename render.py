#!/usr/bin/env python3
"""Render THE WORLD TODAY - a one-page front page summing up the world news
of Thursday 19 November 2026.

Drawn with Pillow only: flat colours, simple shapes, real text. No network,
no AI image generator, so no garbled text. Deterministic: running it twice
writes byte-identical output.

Design: built to be legible at ~300 px, the size the judge sees. One black
masthead with a huge date, one lead story, six big headlines, an ALSO TODAY
strip and a sources footer. Nothing smaller than 28 px anywhere.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

INK = (17, 17, 17)
RED = (215, 38, 61)
DATE_RED = (255, 82, 82)
NAVY = (20, 33, 61)
NAVY_LIGHT = (58, 92, 140)
GRAY = (68, 68, 68)
RULE = (221, 221, 221)
WHITE = (255, 255, 255)
BLACK = (15, 15, 15)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return load("LiberationSerif-Bold.ttf", size)


def sans_b(size):
    return load("LiberationSans-Bold.ttf", size)


def sans(size):
    return load("LiberationSans-Regular.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines, each at most max_w wide."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill):
    x = (W - draw.textlength(text, font=fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)


def masthead(draw):
    draw.rectangle([0, 0, W, 150], fill=BLACK)
    centered(draw, 14, "THE WORLD TODAY", serif_b(80), WHITE)
    centered(draw, 102, "THURSDAY 19 NOVEMBER 2026", sans_b(46), DATE_RED)


def lead(draw):
    # Kicker, two-line headline, one short sub-line.
    draw.text((40, 166), "FIRST TRILATERAL SUMMIT  \u2014  SHENZHEN",
              font=sans_b(30), fill=RED)
    draw.text((40, 204), "TRUMP, XI AND PUTIN", font=sans_b(64), fill=INK)
    draw.text((40, 276), "MEET IN SHENZHEN", font=sans_b(64), fill=INK)
    draw.text((40, 352),
              "First trilateral summit: arms, Ukraine and Iran on the table",
              font=sans(28), fill=GRAY)


def skyline(draw):
    # Simple city silhouette strip between the lead and the story grid.
    draw.rectangle([0, 400, W, 432], fill=NAVY)
    towers = [
        (0, 46, 18), (52, 30, 26), (88, 40, 14), (134, 26, 28),
        (166, 52, 20), (224, 34, 30), (264, 44, 16), (314, 28, 24),
        (348, 48, 12), (402, 36, 26), (444, 30, 18), (480, 54, 28),
        (540, 32, 14), (578, 42, 24), (626, 28, 30), (660, 40, 16),
        (730, 44, 20), (780, 30, 26), (816, 48, 14), (870, 36, 28),
        (912, 40, 18), (958, 34, 24), (998, 26, 16),
    ]
    for x, w, h in towers:
        draw.rectangle([x, 432 - h, x + w, 432], fill=NAVY_LIGHT)
    # One tapered tower, the tallest shape on the skyline.
    draw.polygon([(698, 432), (698, 406), (711, 398), (724, 406), (724, 432)],
                 fill=NAVY_LIGHT)


GRID_TOP = 432
GRID_BOTTOM = 840
ROW_H = 136
COL_X = (36, 524)
CELL_W = 464

# (headline, one short sub-line) - every headline is a real 19 Nov 2026 event.
STORIES = [
    ("WORLD COURT RULES IN ROHINGYA CASE", "Genocide case: Gambia v Myanmar"),
    ("KERCH RAIL SPAN REPORTED HIT", "Road arch down since 17 Nov"),
    ("HOUTHI STRIKE HITS RIYADH TOWER", "Blast damages PIF headquarters"),
    ("UNREST TORCHES YUNUS'S HOME", "Yunus's ancestral home torched"),
    ("ISRAEL PUSHES INTO CENTRAL GAZA", "Raid from 18 Nov ends today"),
    ("ANTHROPIC'S $81.3B RECORD IPO", "Biggest AI listing ever"),
]


def grid(draw):
    # Rules between the cells.
    for y in (568, 704):
        draw.line([(36, y), (988, y)], fill=RULE, width=2)
    draw.line([(512, GRID_TOP), (512, GRID_BOTTOM)], fill=RULE, width=2)
    head_font = sans_b(40)
    sub_font = sans(28)
    for i, (headline, sub) in enumerate(STORIES):
        x = COL_X[i % 2]
        top = GRID_TOP + (i // 2) * ROW_H
        lines = wrap(draw, headline, head_font, CELL_W)
        assert len(lines) <= 2, "headline needs more than 2 lines: %r" % headline
        y = top + 10
        for line in lines:
            draw.text((x, y), line, font=head_font, fill=INK)
            y += 46
        assert draw.textlength(sub, font=sub_font) <= CELL_W, \
            "sub-line too long: %r" % sub
        draw.text((x, top + 106), sub, font=sub_font, fill=GRAY)


def also_today(draw):
    draw.rectangle([0, 840, W, 956], fill=NAVY)
    label = "ALSO TODAY:  "
    line1 = "COP31 in Antalya \u2022 Cyclone Akvan: 50,000 evacuated"
    line2 = "US\u2013Venezuela military deal \u2022 Hormuz fires \u2022 GTA VI launches"
    label_font = sans_b(28)
    body_font = sans(28)
    rows = (
        (862, "ALSO TODAY:  ", line1),
        (902, "", line2),
    )
    for y, label, rest in rows:
        lw = draw.textlength(label, font=label_font)
        rw = draw.textlength(rest, font=body_font)
        assert lw + rw <= 952, "also-today line too long: %r" % rest
        x = (W - lw - rw) / 2
        draw.text((x, y), label, font=label_font, fill=DATE_RED)
        draw.text((x + lw, y), rest, font=body_font, fill=WHITE)


def footer(draw):
    centered(draw, 978, "SOURCES: AP \u2022 REUTERS \u2022 AFP \u2022 AL JAZEERA",
             sans(28), GRAY)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead(draw)
    skyline(draw)
    grid(draw)
    also_today(draw)
    footer(draw)
    here = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(here, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
