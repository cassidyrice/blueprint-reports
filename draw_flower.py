
"""
Flower of Life with 13 pip symbols — rendered via Pillow using Segoe UI Symbol
for crisp Unicode suit rendering (♠ ♥ ♦ ♣).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT = r"c:\Users\abvik\OneDrive\Desktop\Hotel\outputs\flower_of_life.png"
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# ── Canvas settings ───────────────────────────────────────────────────────────
SIZE     = 1600        # px square canvas
CX = CY  = SIZE // 2
R        = 118         # radius of each small circle (px)

# ── Colors ────────────────────────────────────────────────────────────────────
CREAM      = (253, 250, 245)
INK        = (26,  26,  26)
RED        = (196, 30,  58)
RING_LIGHT = (180, 180, 180)

# ── Fonts (Windows — Segoe UI Symbol renders ♠ ♥ ♦ ♣ natively) ───────────────
FONT_PATH_SYMBOL = r"C:\Windows\Fonts\seguisym.ttf"   # Segoe UI Symbol
FONT_PATH_BOLD   = r"C:\Windows\Fonts\arialbd.ttf"    # fallback

def load_font(size):
    for path in [FONT_PATH_SYMBOL, FONT_PATH_BOLD]:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()

# ── Geometry helpers ──────────────────────────────────────────────────────────
def hex_to_xy(q, r_hex, radius):
    """Axial hex → cartesian (pointy-top orientation)."""
    x = radius * (math.sqrt(3) * q + math.sqrt(3) / 2 * r_hex)
    y = radius * (3 / 2 * r_hex)
    return x, y

def circle_points(cx, cy, r, steps=300):
    pts = []
    for i in range(steps + 1):
        a = 2 * math.pi * i / steps
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

# ── Draw Flower of Life ───────────────────────────────────────────────────────
# 19 inner circles in standard hex shell arrangement
HEX_RING_0 = [(0, 0)]
HEX_RING_1 = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
HEX_RING_2 = [
    (2,0),(1,1),(0,2),(-1,2),(-2,2),(-2,1),
    (-2,0),(-1,-1),(0,-2),(1,-2),(2,-2),(2,-1)
]
ALL_HEXES = HEX_RING_0 + HEX_RING_1 + HEX_RING_2

# ── 13 Pip positions in axial coords ─────────────────────────────────────────
# Center column (5): q=0, r = -2,-1,0,1,2
# Left column   (4): q=-1, r = -1,0,1,2
# Right column  (4): q=1,  r = -2,-1,0,1
PIP_POSITIONS = [
    # (q, r_hex, suit_symbol, pip_color)
    # CENTER column — bottom to top
    (0, -2, "♠", INK),
    (0, -1, "♥", RED),
    (0,  0, "♦", RED),
    (0,  1, "♣", INK),
    (0,  2, "♠", INK),
    # LEFT column — bottom to top (offset)
    (-1, -1, "♥", RED),
    (-1,  0, "♦", RED),
    (-1,  1, "♣", INK),
    (-1,  2, "♠", INK),
    # RIGHT column — bottom to top (offset)
    (1, -2, "♥", RED),
    (1, -1, "♦", RED),
    (1,  0, "♣", INK),
    (1,  1, "♠", INK),
]

def main():
    img = Image.new("RGB", (SIZE, SIZE), CREAM)
    draw = ImageDraw.Draw(img)

    # ── Draw the 19 inner circles of the Flower of Life ──────────────────────
    for (q, r_hex) in ALL_HEXES:
        dx, dy = hex_to_xy(q, r_hex, R)
        ox, oy = CX + dx, CY - dy   # invert Y for screen coords
        bbox = [ox - R, oy - R, ox + R, oy + R]
        draw.ellipse(bbox, outline=INK, width=2)

    # ── Draw outer containment rings ──────────────────────────────────────────
    outer1 = 2 * R + R * 0.22
    outer2 = 2 * R + R * 0.10
    for radius, width in [(outer1, 5), (outer2, 2)]:
        bbox = [CX - radius, CY - radius, CX + radius, CY + radius]
        draw.ellipse(bbox, outline=INK, width=width)

    # ── Draw pip symbols ──────────────────────────────────────────────────────
    pip_font = load_font(int(R * 0.72))

    for (q, r_hex, sym, color) in PIP_POSITIONS:
        dx, dy = hex_to_xy(q, r_hex, R)
        px, py = CX + dx, CY - dy   # invert Y

        # Cream backing circle so pip reads cleanly over dark ink lines
        backing_r = int(R * 0.38)
        bbox = [px - backing_r, py - backing_r, px + backing_r, py + backing_r]
        draw.ellipse(bbox, fill=CREAM, outline=None)

        # Draw the suit symbol centered
        bbox_text = draw.textbbox((0, 0), sym, font=pip_font)
        tw = bbox_text[2] - bbox_text[0]
        th = bbox_text[3] - bbox_text[1]
        tx = px - tw / 2 - bbox_text[0]
        ty = py - th / 2 - bbox_text[1]
        draw.text((tx, ty), sym, font=pip_font, fill=color)

    img.save(OUTPUT, dpi=(300, 300))
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()
