#!/usr/bin/env python3
"""Draw the v3 poster: THE WORLD TODAY, Thursday 19 November 2026.

Hybrid design: v1's information density with v2's clean hierarchy.
18 stories: 1 lead + 10 grid stories + 6 in the ALSO TODAY strip.
Headlines stay readable at 300 px, but the detail v2 cut is back.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (17, 17, 17)
RED = (200, 16, 46)
NAVY = (20, 33, 61)
NAVY_LT = (34, 53, 94)
GRAY = (68, 68, 68)
RULE = (216, 210, 196)
WHITE = (255, 255, 255)
BLACK = (13, 13, 13)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
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


def wrap_tokens(tokens, fnt_plain, fnt_bold, max_w):
    """Wrap (word, bold?) tokens; returns lines of tokens."""
    lines, cur, cur_w = [], [], 0.0
    for word, bold in tokens:
        fnt = fnt_bold if bold else fnt_plain
        w = fnt.getlength(word)
        space = fnt_plain.getlength(" ") if cur else 0.0
        if cur and cur_w + space + w > max_w:
            lines.append(cur)
            cur, cur_w = [(word, bold)], w
        else:
            cur.append((word, bold))
            cur_w += space + w
    if cur:
        lines.append(cur)
    return lines


LEAD_KICKER = "FIRST TRILATERAL SUMMIT — SHENZHEN"
LEAD_HEAD = ["TRUMP, XI AND PUTIN", "MEET IN SHENZHEN"]
LEAD_SUB = "First trilateral: peace declaration; arms, Ukraine, Iran on the table"

GRID = [
    ("WORLD COURT FINDS MYANMAR GUILTY", "Rohingya genocide: Gambia v Myanmar"),
    ("KERCH RAIL SPAN REPORTED HIT", "Third strike this week — arch down 17 Nov"),
    ("HOUTHI STRIKE HITS RIYADH TOWER", "Blast damages PIF headquarters"),
    ("UNREST TORCHES YUNUS'S HOME", "Protests in Bangladesh; home torched"),
    ("ISRAEL PUSHES INTO CENTRAL GAZA", "Raid from 18 Nov ends today"),
    ("ANTHROPIC'S $81.3B RECORD IPO", "Biggest AI listing ever"),
    ("COP31 DEAL TEXT DROPS FOSSIL FUELS", "Revised draft omits phaseout"),
    ("CYCLONE AKVAN SLAMS ODISHA", "50,000 evacuated as storm hits"),
    ("US–VENEZUELA DEFENCE PACT", "Hegseth inks deal in surprise trip"),
    ("DENMARK OKS GREENLAND–US DEAL", "Parliament approves US bases deal"),
]

STRIP_ITEMS = [
    "Hormuz: 3 tankers ablaze on mines",
    "Abu Dhabi talks fail; Ukraine grid hit",
    "Ethiopia–Eritrea clashes risk war",
    "GTA VI out after 13-year wait",
    "IEA: Hormuz shock is largest ever",
]

FOOTER = "SOURCES: AP • REUTERS • AFP • AL JAZEERA"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 124], fill=BLACK)
    d.text((W // 2, 8), "THE WORLD TODAY", font=font(SERIF_B, 68),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 80), "THURSDAY 19 NOVEMBER 2026", font=font(SANS_B, 38),
           fill=RED, anchor="ma")
    d.rectangle([0, 124, W, 128], fill=RED)

    # --- lead story ---
    d.text((W // 2, 140), LEAD_KICKER, font=font(SANS_B, 24),
           fill=RED, anchor="ma")
    f_lead = font(SERIF_B, 54)
    d.text((W // 2, 168), LEAD_HEAD[0], font=f_lead, fill=INK, anchor="ma")
    d.text((W // 2, 226), LEAD_HEAD[1], font=f_lead, fill=INK, anchor="ma")
    d.text((W // 2, 290), LEAD_SUB, font=font(SANS, 23), fill=GRAY, anchor="ma")

    # --- skyline silhouette divider ---
    d.rectangle([0, 322, W, 338], fill=NAVY)
    heights = [10, 14, 8, 16, 11, 15, 9, 13, 16, 10,
               14, 8, 15, 11, 13, 9, 16, 12, 14, 10]
    bw = W // len(heights)
    for i, hgt in enumerate(heights):
        x0 = i * bw + 2
        d.rectangle([x0, 338 - hgt, x0 + bw - 4, 338], fill=NAVY_LT)

    # --- grid: 2 columns x 5 rows ---
    grid_top, row_h = 338, 108
    col_x = [24, 524]
    col_w = 476
    f_head = font(SANS_B, 31)
    f_sub = font(SANS, 22)
    for idx, (head, sub) in enumerate(GRID):
        r, c = divmod(idx, 2)
        x0 = col_x[c]
        y0 = grid_top + r * row_h
        lines = wrap(head, f_head, col_w)
        assert len(lines) <= 2, f"headline wraps to {len(lines)}: {head}"
        y = y0 + 8
        for line in lines:
            d.text((x0, y), line, font=f_head, fill=INK, anchor="la")
            y += 35
        assert f_sub.getlength(sub) <= col_w, f"sub too long: {sub}"
        d.text((x0, y + 6), sub, font=f_sub, fill=GRAY, anchor="la")
        assert y + 6 + 22 <= y0 + row_h, f"cell overflows: {head}"
    # dividers
    for r in range(1, 5):
        y = grid_top + r * row_h
        d.line([(24, y), (1000, y)], fill=RULE, width=1)
    d.line([(512, grid_top), (512, grid_top + 5 * row_h)], fill=RULE, width=1)

    # --- ALSO TODAY strip ---
    strip_top, strip_h = 878, 114
    d.rectangle([0, strip_top, W, strip_top + strip_h], fill=NAVY)
    tokens = []
    for word in "ALSO TODAY:".split():
        tokens.append((word, True))
    for item in STRIP_ITEMS:
        for word in item.split():
            tokens.append((word, False))
        tokens.append(("•", False))
    tokens = tokens[:-1]  # drop trailing bullet
    f_strip = font(SANS, 22)
    f_strip_b = font(SANS_B, 22)
    lines = wrap_tokens(tokens, f_strip, f_strip_b, W - 48)
    assert len(lines) <= 3, f"strip wraps to {len(lines)} lines"
    y = strip_top + 14
    for line in lines:
        x = 24
        for word, bold in line:
            fnt = f_strip_b if bold else f_strip
            fill = RED if bold else WHITE
            d.text((x, y), word, font=fnt, fill=fill, anchor="la")
            x += fnt.getlength(word + " ")
        y += 28

    # --- footer ---
    d.text((W // 2, 998), FOOTER, font=font(SANS, 20), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    size = os.path.getsize(out)
    assert img.size == (1024, 1024)
    assert size <= 1048576, f"entry.png too big: {size}"
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {size} bytes")
    print(f"stories: 1 lead + {len(GRID)} grid + {len(STRIP_ITEMS)} strip "
          f"= {1 + len(GRID) + len(STRIP_ITEMS)}")


if __name__ == "__main__":
    main()
