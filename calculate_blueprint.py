#!/usr/bin/env python3
"""
Card Blueprints — Core Calculation Engine

Takes a birthday (month, day, year) and a target date, and performs
the core Cardology calculations based on the Grand Life Spread (Spread 1).
"""

import json
import os
import sys
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'card_blueprints_data.json')
_DATA = None

def init_data():
    global _DATA
    if _DATA is not None: return
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found at {DATA_FILE}"); sys.exit(1)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        _DATA = json.load(f)

def get_data(section):
    init_data(); return _DATA.get(section, {})

def get_spreads(): return get_data('yearly_spreads')
def get_card_descriptions(): return get_data('card_descriptions')
def get_weekly_meanings(): return get_data('weekly_card_meanings')

# ---------------------------------------------------------------------------
# Constants & Reference Data
# ---------------------------------------------------------------------------

SOLAR_TO_CARD = {
    0: "Joker",
    1: "A♥", 2: "2♥", 3: "3♥", 4: "4♥", 5: "5♥", 6: "6♥", 7: "7♥",
    8: "8♥", 9: "9♥", 10: "10♥", 11: "J♥", 12: "Q♥", 13: "K♥",
    14: "A♣", 15: "2♣", 16: "3♣", 17: "4♣", 18: "5♣", 19: "6♣", 20: "7♣",
    21: "8♣", 22: "9♣", 23: "10♣", 24: "J♣", 25: "Q♣", 26: "K♣",
    27: "A♦", 28: "2♦", 29: "3♦", 30: "4♦", 31: "5♦", 32: "6♦", 33: "7♦",
    34: "8♦", 35: "9♦", 36: "10♦", 37: "J♦", 38: "Q♦", 39: "K♦",
    40: "A♠", 41: "2♠", 42: "3♠", 43: "4♠", 44: "5♠", 45: "6♠", 46: "7♠",
    47: "8♠", 48: "9♠", 49: "10♠", 50: "J♠", 51: "Q♠", 52: "K♠"
}

CARD_TO_SOLAR = {v: k for k, v in SOLAR_TO_CARD.items()}

SUIT_DOMAINS = {
    "♥": "Emotional Patterns",
    "♣": "Behavioral/Intellectual Patterns",
    "♦": "Value/Resource Patterns",
    "♠": "Lifestyle/Transformation Patterns"
}

PLANET_NAMES = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

# Grid layout labels (standard Cardology)
ROW_NAMES = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
COL_NAMES = ["Neptune", "Uranus", "Saturn", "Jupiter", "Mars", "Venus", "Mercury"]

# Relationship Dynamics (from PDF)
REL_DYNAMICS = [
    {"index": 0, "name": "Moon", "tagline": "A supportive, nurturing presence.", "desc": "Supportive and intimate connection."},
    {"index": 1, "name": "Primary Energy", "tagline": "You shine this light.", "desc": "The Birth Card is your core gift."},
    {"index": 2, "name": "Mercury", "tagline": "A close confidant.", "desc": "Strong mental connection; easy to talk to."},
    {"index": 3, "name": "Venus", "tagline": "A lover/dear companion.", "desc": "Inexplicably drawn; Cupid's arrow."},
    {"index": 4, "name": "Mars", "tagline": "Sparks fly/passion heats up.", "desc": "Stimulating but also competitive or confrontational. (High Friction)"},
    {"index": 5, "name": "Jupiter", "tagline": "An expansive influence.", "desc": "Mutual benefit and abundance. (Aligned Goals)"},
    {"index": 6, "name": "Saturn", "tagline": "A teacher or taskmaster.", "desc": "Guide who reminds you of lessons; possible friction/resistance."},
    {"index": 7, "name": "Uranus", "tagline": "A friendly, variable presence.", "desc": "Pivotal benefit but unpredictable surprises."},
    {"index": 8, "name": "Neptune", "tagline": "Object of hopes and fears.", "desc": "Rose-colored glasses; dreamy but potential for shattered illusions."},
    {"index": 9, "name": "Pluto", "tagline": "A shadowy, uneasy presence.", "desc": "Reveals shadow side; can be awkward or invasive."},
    {"index": 10, "name": "The Princess", "tagline": "A possible gift.", "desc": "Appear as a gift when ready to welcome them."},
    {"index": 11, "name": "The Prince", "tagline": "Someone who tests your resolve.", "desc": "Can be irking or frustrating; energetic challenge."},
    {"index": 12, "name": "The Queen", "tagline": "An advocate of your growth.", "desc": "Helps you embody your fullness; supportive role."},
    {"index": 13, "name": "The King", "tagline": "An example for you to follow.", "desc": "Model for greatness but potentially aloof or mysterious."}
]

