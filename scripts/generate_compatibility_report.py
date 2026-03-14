#!/usr/bin/env python3
"""
Compatibility Report — Print-Ready PDF
Same architectural/blueprint aesthetic as Card Blueprint.
Red for ♥/♦, black for ♠/♣. Small text bumped 2-3pt and set to black.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── FONTS ──────────────────────────────────────────────
FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
SYS_FONTS = "/usr/share/fonts/truetype"

pdfmetrics.registerFont(TTFont("GeistMono", f"{FONT_DIR}/GeistMono-Regular.ttf"))
pdfmetrics.registerFont(TTFont("GeistMono-Bold", f"{FONT_DIR}/GeistMono-Bold.ttf"))
pdfmetrics.registerFont(TTFont("InstrumentSans", f"{FONT_DIR}/InstrumentSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("InstrumentSans-Bold", f"{FONT_DIR}/InstrumentSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("BigShoulders", f"{FONT_DIR}/BigShoulders-Regular.ttf"))
pdfmetrics.registerFont(TTFont("BigShoulders-Bold", f"{FONT_DIR}/BigShoulders-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Jura-Light", f"{FONT_DIR}/Jura-Light.ttf"))
pdfmetrics.registerFont(TTFont("Jura-Medium", f"{FONT_DIR}/Jura-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Outfit", f"{FONT_DIR}/Outfit-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Outfit-Bold", f"{FONT_DIR}/Outfit-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu", f"{SYS_FONTS}/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", f"{SYS_FONTS}/dejavu/DejaVuSans-Bold.ttf"))

# ── COLORS ─────────────────────────────────────────────
WARM_BLACK = HexColor("#1A1A1A")
RED = HexColor("#C41E3A")
DARK_GRAY = HexColor("#333333")
MID_GRAY = HexColor("#777777")
LIGHT_GRAY = HexColor("#CCCCCC")
HAIRLINE_GRAY = HexColor("#E0E0E0")
BG_CREAM = HexColor("#FAFAF8")
FAINT_RED = HexColor("#FBF0F0")
FAINT_BLACK = HexColor("#F4F4F3")
ACCENT_LINE = HexColor("#B8B8B8")
WHITE = HexColor("#FFFFFF")

# Text color override: small body text → WARM_BLACK (not gray)
BODY_TEXT = WARM_BLACK

W, H = letter
MARGIN = 0.55 * inch
INNER_W = W - 2 * MARGIN
INNER_H = H - 2 * MARGIN


def suit_color(card_str):
    if "♥" in card_str or "♦" in card_str:
        return RED
    return WARM_BLACK


def get_suit(card_str):
    for ch in card_str:
        if ch in "♥♦♠♣":
            return ch
    return ""


def get_rank(card_str):
    return card_str.replace("♥", "").replace("♦", "").replace("♠", "").replace("♣", "")


def draw_card_chip(c, x, y, card, size=9, chip_w=32, chip_h=17):
    color = suit_color(card)
    rank = get_rank(card)
    suit = get_suit(card)
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.setFillColor(WHITE)
    c.roundRect(x, y - 4, chip_w, chip_h, 2.5, fill=1, stroke=1)
    c.setFillColor(color)
    c.setFont("GeistMono-Bold", size)
    rw = c.stringWidth(rank, "GeistMono-Bold", size)
    c.setFont("DejaVu-Bold", size - 1)
    sw = c.stringWidth(suit, "DejaVu-Bold", size - 1)
    total = rw + sw + 1
    start_x = x + (chip_w - total) / 2
    c.setFont("GeistMono-Bold", size)
    c.setFillColor(color)
    c.drawString(start_x, y, rank)
    c.setFont("DejaVu-Bold", size - 1)
    c.drawString(start_x + rw + 1, y, suit)


def draw_big_card(c, x, y, card, rank_size=36, suit_size=28):
    """Draw a large card display (rank + suit)."""
    color = suit_color(card)
    rank = get_rank(card)
    suit = get_suit(card)
    c.setFillColor(color)
    c.setFont("BigShoulders-Bold", rank_size)
    c.drawString(x, y, rank)
    rw = c.stringWidth(rank, "BigShoulders-Bold", rank_size)
    c.setFont("DejaVu-Bold", suit_size)
    c.drawString(x + rw + 2, y + 4, suit)
    return rw + c.stringWidth(suit, "DejaVu-Bold", suit_size) + 2


def hrule(c, y, x1=None, x2=None):
    x1 = x1 or (MARGIN + 10)
    x2 = x2 or (W - MARGIN - 10)
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.3)
    c.line(x1, y, x2, y)
    return y


def draw_registration_marks(c):
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.3)
    off = 0.32 * inch
    ln = 0.18 * inch
    for cx, cy in [(MARGIN, H - MARGIN), (W - MARGIN, H - MARGIN),
                   (MARGIN, MARGIN), (W - MARGIN, MARGIN)]:
        dx = -1 if cx < W / 2 else 1
        dy = -1 if cy < H / 2 else 1
        c.line(cx - dx * off, cy, cx - dx * (off + ln), cy)
        c.line(cx, cy - dy * off, cx, cy - dy * (off + ln))


def draw_frame(c):
    c.setStrokeColor(DARK_GRAY)
    c.setLineWidth(1.2)
    c.rect(MARGIN, MARGIN, INNER_W, INNER_H)
    c.setStrokeColor(ACCENT_LINE)
    c.setLineWidth(0.3)
    c.rect(MARGIN + 3.5, MARGIN + 3.5, INNER_W - 7, INNER_H - 7)


def draw_bg_grid(c):
    c.setStrokeColor(HexColor("#F0EFED"))
    c.setLineWidth(0.12)
    for i in range(1, 12):
        x = MARGIN + (INNER_W / 12) * i
        c.line(x, MARGIN + 22, x, H - MARGIN - 76)
    for i in range(1, 22):
        yy = MARGIN + 22 + (INNER_H - 98) / 22 * i
        c.line(MARGIN + 6, yy, W - MARGIN - 6, yy)


def draw_header(c):
    y_top = H - MARGIN - 3.5
    hh = 62

    c.setFillColor(WARM_BLACK)
    c.rect(MARGIN + 3.5, y_top - hh, INNER_W - 7, hh, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("BigShoulders-Bold", 26)
    c.drawString(MARGIN + 18, y_top - 30, "COMPATIBILITY REPORT")

    # Suit decorations
    suits_x = W - MARGIN - 90
    c.setFont("DejaVu-Bold", 18)
    c.setFillColor(RED)
    c.drawString(suits_x, y_top - 29, "♥")
    c.drawString(suits_x + 20, y_top - 29, "♦")
    c.setFillColor(HexColor("#999999"))
    c.drawString(suits_x + 40, y_top - 29, "♠")
    c.drawString(suits_x + 60, y_top - 29, "♣")

    c.setFont("Jura-Medium", 9)
    c.setFillColor(LIGHT_GRAY)
    c.drawString(MARGIN + 18, y_top - 48, "GRAND LIFE SPREAD  ·  MATHEMATICAL CARDOLOGY  ·  52-CARD SYSTEM")

    c.setFont("GeistMono", 8)
    c.setFillColor(MID_GRAY)
    c.drawRightString(W - MARGIN - 18, y_top - 48, "2026-03-14  |  REV 01")

    # Red accent bar
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    c.line(MARGIN + 3.5, y_top - hh, W - MARGIN - 3.5, y_top - hh)

    return y_top - hh


def draw_persons_section(c, y_start):
    """Draw both persons' identity blocks side by side."""
    y = y_start - 18

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "§01  SUBJECTS")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 100, y + 3, W - MARGIN - 14, y + 3)

    y -= 32
    x = MARGIN + 14
    mid = MARGIN + INNER_W / 2

    # ── Person 1 ──
    # Light background card
    c.setFillColor(FAINT_RED)
    c.roundRect(x - 4, y - 32, (INNER_W / 2) - 16, 62, 4, fill=1, stroke=0)

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(x + 6, y + 18, "PERSON 1")

    # Big card
    draw_big_card(c, x + 6, y - 14, "8♦", rank_size=30, suit_size=22)

    # Info
    lx = x + 56
    c.setFont("InstrumentSans-Bold", 11)
    c.setFillColor(WARM_BLACK)
    c.drawString(lx, y + 6, "8")
    c.setFont("DejaVu-Bold", 10)
    c.setFillColor(RED)
    c.drawString(lx + 9, y + 6, "♦")

    c.setFont("GeistMono", 9)
    c.setFillColor(BODY_TEXT)
    c.drawString(lx + 24, y + 6, "Birth Card")

    c.setFont("GeistMono", 9)
    c.setFillColor(BODY_TEXT)
    c.drawString(lx, y - 8, "Born: 2/17/1991")

    # ── Person 2 ──
    p2x = mid + 8
    c.setFillColor(FAINT_BLACK)
    c.roundRect(p2x - 4, y - 32, (INNER_W / 2) - 16, 62, 4, fill=1, stroke=0)

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(p2x + 6, y + 18, "PERSON 2")

    draw_big_card(c, p2x + 6, y - 14, "5♣", rank_size=30, suit_size=22)

    lx2 = p2x + 56
    c.setFont("InstrumentSans-Bold", 11)
    c.setFillColor(WARM_BLACK)
    c.drawString(lx2, y + 6, "5")
    c.setFont("DejaVu-Bold", 10)
    c.setFillColor(WARM_BLACK)
    c.drawString(lx2 + 9, y + 6, "♣")

    c.setFont("GeistMono", 9)
    c.setFillColor(BODY_TEXT)
    c.drawString(lx2 + 24, y + 6, "Birth Card")

    c.setFont("GeistMono", 9)
    c.setFillColor(BODY_TEXT)
    c.drawString(lx2, y - 8, "Born: 12/13/1987")

    # Connector line between the two
    c.setStrokeColor(ACCENT_LINE)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.line(mid - 8, y + 22, mid - 8, y - 32)
    c.setDash()

    return y - 44


