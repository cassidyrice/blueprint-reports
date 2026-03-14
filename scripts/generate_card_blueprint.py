#!/usr/bin/env python3
"""
Card Blueprint Report — Print-Ready PDF v2
Architectural/blueprint aesthetic. Red for ♥/♦, black for ♠/♣.
Uses DejaVu Sans Mono for suit symbols (full Unicode support).
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
# DejaVu for suit symbols
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

W, H = letter
MARGIN = 0.55 * inch
INNER_W = W - 2 * MARGIN
INNER_H = H - 2 * MARGIN


def suit_color(card_str):
    if "\u2665" in card_str or "\u2666" in card_str:
        return RED
    return WARM_BLACK


def get_suit(card_str):
    for ch in card_str:
        if ch in "\u2665\u2666\u2660\u2663":
            return ch
    return ""


def get_rank(card_str):
    return card_str.replace("\u2665", "").replace("\u2666", "").replace("\u2660", "").replace("\u2663", "")


def draw_card_chip(c, x, y, card, size=9, chip_w=32, chip_h=17):
    """Draw a card inside a rounded rectangle chip."""
    color = suit_color(card)
    rank = get_rank(card)
    suit = get_suit(card)

    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.setFillColor(WHITE)
    c.roundRect(x, y - 4, chip_w, chip_h, 2.5, fill=1, stroke=1)

    # Rank in GeistMono-Bold, suit in DejaVu
    c.setFillColor(color)
    # Calculate centering
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


def draw_suit_text(c, x, y, card, font="GeistMono-Bold", size=9):
    """Draw card text with proper suit rendering."""
    color = suit_color(card)
    rank = get_rank(card)
    suit = get_suit(card)
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, rank)
    rw = c.stringWidth(rank, font, size)
    c.setFont("DejaVu-Bold", size - 0.5)
    c.drawString(x + rw, y, suit)
    return rw + c.stringWidth(suit, "DejaVu-Bold", size - 0.5)


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
    hh = 56

    c.setFillColor(WARM_BLACK)
    c.rect(MARGIN + 3.5, y_top - hh, INNER_W - 7, hh, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("BigShoulders-Bold", 28)
    c.drawString(MARGIN + 18, y_top - 27, "CARD BLUEPRINT")

    # Suit decorations
    suits_x = W - MARGIN - 90
    c.setFont("DejaVu-Bold", 18)
    c.setFillColor(RED)
    c.drawString(suits_x, y_top - 26, "\u2665")
    c.drawString(suits_x + 20, y_top - 26, "\u2666")
    c.setFillColor(HexColor("#999999"))
    c.drawString(suits_x + 40, y_top - 26, "\u2660")
    c.drawString(suits_x + 60, y_top - 26, "\u2663")

    c.setFont("Jura-Light", 7.5)
    c.setFillColor(LIGHT_GRAY)
    c.drawString(MARGIN + 18, y_top - 44, "SOLAR YEAR ANALYSIS  \u00b7  MATHEMATICAL CARDOLOGY  \u00b7  52-CARD SYSTEM")

    c.setFont("GeistMono", 6.5)
    c.setFillColor(MID_GRAY)
    c.drawRightString(W - MARGIN - 18, y_top - 44, "2026-03-14  |  REV 01")

    # Red accent bar
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    c.line(MARGIN + 3.5, y_top - hh, W - MARGIN - 3.5, y_top - hh)

    return y_top - hh


def draw_archetype(c, y_start):
    y = y_start - 12

    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "\u00a701  ARCHETYPE")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 100, y + 2.5, W - MARGIN - 14, y + 2.5)

    y -= 24

    # Birth card big display
    x = MARGIN + 14
    c.setFont("BigShoulders-Bold", 30)
    c.setFillColor(WARM_BLACK)
    c.drawString(x, y - 2, "5")
    c.setFont("DejaVu-Bold", 23)
    c.drawString(x + 22, y + 1, "\u2663")

    # Labels
    lx = x + 54
    c.setFont("InstrumentSans-Bold", 9.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(lx, y + 10, "BIRTH CARD")
    c.setFont("GeistMono", 7)
    c.setFillColor(MID_GRAY)
    c.drawString(lx, y - 1, "Solar Value: 18")
    c.setFont("Jura-Light", 7)
    c.setFillColor(WARM_BLACK)
    c.drawString(lx, y - 12, "Domain: Behavioral / Intellectual Patterns")

    # Divider
    div_x = MARGIN + 240
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.3)
    c.line(div_x, y + 16, div_x, y - 18)

    # Timing
    tx = div_x + 12
    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(tx, y + 10, "TIMING")

    pairs = [("Birth Date", "12/13/1987"), ("Target Date", "2026-03-14"), ("Age / Year", "38 / 39")]
    c.setFont("GeistMono", 7)
    dy = y - 2
    for label, val in pairs:
        c.setFillColor(MID_GRAY)
        c.drawString(tx, dy, label)
        c.setFillColor(WARM_BLACK)
        c.drawString(tx + 100, dy, val)
        dy -= 11

    # Crown Line
    cx = W - MARGIN - 130
    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(cx, y + 10, "CROWN LINE")

    crown = [("K", "\u2660"), ("2", "\u2666"), ("3", "\u2665")]
    chip_x = cx
    chip_y = y - 8
    for rank, suit in crown:
        draw_card_chip(c, chip_x, chip_y, rank + suit, size=9, chip_w=32, chip_h=17)
        chip_x += 38

    return y - 28


def draw_period_row(c, x, y, planet, card, d1, d2="", active=False):
    row_h = 34 if d2 else 26

    if active:
        c.setFillColor(FAINT_RED)
        c.roundRect(x - 2, y - row_h + 12, INNER_W - 18, row_h, 2, fill=1, stroke=0)
        c.setFillColor(RED)
        c.rect(x - 2, y - row_h + 12, 2.5, row_h, fill=1, stroke=0)

    # Planet
    c.setFont("Outfit-Bold" if active else "Outfit", 7.5)
    c.setFillColor(RED if active else MID_GRAY)
    c.drawString(x + 6, y, planet.upper())

    # Arrow
    c.setFont("GeistMono", 6.5)
    c.setFillColor(LIGHT_GRAY)
    c.drawString(x + 62, y, "\u2192")

    # Card chip
    draw_card_chip(c, x + 78, y, card, size=8, chip_w=30, chip_h=15)

    badge_offset = 0
    if active:
        c.setFillColor(RED)
        c.roundRect(x + 114, y - 1, 38, 11, 2, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("GeistMono-Bold", 5)
        c.drawCentredString(x + 133, y + 1, "ACTIVE")
        badge_offset = 44

    desc_x = x + 116 + badge_offset
    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(desc_x, y, d1)
    if d2:
        c.drawString(desc_x, y - 10, d2)

    return y - row_h


def draw_yearly_spread(c, y_start):
    y = y_start - 6

    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    lbl = "\u00a702  YEARLY SPREAD"
    c.drawString(MARGIN + 14, y, lbl)

    # 5♣ label after section title
    lbl_w = c.stringWidth(lbl, "Outfit-Bold", 7.5)
    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(MARGIN + 14 + lbl_w + 4, y, " \u00b7  5")
    c.setFont("DejaVu-Bold", 7)
    c.setFillColor(WARM_BLACK)
    c.drawString(MARGIN + 14 + lbl_w + 30, y, "\u2663")

    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 14 + lbl_w + 42, y + 2.5, W - MARGIN - 14, y + 2.5)

    c.setFont("GeistMono", 6)
    c.setFillColor(MID_GRAY)
    c.drawRightString(W - MARGIN - 14, y, "Grid: Row=Saturn  Col=Mars")

    y -= 16
    x = MARGIN + 14

    periods = [
        ("Mercury", "10\u2663", "Sudden success at school, in teaching or giving a talk.", "An overnight success in the communications fields.", False),
        ("Venus", "9\u2665", "Divorce, ending of a relationship, disappointment over", "relationships or finances.", True),
        ("Mars", "A\u2666", "An aggressive pursuit of money, a new money idea", "related to men or a legal matter.", False),
        ("Jupiter", "5\u2665", "A financially beneficial divorce or separation or", "change in the business, a successful business.", False),
        ("Saturn", "6\u2663", "No changes in health conditions, difficulty in", "following intuition, difficult compromises.", False),
        ("Uranus", "4\u2665", "A spiritual, unusual or unexpected romance or marriage,", "a period of satisfaction in love.", False),
        ("Neptune", "4\u2666", "Contentment with money related to travel, foreign", "interests, psychic gifts, or a secret stash.", False),
    ]

    for planet, card, d1, d2, active in periods:
        y = draw_period_row(c, x, y, planet, card, d1, d2, active)
        if not active:
            hrule(c, y + 6, x - 2, W - MARGIN - 14)

    return y


def draw_transformation(c, y_start):
    y = y_start - 4

    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "\u00a703  TRANSFORMATION ARC")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 160, y + 2.5, W - MARGIN - 14, y + 2.5)

    y -= 18
    x = MARGIN + 14

    # Pluto
    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x, y, "PLUTO")
    draw_card_chip(c, x + 55, y, "6\u2665", size=8, chip_w=28, chip_h=15)
    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x + 92, y, "I am challenged to make compromises and to take complete")
    c.drawString(x + 92, y - 10, "responsibility in my personal relationships.")

    y -= 26

    # Dashed connector
    c.setStrokeColor(ACCENT_LINE)
    c.setLineWidth(0.4)
    c.setDash(2, 2)
    c.line(x + 69, y + 16, x + 69, y + 6)
    c.setDash()

    # Result
    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x, y, "RESULT")
    draw_card_chip(c, x + 55, y, "5\u2666", size=8, chip_w=28, chip_h=15)
    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x + 92, y, "The result is a totally new me, perhaps with a new job,")
    c.drawString(x + 92, y - 10, "relationship or place to live.")

    return y - 18


def draw_long_range(c, y_start):
    y = y_start - 2

    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "\u00a704  LONG RANGE")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 110, y + 2.5, W - MARGIN - 14, y + 2.5)

    y -= 24
    x = MARGIN + 14

    # Big A♥
    c.setFont("BigShoulders-Bold", 28)
    c.setFillColor(RED)
    c.drawString(x, y - 2, "A")
    c.setFont("DejaVu-Bold", 21)
    c.drawString(x + 19, y + 1, "\u2665")

    lx = x + 48
    c.setFont("InstrumentSans-Bold", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(lx, y + 8, "LONG RANGE CARD")
    c.setFont("GeistMono", 6.5)
    c.setFillColor(MID_GRAY)
    c.drawString(lx, y - 2, "Cycle 5  \u00b7  Spread 6  \u00b7  Jupiter")
    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(lx, y - 13, "A desire for love and affection, initiating new love")
    c.drawString(lx, y - 23, "relationships and love affairs, the birth of a child.")

    return y - 30


def draw_env_disp(c, y_start):
    y = y_start - 2

    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "\u00a705  ENVIRONMENT & DISPLACEMENT")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 218, y + 2.5, W - MARGIN - 14, y + 2.5)

    y -= 18
    x = MARGIN + 14
    mid = MARGIN + INNER_W / 2

    # Environment
    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x, y, "ENVIRONMENT")
    draw_card_chip(c, x + 82, y, "J\u2666", size=8, chip_w=28, chip_h=15)
    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x, y - 14, "\"Who moved into your house.\" My ability to promote myself,")
    c.drawString(x, y - 24, "my products and services are the greatest blessings.")

    # Divider
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.3)
    c.line(mid - 6, y + 6, mid - 6, y - 28)

    # Displacement
    dx = mid + 8
    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(dx, y, "DISPLACEMENT")
    draw_card_chip(c, dx + 90, y, "5\u2666", size=8, chip_w=28, chip_h=15)
    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(dx, y - 14, "\"Landlord where you moved.\"")

    return y - 32


def draw_active_period(c, y_start):
    y = y_start - 2

    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "\u00a706  ACTIVE PERIOD")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 120, y + 2.5, W - MARGIN - 14, y + 2.5)

    y -= 14
    x = MARGIN + 14
    box_w = INNER_W - 18
    box_h = 28

    c.setStrokeColor(RED)
    c.setLineWidth(0.8)
    c.setFillColor(FAINT_RED)
    c.roundRect(x - 2, y - box_h + 12, box_w, box_h, 3, fill=1, stroke=1)

    c.setFont("Outfit-Bold", 8.5)
    c.setFillColor(RED)
    c.drawString(x + 8, y, "VENUS")
    c.setFont("Jura-Light", 6)
    c.setFillColor(WARM_BLACK)
    c.drawString(x + 8, y - 11, "Relationships, values, love")

    # Card centered
    mid_x = MARGIN + INNER_W / 2 - 12
    c.setFont("GeistMono-Bold", 13)
    c.setFillColor(RED)
    c.drawString(mid_x, y - 4, "9")
    c.setFont("DejaVu-Bold", 12)
    c.drawString(mid_x + 10, y - 4, "\u2665")

    c.setFont("GeistMono", 6.5)
    c.setFillColor(MID_GRAY)
    c.drawRightString(W - MARGIN - 22, y - 2, "Day in Year: 91")

    return y - box_h


def draw_navigation(c, y_start):
    y = y_start - 2

    c.setFont("Outfit-Bold", 7.5)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y, "\u00a707  NAVIGATION & KARMA")
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.4)
    c.line(MARGIN + 162, y + 2.5, W - MARGIN - 14, y + 2.5)

    y -= 16
    x = MARGIN + 14

    # Formula bar
    c.setFillColor(FAINT_BLACK)
    c.roundRect(x - 2, y - 6, INNER_W - 18, 20, 2, fill=1, stroke=0)
    c.setFont("Outfit-Bold", 7)
    c.setFillColor(MID_GRAY)
    c.drawString(x + 4, y + 1, "FORMULA")

    fx = x + 62
    # 5♣
    tw = draw_suit_text(c, fx, y + 1, "5\u2663", "GeistMono-Bold", 9)
    fx += tw + 6
    c.setFont("GeistMono", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(fx, y + 1, "+")
    fx += 14
    # 9♥
    tw = draw_suit_text(c, fx, y + 1, "9\u2665", "GeistMono-Bold", 9)
    fx += tw + 6
    c.setFont("GeistMono", 9)
    c.setFillColor(MID_GRAY)
    c.drawString(fx, y + 1, "+")
    fx += 14
    c.setFont("Outfit-Bold", 9)
    c.setFillColor(RED)
    c.drawString(fx, y + 1, "Venus")

    y -= 24

    # All 7 cards
    c.setFont("Outfit-Bold", 7)
    c.setFillColor(MID_GRAY)
    c.drawString(x, y + 4, "ALL 7 CARDS")

    all_cards = ["10\u2663", "9\u2665", "A\u2666", "5\u2665", "6\u2663", "4\u2665", "4\u2666"]
    card_x = x + 80
    for card in all_cards:
        draw_card_chip(c, card_x, y, card, size=7.5, chip_w=30, chip_h=14)
        card_x += 36

    y -= 22

    # Karma
    c.setFont("Outfit-Bold", 7)
    c.setFillColor(MID_GRAY)
    c.drawString(x, y + 3, "LIFETIME KARMA")

    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x + 96, y + 3, "Challenge")
    draw_card_chip(c, x + 142, y, "5\u2665", size=7.5, chip_w=26, chip_h=14)

    c.setFont("Jura-Medium", 8.5)
    c.setFillColor(WARM_BLACK)
    c.drawString(x + 182, y + 3, "Supporting")
    draw_card_chip(c, x + 232, y, "4\u2663", size=7.5, chip_w=26, chip_h=14)

    return y - 12


def draw_footer(c):
    y = MARGIN + 3.5
    c.setStrokeColor(WARM_BLACK)
    c.setLineWidth(0.6)
    c.line(MARGIN + 3.5, y + 16, W - MARGIN - 3.5, y + 16)
    c.setFont("GeistMono", 5)
    c.setFillColor(MID_GRAY)
    c.drawString(MARGIN + 14, y + 7, "CARD BLUEPRINTS  \u00b7  MATHEMATICAL CARDOLOGY  \u00b7  52-CARD SOLAR SYSTEM")
    c.drawRightString(W - MARGIN - 14, y + 7, "cardblueprints.com  \u00b7  The math is the math.")


# ── MAIN ───────────────────────────────────────────────
def main():
    out = "/home/claude/card_blueprint_report.pdf"
    c = canvas.Canvas(out, pagesize=letter)
    c.setTitle("Card Blueprint \u2014 5\u2663 \u2014 Solar Year 39")
    c.setAuthor("Card Blueprints")

    # Background
    c.setFillColor(BG_CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    draw_bg_grid(c)
    draw_registration_marks(c)
    draw_frame(c)

    y = draw_header(c)
    y = draw_archetype(c, y)
    hrule(c, y)
    y = draw_yearly_spread(c, y)
    hrule(c, y + 3)
    y = draw_transformation(c, y)
    hrule(c, y + 2)
    y = draw_long_range(c, y)
    hrule(c, y + 2)
    y = draw_env_disp(c, y)
    hrule(c, y + 2)
    y = draw_active_period(c, y)
    hrule(c, y + 2)
    y = draw_navigation(c, y)

    draw_footer(c)

    c.save()
    print(f"Done: {out}")
    print(f"Final y position: {y:.0f}, margin bottom: {MARGIN + 20:.0f}")


if __name__ == "__main__":
    main()
