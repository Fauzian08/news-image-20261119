#!/usr/bin/env python3
"""Render v4 poster: THE WORLD TODAY — Thursday 19 November 2026.

Draws 19 verified stories of 19 Nov 2026 with Python PIL only.
Writes entry.png (1024x1024, < 1 MiB).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

INK = (17, 17, 17)
RED = (200, 16, 46)
SUB = (51, 51, 51)
GREY = (119, 119, 119)
RULE = (204, 204, 204)
NAVY = (13, 27, 45)
WHITE = (255, 255, 255)
PAPER = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap by measured width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="mm")


# ---------------------------------------------------------------- content
LEAD_KICKER = "FIRST TRILATERAL SUMMIT \u2014 SHENZHEN"
LEAD_HEAD = "TRUMP, XI AND PUTIN MEET IN SHENZHEN"
LEAD_SUB = (
    "First trilateral summit: Trump met Putin about 40 minutes and Xi "
    "separately first; a peace declaration and nuclear arms control \u2014 "
    "New START expiring \u2014 plus Ukraine and Iran on the table."
)

# (headline, sub-line) — 12 grid stories
GRID = [
    ("MYANMAR GUILTY",
     "World court 9\u20136: Rohingya genocide; ~10,000 killed, first state held responsible"),
    ("KERCH BRIDGE HIT AGAIN",
     "Rail span reported struck \u2014 third this week; road arch down 17 Nov"),
    ("RIYADH'S TALLEST TOWER HIT",
     "Houthi strike damages PIF headquarters"),
    ("YUNUS HOME TORCHED IN UNREST",
     "Bangladesh: protesters torch Yunus's home"),
    ("GAZA RAID ENDS TODAY",
     "Israel's central Gaza operation, begun 18 Nov, ends"),
    ("ANTHROPIC'S $81.3B RECORD IPO",
     "Biggest AI listing ever; priced $83 a share"),
    ("COP31 DROPS FOSSIL FUELS",
     "Revised draft omits phaseout; final stretch"),
    ("CYCLONE AKVAN SLAMS ODISHA",
     "50,000 evacuated as storm makes landfall"),
    ("US\u2013VENEZUELA DEFENCE PACT",
     "Hegseth inks deal in surprise Caracas trip"),
    ("DENMARK OKS US BASES DEAL",
     "Greenland pact approved 109\u20130 in parliament"),
    ("SAUDI STRIKES HIT YEMEN",
     "Sanaa, Saada, Taiz bombed; 11 killed, 36 hurt"),
    ("IEA: HORMUZ SHOCK IS LARGEST EVER",
     "2.8bn barrels of oil, 60 bcm gas lost"),
]

# also-today strip: 6 items, 2 per line
STRIP = [
    ("Hormuz: 3 tankers ablaze on mines", "Abu Dhabi talks fail; Ukraine grid hit"),
    ("Ethiopia\u2013Eritrea clashes risk war", "GTA VI out after 13-year wait"),
    ("IAEA: N. Korea expands uranium plant", "US carrier leaves Gulf after 3 months"),
]

FOOTER = "Sources: AP \u2022 Reuters \u2022 AFP \u2022 Al Jazeera"

# ---------------------------------------------------------------- drawing
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
warnings = []

# Masthead: black band + title
d.rectangle([0, 20, W, 84], fill=(10, 10, 10))
draw_center(d, W // 2, 52, "THE WORLD TODAY", font(SERIF_B, 54), WHITE)

# Date line, huge and red
draw_center(d, W // 2, 111, "THURSDAY 19 NOVEMBER 2026", font(SERIF_B, 40), RED)
d.line([36, 140, 988, 140], fill=RULE, width=2)

# Lead
d.text((36, 148), LEAD_KICKER, font=font(SANS_B, 21), fill=RED)
lead_head_font = font(SERIF_B, 50)
lead_lines = wrap(LEAD_HEAD, lead_head_font, 952)
if len(lead_lines) != 2:
    warnings.append(f"lead headline wrapped to {len(lead_lines)} lines: {lead_lines}")
for i, line in enumerate(lead_lines):
    d.text((36, 176 + i * 54), line, font=lead_head_font, fill=INK)
lead_sub_font = font(SANS, 22)
sub_lines = wrap(LEAD_SUB, lead_sub_font, 952)
if len(sub_lines) > 3:
    warnings.append(f"lead sub wrapped to {len(sub_lines)} lines")
for i, line in enumerate(sub_lines[:3]):
    d.text((36, 286 + i * 25), line, font=lead_sub_font, fill=SUB)

# Skyline silhouette divider under the lead
skyline = [8, 11, 6, 13, 10, 7, 14, 9, 6, 12, 8, 10, 6, 13, 10, 7, 11, 9, 6, 12, 8, 10, 7, 12, 9, 6, 11, 8, 13, 9, 7, 10]
x = 36
step = (988 - 36) / len(skyline)
for hgt in skyline:
    d.rectangle([x, 378 - hgt, x + step - 2, 378], fill=(26, 26, 26))
    x += step
# two taller towers with spires
d.rectangle([300, 364, 312, 378], fill=(26, 26, 26))
d.line([306, 360, 306, 364], fill=(26, 26, 26), width=3)
d.rectangle([700, 366, 711, 378], fill=(26, 26, 26))
d.line([705, 362, 705, 366], fill=(26, 26, 26), width=3)

# Grid: 6 rows x 2 cols, row height 84, starting y 388
head_font = font(SERIF_B, 28)
sub_font = font(SANS, 20)
COL_W = 464
for idx, (headline, sub) in enumerate(GRID):
    row, col = divmod(idx, 2)
    cx = 36 + col * (COL_W + 24)
    y0 = 388 + row * 84
    h_lines = wrap(headline, head_font, COL_W)
    if len(h_lines) > 2:
        warnings.append(f"grid {idx+1} headline {len(h_lines)} lines: {headline}")
    for i, line in enumerate(h_lines[:2]):
        d.text((cx, y0 + 1 + i * 29), line, font=head_font, fill=INK)
    max_sub_lines = 2 if len(h_lines) == 1 else 1
    s_lines = wrap(sub, sub_font, COL_W)
    if len(s_lines) > max_sub_lines:
        warnings.append(
            f"grid {idx+1} sub needs {len(s_lines)} lines, budget {max_sub_lines}: {sub}")
    sub_y = y0 + 33 if len(h_lines) == 1 else y0 + 61
    for i, line in enumerate(s_lines[:max_sub_lines]):
        d.text((cx, sub_y + i * 23), line, font=sub_font, fill=SUB)
    if row < 5:
        d.line([36, y0 + 84, 988, y0 + 84], fill=(221, 221, 221), width=1)

# Also-today strip: dark navy band
d.rectangle([0, 898, W, 1000], fill=NAVY)
d.text((36, 904), "ALSO TODAY", font=font(SANS_B, 20), fill=(255, 90, 90))
for li, (left, right) in enumerate(STRIP):
    y = 928 + li * 24
    size = 22
    while size >= 18:
        fnt = font(SANS, size)
        text = f"{left}   \u2022   {right}"
        if fnt.getlength(text) <= 952:
            break
        size -= 1
    d.text((36, y), text, font=font(SANS, size), fill=WHITE)

# Footer
draw_center(d, W // 2, 1012, FOOTER, font(SANS, 15), GREY)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out_path, "PNG")
size = os.path.getsize(out_path)
print(f"saved {out_path}  {size} bytes  ({size/1024:.1f} KiB)")
print(f"grid stories: {len(GRID)}  strip items: {len(STRIP)*2}  "
      f"total stories: {1 + len(GRID) + len(STRIP)*2}")
if warnings:
    print("WARNINGS:")
    for w_ in warnings:
        print(" -", w_)
else:
    print("no layout warnings")