def draw_relation_block(c, y_start, section_num, title, subtitle,
                        position_label, position_val, context_text,
                        person_card, target_card, is_empty=False):
    """Draw a single relationship direction block."""
    y = y_start - 10

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, f"§0{section_num}  {title}")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 14 + c.stringWidth(f"§0{section_num}  {title}", "Outfit-Bold", 9) + 10,
           y + 3, W - MARGIN - 14, y + 3)

    y -= 22
    x = MARGIN + 14

    # Subtitle
    c.setFont("Jura-Medium", 9.5)
    c.setFillColor(BODY_TEXT)
    c.drawString(x, y, subtitle)

    y -= 28

    if is_empty:
        # Empty state — card not found
        c.setFillColor(FAINT_BLACK)
        c.roundRect(x - 2, y - 20, INNER_W - 18, 44, 3, fill=1, stroke=0)

        # Left: person card
        draw_card_chip(c, x + 8, y + 4, person_card, size=10, chip_w=36, chip_h=20)

        # Arrow with X
        c.setFont("GeistMono", 12)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(x + 54, y + 4, "→")
        c.setFont("GeistMono-Bold", 10)
        c.setFillColor(RED)
        c.drawString(x + 70, y + 4, "✗")

        # Target card
        draw_card_chip(c, x + 88, y + 4, target_card, size=10, chip_w=36, chip_h=20)

        # Message
        c.setFont("Jura-Medium", 10)
        c.setFillColor(BODY_TEXT)
        c.drawString(x + 138, y + 6, "Does not appear in Life Path.")
        c.setFont("Jura-Light", 9)
        c.setFillColor(DARK_GRAY)
        c.drawString(x + 138, y - 6, "No direct positional connection found.")

        return y - 30

    # Active state — position found
    c.setFillColor(FAINT_RED)
    c.roundRect(x - 2, y - 24, INNER_W - 18, 52, 3, fill=1, stroke=0)
    # Left accent bar
    c.setFillColor(RED)
    c.rect(x - 2, y - 24, 2.5, 52, fill=1, stroke=0)

    # Left: person card → target card
    draw_card_chip(c, x + 10, y + 8, person_card, size=10, chip_w=36, chip_h=20)
    c.setFont("GeistMono", 12)
    c.setFillColor(ACCENT_LINE)
    c.drawString(x + 56, y + 10, "→")
    draw_card_chip(c, x + 76, y + 8, target_card, size=10, chip_w=36, chip_h=20)

    # Position badge
    c.setFillColor(RED)
    c.roundRect(x + 124, y + 8, 90, 18, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("GeistMono-Bold", 8)
    c.drawCentredString(x + 169, y + 12, position_label)

    # Description
    c.setFont("Jura-Medium", 10)
    c.setFillColor(BODY_TEXT)
    c.drawString(x + 226, y + 12, position_val)

    # Context line
    c.setFont("Jura-Light", 9.5)
    c.setFillColor(BODY_TEXT)
    c.drawString(x + 10, y - 8, context_text)

    return y - 34


def draw_summary_section(c, y_start):
    """Draw the Aligned Goals / Friction Desk summary."""
    y = y_start - 10

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "§04  SUMMARY")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 100, y + 3, W - MARGIN - 14, y + 3)

    y -= 28
    x = MARGIN + 14
    mid = MARGIN + INNER_W / 2

    # Aligned Goals box
    box_w = (INNER_W / 2) - 20
    box_h = 56

    c.setStrokeColor(WARM_BLACK)
    c.setLineWidth(0.6)
    c.setFillColor(FAINT_BLACK)
    c.roundRect(x, y - box_h + 20, box_w, box_h, 4, fill=1, stroke=1)

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(x + 12, y + 4, "ALIGNED GOALS")

    c.setFont("BigShoulders-Bold", 20)
    c.setFillColor(WARM_BLACK)
    c.drawString(x + 12, y - 18, "Natural Balance")

    # Small decorative line
    c.setStrokeColor(WARM_BLACK)
    c.setLineWidth(1)
    c.line(x + 12, y - 24, x + 60, y - 24)

    # Friction Desk box
    fx = mid + 4
    c.setStrokeColor(RED)
    c.setLineWidth(0.6)
    c.setFillColor(FAINT_RED)
    c.roundRect(fx, y - box_h + 20, box_w, box_h, 4, fill=1, stroke=1)

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(fx + 12, y + 4, "FRICTION DESK")

    c.setFont("BigShoulders-Bold", 20)
    c.setFillColor(RED)
    c.drawString(fx + 12, y - 18, "Low Conflict")

    c.setStrokeColor(RED)
    c.setLineWidth(1)
    c.line(fx + 12, y - 24, fx + 60, y - 24)

    return y - box_h - 10


