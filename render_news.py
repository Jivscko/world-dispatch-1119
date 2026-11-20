#!/usr/bin/env python3
"""World Dispatch - 19 November 2026 front page renderer.

Draws a 1024x1024 newspaper-style news infographic with PIL only:
off-white paper, dark ink, red section labels, PIL-drawn icons.
No network, no external assets (uses Pillow's bundled default font).
Fact check: 19 November 2026 is a THURSDAY.
"""

import datetime
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 44  # page margin

PAPER = (248, 245, 238)
INK = (26, 26, 30)
RED = (176, 32, 32)
GRAY = (92, 92, 98)
RULE_LIGHT = (190, 186, 176)

# Sanity: the date line must match the real calendar.
assert datetime.date(2026, 11, 19).strftime("%A") == "Thursday"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(size: int):
    return ImageFont.load_default(size=size)


def text(x, y, s, size, fill=INK, bold=False, anchor=None):
    d.text((x, y), s, font=font(size), fill=fill,
           stroke_width=1 if bold else 0, stroke_fill=fill, anchor=anchor)


def width(s, size, bold=False):
    # stroke adds ~2px for bold text; budget for it so wraps stay safe
    return d.textlength(s, font=font(size)) + (2 if bold else 0)


def wrap(s, size, max_w, bold=False):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if width(trial, size, bold) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(y, s, size, fill=INK, bold=False):
    text(W // 2, y, s, size, fill, bold, anchor="ma")


def hrule(y, x0=M, x1=W - M, fill=INK, w=2):
    d.rectangle([x0, y, x1, y + w - 1], fill=fill)


# ---------------------------------------------------------------- masthead
centered(28, "THE WORLD DISPATCH", 62, INK, bold=True)
centered(106, "THURSDAY, 19 NOVEMBER 2026 - GLOBAL EDITION", 19, INK)
hrule(140, w=3)
hrule(146, w=1)

# ---------------------------------------------------------------- lead
text(M, 160, "CULTURE", 17, RED, bold=True)
text(M, 184, "GTA VI launches worldwide", 40, INK, bold=True)
lead_sub = ("Rockstar's Vice City sequel arrives after a 13-year wait; "
            "players and spectators experience the launch together.")
y = 238
for line in wrap(lead_sub, 21, W - 2 * M):
    text(M, y, line, 21, GRAY)
    y += 27
hrule(304, w=2)

# ---------------------------------------------------------------- icons
def icon_globe(x, y):
    d.ellipse([x + 3, y + 3, x + 43, y + 43], outline=INK, width=3)
    d.ellipse([x + 14, y + 3, x + 32, y + 43], outline=INK, width=2)
    d.line([x + 5, y + 16, x + 41, y + 16], fill=INK, width=2)
    d.line([x + 5, y + 30, x + 41, y + 30], fill=INK, width=2)


def icon_scales(x, y):
    d.line([x + 23, y + 6, x + 23, y + 38], fill=INK, width=3)
    d.line([x + 12, y + 40, x + 34, y + 40], fill=INK, width=3)
    d.line([x + 6, y + 12, x + 40, y + 12], fill=INK, width=3)
    for cx in (x + 8, x + 38):
        d.line([cx, y + 12, cx, y + 20], fill=INK, width=2)
        d.arc([cx - 7, y + 14, cx + 7, y + 28], 0, 180, fill=RED, width=3)


def icon_chart(x, y):
    d.line([x + 6, y + 6, x + 6, y + 40], fill=INK, width=3)
    d.line([x + 6, y + 40, x + 42, y + 40], fill=INK, width=3)
    d.rectangle([x + 12, y + 28, x + 18, y + 38], fill=INK)
    d.rectangle([x + 22, y + 20, x + 28, y + 38], fill=INK)
    d.rectangle([x + 32, y + 10, x + 38, y + 38], fill=RED)


def icon_bridge(x, y):
    d.line([x + 2, y + 32, x + 44, y + 32], fill=INK, width=3)
    for tx in (x + 12, x + 34):
        d.line([tx, y + 10, tx, y + 32], fill=INK, width=3)
    d.line([x + 12, y + 10, x + 2, y + 32], fill=INK, width=2)
    d.line([x + 34, y + 10, x + 44, y + 32], fill=INK, width=2)
    d.line([x + 12, y + 10, x + 23, y + 28], fill=INK, width=2)
    d.line([x + 34, y + 10, x + 23, y + 28], fill=INK, width=2)
    # strike burst
    for dx, dy in ((0, -7), (0, 7), (-7, 0), (7, 0), (-5, -5), (5, 5), (-5, 5), (5, -5)):
        d.line([x + 23, y + 20, x + 23 + dx, y + 20 + dy], fill=RED, width=2)


def icon_storm(x, y):
    d.ellipse([x + 4, y + 8, x + 26, y + 26], outline=INK, width=3)
    d.ellipse([x + 18, y + 4, x + 42, y + 24], outline=INK, width=3)
    d.line([x + 8, y + 25, x + 38, y + 25], fill=INK, width=3)
    d.polygon([(x + 26, y + 26), (x + 16, y + 36), (x + 22, y + 36),
               (x + 17, y + 45), (x + 31, y + 33), (x + 25, y + 33),
               (x + 29, y + 26)], fill=RED)


def icon_heart(x, y):
    d.ellipse([x + 5, y + 8, x + 25, y + 28], fill=RED)
    d.ellipse([x + 21, y + 8, x + 41, y + 28], fill=RED)
    d.polygon([(x + 7, y + 21), (x + 39, y + 21), (x + 23, y + 43)], fill=RED)


# ---------------------------------------------------------------- story grid
STORIES = [
    ("GEOPOLITICS", "Trump, Putin, Xi nuclear pact",
     "Joint statement echoes Reagan-Gorbachev.", icon_globe),
    ("INTERNATIONAL LAW", "UN: Myanmar Rohingya genocide",
     "UN tribunal confirms Rohingya genocide.", icon_scales),
    ("BUSINESS & TECH", "Anthropic sets record $83 IPO",
     "AI lab passes IPO test; staff wealthy.", icon_chart),
    ("CONFLICT", "Crimea bridge hit again",
     "Strategic link struck third time.", icon_bridge),
    ("WEATHER", "Florida storm snarls travel",
     "System may disrupt Thanksgiving trips.", icon_storm),
    ("UNITED STATES", "Fiona the hippo dies",
     "Cincinnati Zoo icon remembered.", icon_heart),
]

GAP = 28
COL_W = (W - 2 * M - GAP) // 2  # 454
GRID_TOP = 322
ROW_H = 202

for i, (tag, head, sub, icon) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x = M + col * (COL_W + GAP)
    y = GRID_TOP + row * ROW_H
    icon(x, y)
    text(x + 58, y + 4, tag, 15, RED, bold=True)
    hy = y + 56
    for line in wrap(head, 23, COL_W, bold=True):
        text(x, hy, line, 23, INK, bold=True)
        hy += 29
    sy = hy + 6
    for line in wrap(sub, 17, COL_W):
        text(x, sy, line, 17, GRAY)
        sy += 22
    if row < 2:
        hrule(y + ROW_H - 10, x0=x, x1=x + COL_W, fill=RULE_LIGHT, w=1)

# column divider
d.rectangle([W // 2 - 1, GRID_TOP, W // 2, GRID_TOP + 3 * ROW_H - 14], fill=RULE_LIGHT)

# ---------------------------------------------------------------- footer
hrule(944, w=2)
centered(958, "WORLD NEWS - 19 NOVEMBER 2026 - POLITICS LAW BUSINESS CONFLICT WEATHER CULTURE",
         16, INK)

# ---------------------------------------------------------------- save + verify
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)

check = Image.open(out)
nbytes = os.path.getsize(out)
assert check.size == (1024, 1024), check.size
assert nbytes <= 1_048_576, nbytes
print(f"entry.png: {check.size[0]}x{check.size[1]}, {nbytes} bytes - OK")