# ---------------------------------------------------------------------------
# Core Logic
# ---------------------------------------------------------------------------

def get_birth_card(month, day):
    """Calculates birth card and solar value."""
    sv = 55 - (2 * month + day)
    while sv < 0: sv += 52
    if month == 12 and day == 31: sv = 0
    return SOLAR_TO_CARD.get(sv, "Joker"), sv

def get_sun_sign(m, d):
    """Returns (Sign Name, Ruling Planet)"""
    if (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn", "Saturn"
    if (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius", "Uranus"
    if (m == 2 and d >= 19) or (m == 3 and d <= 20): return "Pisces", "Neptune"
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries", "Mars"
    if (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus", "Venus"
    if (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini", "Mercury"
    if (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer", "Neptune"
    if (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo", "Jupiter"
    if (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo", "Mercury"
    if (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra", "Venus"
    if (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio", "Mars"
    if (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius", "Jupiter"
    return "Unknown", None

def get_linear_flow(spread):
    """Linearizes a 49-card grid + 3-card crown into a 52-card list."""
    grid, crown = spread["grid"], spread["crown"]
    flow = []
    # In Cardology, the flow is Row 0 -> Row 6, moving col 6 down to 0
    for r in range(7):
        for c in range(6, -1, -1):
            flow.append(grid[r*7 + c])
    # Crown Line: Mars, Jupiter, Saturn
    flow.extend([crown[2], crown[1], crown[0]]) 
    return flow

def get_life_path(card):
    """
    Extracts the Life Path for a card based on the Grand Life Spread (Spread 1).
    Moon: 1 Right (index - 1)
    Primary: Core Card (index)
    Mercury-King: 1-12 Left (index + 1 to +12)
    """
    init_data()
    spread = get_spreads()["1"] # Grand Life Spread
    flow = get_linear_flow(spread)
    
    try: idx = flow.index(card)
    except ValueError: return [None] * 14
    
    path = []
    # Moon position is idx-1
    path.append(flow[(idx - 1) % 52])
    # Birth Card and onwards
    for offset in range(0, 13):
        path.append(flow[(idx + offset) % 52])
    return path

def calculate_blueprint(month, day, year, target_date=None, anchor_card=None):
    """
    Calculates all necessary data for a Card Blueprint.
    Includes Archetype, Timing, Yearly Spread, Active Period, Long Range, Karma, and Navigation.
    If anchor_card is provided, it calculates for that card instead of the Birth Card.
    """
    if not target_date: target_date = date.today()
    bc, sv = get_birth_card(month, day)
    
    # Use anchor_card if provided (e.g. for PRC analysis)
    anchor = anchor_card if anchor_card else bc
    
    bday_this_year = date(target_date.year, month, day)
    age = target_date.year - year - (1 if target_date < bday_this_year else 0)
    spread_year = max(0, min(90, age + 1))
    
    # Load Spreads
    spirit = get_spreads()["0"]
    y1 = get_spreads()["1"]
    current_spread = get_spreads().get(str(spread_year))
    
    # Yearly Spread Cards (Mercury through Result)
    current_flow = get_linear_flow(current_spread)
    try:
        idx = current_flow.index(anchor)
        # Period cards are idx+1 to idx+9
        period_cards = [current_flow[(idx + i) % 52] for i in range(1, 10)]
    except ValueError: period_cards = ["?"] * 9
    
    # Grid Position in current spread
    try:
        grid_idx = current_spread["grid"].index(anchor)
        grid_pos = {"row": ROW_NAMES[grid_idx // 7], "col": COL_NAMES[grid_idx % 7]}
    except ValueError: grid_pos = None
    
    # Active Period
    last_bday = bday_this_year if target_date >= bday_this_year else date(target_date.year-1, month, day)
    days_in = (target_date - last_bday).days
    p_idx = min(6, days_in // 52)
    
    # Long Range (7-year cycle)
    lr_cycle = age // 7
    lr_pos = age % 7
    lr_spread_key = str(lr_cycle + 1)
    lr_spread = get_spreads().get(lr_spread_key)
    lr_card = "?"
    if lr_spread:
        lr_flow = get_linear_flow(lr_spread)
        try:
            l_idx = lr_flow.index(anchor)
            lr_card = lr_flow[(l_idx + lr_pos + 1) % 52]
        except ValueError: pass
        
    # Environment & Displacement
    # These typically use the Spirit Spread (0) as the reference
    def get_pos_info(c, s):
        try: return ("grid", s["grid"].index(c))
        except: 
            try: return ("crown", s["crown"].index(c))
            except: return None
    def get_at_pos(p, s):
        if p[0] == "grid": return s["grid"][p[1]]
        return s["crown"][p[1]]
        
    spirit_pos = get_pos_info(anchor, spirit)
    current_pos = get_pos_info(anchor, current_spread)
    
    env = get_at_pos(spirit_pos, current_spread) if spirit_pos else "?"
    disp = get_at_pos(current_pos, spirit) if current_pos else "?"
    
    # Lifetime Karma (Year 1 Environment/Displacement)
    y1_bc_pos = get_pos_info(anchor, y1)
    supp = get_at_pos(spirit_pos, y1) if spirit_pos else "?"
    chall = get_at_pos(y1_bc_pos, spirit) if y1_bc_pos else "?"

    # Suit and Domain
    suit = anchor[-1]
    domain = SUIT_DOMAINS.get(suit, "Unknown")

    # Sign & PRC for the birth person (always based on birth date)
    sign, r_planet = get_sun_sign(month, day)
    lp_y1_bc = get_life_path(bc) # Core life path for the birth card
    prc = "?"
    if r_planet in PLANET_NAMES:
        planet_pos = PLANET_NAMES.index(r_planet)
        prc = lp_y1_bc[planet_pos + 2] if len(lp_y1_bc) > planet_pos + 2 else "?"

    # Purpose from card descriptions
    desc = get_card_descriptions()
    anchor_desc = desc.get(anchor, {})
    purpose = anchor_desc.get("life_direction", "")

    # Long Range as structured dict
    lr_planet = PLANET_NAMES[lr_pos] if lr_pos < len(PLANET_NAMES) else "?"
    long_range = {
        "card": lr_card,
        "cycle": lr_cycle,
        "spread": int(lr_spread_key),
        "planet": lr_planet
    }

    return {
        "archetype": {
            "anchor": anchor,
            "birth_card": bc,
            "solar_value": sv,
            "prc": prc,
            "sun_sign": sign,
            "ruling_planet": r_planet,
            "domain": domain,
            "purpose": purpose,
        },
        "timing": {
            "birth_date": f"{month}/{day}/{year}",
            "target_date": target_date.isoformat(),
            "age": age,
            "spread_year": spread_year,
            "crown_line": current_spread["crown"]
        },
        "yearly_spread": {
            "anchor": anchor,
            "grid_position": grid_pos,
            "periods": period_cards, # Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Result
            "pluto": period_cards[7] if len(period_cards) > 7 else "?",
            "result": period_cards[8] if len(period_cards) > 8 else "?"
        },
        "active_period": {
            "planet": PLANET_NAMES[p_idx],
            "day_in_year": days_in + 1,
            "card": period_cards[p_idx] if p_idx < len(period_cards) else "?"
        },
        "long_range": long_range,
        "environment_displacement": {
            "environment": env,
            "displacement": disp
        },
        "lifetime_karma": {
            "supporting": supp,
            "challenge": chall
        },
        "navigation": {
            "formula": f"{anchor} + {period_cards[p_idx]} + {PLANET_NAMES[p_idx]}" if p_idx < len(period_cards) else "?",
            "all_7_cards": period_cards[:7]
        },
        "life_path": get_life_path(anchor),
        "life_path_prc": get_life_path(prc) if prc != "?" else [None]*14,
        "birth_info": {"m": month, "d": day, "y": year}
    }

def calculate_compatibility(p1, p2):
    """Calculates compatibility based on the Grand Life Spread (Spread 1)."""
    
    def analyze(main_anchor_path, target_bc):
        pos = -1
        if target_bc and target_bc in main_anchor_path: 
            pos = main_anchor_path.index(target_bc)
        aligned = [REL_DYNAMICS[pos]["name"]] if pos in [3, 5] else [] # Venus, Jupiter
        friction = [REL_DYNAMICS[pos]["name"]] if pos in [4, 6] else [] # Mars, Saturn
        return {"pos": pos, "dynamic": REL_DYNAMICS[pos] if pos >= 0 else None, "aligned": aligned, "friction": friction}

    # Connections from P1 perspective
    connections_p1 = {
        "bc_to_bc": analyze(p1["life_path"], p2["archetype"]["birth_card"]),
        "bc_to_prc": analyze(p1["life_path"], p2["archetype"]["prc"]),
        "prc_to_bc": analyze(p1["life_path_prc"], p2["archetype"]["birth_card"]),
        "prc_to_prc": analyze(p1["life_path_prc"], p2["archetype"]["prc"])
    }
    
    # Connections from P2 perspective
    connections_p2 = {
        "bc_to_bc": analyze(p2["life_path"], p1["archetype"]["birth_card"]),
        "bc_to_prc": analyze(p2["life_path"], p1["archetype"]["prc"]),
        "prc_to_bc": analyze(p2["life_path_prc"], p1["archetype"]["birth_card"]),
        "prc_to_prc": analyze(p2["life_path_prc"], p1["archetype"]["prc"])
    }

    return {
        "connections_p1": connections_p1,
        "connections_p2": connections_p2,
        "is_karma_bc": p2["archetype"]["birth_card"] == p1["life_path"][0],
        "is_karma_prc": p2["archetype"]["prc"] == p1["life_path"][0] if p2["archetype"]["prc"] != "?" else False
    }

# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from report_maker import create_standard_report, create_compatibility_report
    import argparse

    parser = argparse.ArgumentParser(description="Card Blueprint Engine")
    parser.add_argument("m", type=int, help="Birth Month")
    parser.add_argument("d", type=int, help="Birth Day")
    parser.add_argument("y", type=int, help="Birth Year")
    parser.add_argument("m2", type=int, nargs="?", help="Second Birth Month (Compatibility)")
    parser.add_argument("d2", type=int, nargs="?", help="Second Birth Day (Compatibility)")
    parser.add_argument("y2", type=int, nargs="?", help="Second Birth Year (Compatibility)")
    parser.add_argument("--report", action="store_true", help="Save report to file")
    parser.add_argument("--target", help="Target Date (YYYY-MM-DD)", default=None)

    args = parser.parse_args()
    
    target_dt = None
    if args.target:
        try:
            target_dt = datetime.strptime(args.target, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid target date format. Use YYYY-MM-DD.")
            sys.exit(1)

    res1 = calculate_blueprint(args.m, args.d, args.y, target_date=target_dt)
    t_str = target_dt.isoformat() if target_dt else date.today().isoformat()
    
    if args.m2 and args.d2 and args.y2:
        res2 = calculate_blueprint(args.m2, args.d2, args.y2, target_date=target_dt)
        comp = calculate_compatibility(res1, res2)
        
        if args.report:
            fname = f"Compatibility_{args.m}_{args.d}_{args.y}_vs_{args.m2}_{args.d2}_{args.y2}_{t_str}.txt"
            print(create_compatibility_report(res1, res2, comp, filename=fname))
        else:
            print(create_compatibility_report(res1, res2, comp))
    else:
        if args.report:
            fname = f"Blueprint_{args.m}_{args.d}_{args.y}_{t_str}.txt"
            print(create_standard_report(res1, filename=fname))
        else:
            print(create_standard_report(res1))