def draw_visual_map(c, y_start):
    """Draw a visual relationship diagram between the two cards."""
    y = y_start - 10

    c.setFont("Outfit-Bold", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "§05  RELATIONSHIP MAP")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 160, y + 3, W - MARGIN - 14, y + 3)

    y -= 36
    center_x = MARGIN + INNER_W / 2
    x = MARGIN + 14

    # Person 1 node
    p1x = x + 40
    c.setStrokeColor(RED)
    c.setLineWidth(1)
    c.setFillColor(WHITE)
    c.roundRect(p1x, y - 10, 80, 44, 6, fill=1, stroke=1)
    c.setFont("Outfit-Bold", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(p1x + 40, y + 22, "PERSON 1")
    draw_card_chip(c, p1x + 22, y, "8♦", size=10, chip_w=36, chip_h=18)

    # Person 2 node
    p2x = W - MARGIN - 14 - 120
    c.setStrokeColor(WARM_BLACK)
    c.setLineWidth(1)
    c.setFillColor(WHITE)
    c.roundRect(p2x, y - 10, 80, 44, 6, fill=1, stroke=1)
    c.setFont("Outfit-Bold", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(p2x + 40, y + 22, "PERSON 2")
    draw_card_chip(c, p2x + 22, y, "5♣", size=10, chip_w=36, chip_h=18)

    # Arrow: P1 → P2 (top arrow, with label)
    arrow_y_top = y + 18
    arrow_x1 = p1x + 80
    arrow_x2 = p2x
    mid_arrow = (arrow_x1 + arrow_x2) / 2

    c.setStrokeColor(RED)
    c.setLineWidth(0.8)
    c.line(arrow_x1 + 4, arrow_y_top, arrow_x2 - 4, arrow_y_top)
    # Arrowhead
    c.line(arrow_x2 - 10, arrow_y_top + 4, arrow_x2 - 4, arrow_y_top)
    c.line(arrow_x2 - 10, arrow_y_top - 4, arrow_x2 - 4, arrow_y_top)

    # Label above top arrow
    c.setFont("GeistMono-Bold", 7)
    c.setFillColor(RED)
    c.drawCentredString(mid_arrow, arrow_y_top + 8, "Pos 7 · URANUS")

    # Arrow: P2 → P1 (bottom arrow, with label)
    arrow_y_bot = y - 2
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.6)
    c.setDash(3, 3)
    c.line(arrow_x2 - 4, arrow_y_bot, arrow_x1 + 4, arrow_y_bot)
    c.setDash()
    # X mark instead of arrowhead
    c.setFont("GeistMono-Bold", 8)
    c.setFillColor(LIGHT_GRAY)
    c.drawCentredString(arrow_x1 + 2, arrow_y_bot - 3, "✗")

    c.setFont("GeistMono", 7)
    c.setFillColor(LIGHT_GRAY)
    c.drawCentredString(mid_arrow, arrow_y_bot - 10, "No connection found")

    return y - 34


def draw_footer(c):
    y = MARGIN + 3.5
    c.setStrokeColor(WARM_BLACK)
    c.setLineWidth(0.6)
    c.line(MARGIN + 3.5, y + 16, W - MARGIN - 3.5, y + 16)
    c.setFont("GeistMono", 7)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y + 6, "CARD BLUEPRINTS  ·  MATHEMATICAL CARDOLOGY  ·  52-CARD SOLAR SYSTEM")
    c.drawRightString(W - MARGIN - 14, y + 6, "cardblueprints.com  ·  The math is the math.")


# ── MAIN ───────────────────────────────────────────────
def main():
    out = "/home/claude/compatibility_report.pdf"
    c = canvas.Canvas(out, pagesize=letter)
    c.setTitle("Compatibility Report — 8♦ vs 5♣")
    c.setAuthor("Card Blueprints")

    # Background
    c.setFillColor(BG_CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    draw_bg_grid(c)
    draw_registration_marks(c)
    draw_frame(c)

    y = draw_header(c)
    y = draw_persons_section(c, y)
    hrule(c, y + 4)

    y = draw_relation_block(
        c, y,
        section_num=2,
        title="HOW PERSON 1 RELATES TO PERSON 2",
        subtitle="How 8♦ experiences the 5♣ in the Grand Life Spread",
        position_label="Pos 7 · URANUS",
        position_val="A friendly, variable presence.",
        context_text="Pivotal benefit but unpredictable surprises.",
        person_card="8♦",
        target_card="5♣",
        is_empty=False
    )
    hrule(c, y + 4)

    y = draw_relation_block(
        c, y,
        section_num=3,
        title="HOW PERSON 2 RELATES TO PERSON 1",
        subtitle="How 5♣ experiences the 8♦ in the Grand Life Spread",
        position_label="",
        position_val="",
        context_text="",
        person_card="5♣",
        target_card="8♦",
        is_empty=True
    )
    hrule(c, y + 4)

    y = draw_summary_section(c, y)
    hrule(c, y + 4)

    y = draw_visual_map(c, y)

    draw_footer(c)

    c.save()
    print(f"Done: {out}")


if __name__ == "__main__":
    main()
