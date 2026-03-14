
import os
import sys
import textwrap
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from calculate_blueprint import (
    calculate_blueprint, 
    PLANET_NAMES,
    REL_DYNAMICS,
    get_card_descriptions,
    get_weekly_meanings
)

# Colors
WARM_BLACK = HexColor("#1A1A1A")
RED = HexColor("#C41E3A")
MID_GRAY = HexColor("#777777")
LIGHT_GRAY = HexColor("#E0E0E0")
HAIRLINE_GRAY = HexColor("#F0F0F0")
BG_CREAM = HexColor("#FAFAF8")
GOLD = HexColor("#B8860B") # Accent for Premium

RANK_MEANINGS = {
    "A": "Initiation: New beginnings and concentrated desire toward a single goal.",
    "2": "Cooperation: The need for union, logic, and balanced interaction.",
    "3": "Creativity: Multiple ideas, exploration, but potential for scattered worry.",
    "4": "Stability: Firm foundations, security, and a period of building solid walls.",
    "5": "Expansion: Change, travel, and the restless need for new experiences.",
    "6": "Responsibility: Karmic adjustment, maintaining the status quo, and service.",
    "7": "Spirituality: A non-attachment challenge requiring intuition over logic.",
    "8": "Power: Management, focus, and the consolidation of personal authority.",
    "9": "Completion: A humanitarian cycle of letting go and finishing a major phase.",
    "10": "Success: Culmination of efforts, public recognition, and potential overload.",
    "J": "Youthful Mind: Playful, creative, and sometimes deceptive or immature energy.",
    "Q": "Mastery: Receptive power, nurturing authority, and skillful management.",
    "K": "Authority: Ultimate command, the peak of the suit's energy, and leadership."
}

def get_suit_color(card):
    if any(s in card for s in ["♥", "♦", "H", "D", "\u2665", "\u2666"]):
        return RED
    return WARM_BLACK

def get_rank(card):
    return card.replace("♥","").replace("♦","").replace("♠","").replace("♣","").strip()

def draw_blueprint_extras(c, W, H, m):
    # Registration Marks
    c.setStrokeColor(MID_GRAY)
    c.setLineWidth(0.3)
    off, ln = 0.2*inch, 0.1*inch
    for cx, cy in [(m, H-m), (W-m, H-m), (m, m), (W-m, m)]:
        dx = -1 if cx < W/2 else 1
        dy = -1 if cy < H/2 else 1
        c.line(cx - dx*off, cy, cx - dx*(off+ln), cy)
        c.line(cx, cy - dy*off, cx, cy - dy*(off+ln))
    
    # Frame
    c.setStrokeColor(WARM_BLACK)
    c.setLineWidth(1.2)
    c.rect(m, m, W-2*m, H-2*m)
    c.setStrokeColor(GOLD) # Premium accent
    c.setLineWidth(0.4)
    c.rect(m+3, m+3, W-2*m-6, H-2*m-6)
    
    # Large faintly visible grid
    c.setStrokeColor(HexColor("#F2F2F0"))
    c.setLineWidth(0.15)
    for i in range(1, 12):
        x = m + ((W-2*m)/12)*i
        c.line(x, m, x, H-m)
    for i in range(1, 24):
        yy = m + ((H-2*m)/24)*i
        c.line(m, yy, W-m, yy)

def draw_card_chip(c, x, y, card, size=9, w=34, h=18):
    color = get_suit_color(card)
    c.setStrokeColor(color)
    c.setLineWidth(0.6)
    c.setFillColor(white)
    c.roundRect(x, y - 4, w, h, 3, fill=1, stroke=1)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawCentredString(x + w/2, y, card)

def draw_premium_header(c, title, rev, W, H, m, target_date):
    c.setFillColor(WARM_BLACK)
    c.rect(m+3, H-m-65, W-2*m-6, 62, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(m + 20, H - m - 30, title)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(LIGHT_GRAY)
    c.drawString(m + 20, H - m - 45, f"TEMPORAL SYNCHRONIZATION ANALYSIS  \u00b7  {target_date.isoformat()}  \u00b7  {rev}")
    
    # Gold divider line
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(m+3, H-m-65, W-m-3, H-m-65)

def analyze_temporal_bridge(p1_periods, p2_periods):
    """Explains the shared pressure of planetary periods."""
    interpretations = []
    for i, planet in enumerate(PLANET_NAMES):
        c1, c2 = p1_periods[i], p2_periods[i]
        r1, r2 = get_rank(c1), get_rank(c2)
        
        pressure = "Divergent Intent"
        if r1 == r2:
            pressure = "Harmonic Intensity (Shared Numerical Frequency)"
        elif r1 in ["K","Q","J"] and r2 in ["K","Q","J"]:
            pressure = "Power Dynamic (Court Card Collision)"
        
        interpretations.append({
            "planet": planet,
            "c1": c1, "c2": c2,
            "pressure": pressure,
            "intent": f"Managing {planet} energy through {r1} & {r2} frequencies."
        })
    return interpretations

def generate_premium_report(p1_data, p2_data, target_date, out_path):
    c = canvas.Canvas(out_path, pagesize=letter)
    W, H = letter
    m = 0.55 * inch
    
    # -- PAGE 1: INDIVIDUAL ESSENCE & NUMERICAL ALIGNMENT --
    c.setFillColor(BG_CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_blueprint_extras(c, W, H, m)
    draw_premium_header(c, "MID-TICKET PROFESSIONAL AUDIT", "REV 04 / SEC I", W, H, m, target_date)
    
    y = H - m - 90
    
    # Essence Section
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(m+15, y, "\u00a7 01  THE INDIVIDUAL ESSENCES")
    y -= 25

    def draw_person_essence(px, person_data, label):
        nonlocal y
        c.setFillColor(WARM_BLACK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(px, y, label)
        y_loc = y - 20
        
        for anchor_type in ["BC", "PRC"]:
            src = person_data[anchor_type]
            if src["anchor"] == "?": continue
            
            draw_card_chip(c, px, y_loc, src["anchor"])
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(WARM_BLACK)
            c.drawString(px + 40, y_loc + 3, f"{anchor_type} Archetype")
            
            # Get real description
            info = get_card_descriptions().get(src["anchor"], {})
            title = info.get("title", "Significant Identity")
            c.setFont("Helvetica-Oblique", 7)
            c.setFillColor(MID_GRAY)
            wrapped = textwrap.fill(f"{title}", width=40)
            c.drawString(px + 40, y_loc - 6, wrapped)
            
            y_loc -= 30
        return y_loc

    p1_Essence_Y = draw_person_essence(m + 20, p1_data, "PERSON 1: CORE FREQUENCY")
    p2_Essence_Y = draw_person_essence(W/2 + 10, p2_data, "PERSON 2: CORE FREQUENCY")
    y = min(p1_Essence_Y, p2_Essence_Y) - 20
    
    # Numerical Alignment
    c.setStrokeColor(HAIRLINE_GRAY)
    c.line(m+20, y+10, W-m-20, y+10)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(m+15, y, "\u00a7 02  NUMERICAL ALIGNMENT (Shared Ranks)")
    y -= 20
    
    def get_all_ranks(person_data):
        ranks = set()
        for b in [person_data["BC"], person_data["PRC"]]:
            if b["anchor"] == "?": continue
            for k in ["anchor", "long_range", "pluto", "result", "env", "disp"]:
                ranks.add(get_rank(b[k]))
        return ranks

    r1, r2 = get_all_ranks(p1_data), get_all_ranks(p2_data)
    shared = r1.intersection(r2)
    
    if shared:
        for r in sorted(list(shared)):
            c.setFillColor(GOLD)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(m+30, y, f"RANK {r}")
            c.setFont("Helvetica", 8)
            c.setFillColor(WARM_BLACK)
            meaning = RANK_MEANINGS.get(r, "Unique combination of forces.")
            wrapped = textwrap.fill(meaning, width=80)
            for line in wrapped.split('\n'):
                c.drawString(m+80, y, line)
                y -= 10
            y -= 5
    else:
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(MID_GRAY)
        c.drawString(m+30, y, "No shared numerical anchors in main cards.")
        y -= 20

    # -- PAGE 2: THE TEMPORAL BRIDGE (7 PERIODS) --
    c.showPage()
    c.setFillColor(BG_CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_blueprint_extras(c, W, H, m)
    draw_premium_header(c, "MID-TICKET PROFESSIONAL AUDIT", "REV 04 / SEC II", W, H, m, target_date)
    
    y = H - m - 90
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(m+15, y, "\u00a7 03  THE TEMPORAL BRIDGE (52-Day Synchronization)")
    y -= 10
    
    c.setFont("Helvetica", 7)
    c.setFillColor(MID_GRAY)
    instr = "Auditing the 7 Planetary Periods for both subjects simultaneously to identify timing pressure."
    c.drawString(m+15, y, instr)
    y -= 25
    
    # Headers
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(MID_GRAY)
    c.drawString(m+30, y, "PLANET")
    c.drawString(m+95, y, "P1 CARD")
    c.drawString(m+145, y, "P2 CARD")
    c.drawString(m+200, y, "PULSE / PRESSURE")
    y -= 15
    
    bridge = analyze_temporal_bridge(p1_data["BC"]["periods"], p2_data["BC"]["periods"])
    for b in bridge:
        c.setStrokeColor(LIGHT_GRAY)
        c.line(m+25, y+10, W-m-25, y+10)
        
        c.setFillColor(WARM_BLACK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(m+30, y, b["planet"])
        
        draw_card_chip(c, m+90, y, b["c1"], size=8, w=30, h=16)
        draw_card_chip(c, m+140, y, b["c2"], size=8, w=30, h=16)
        
        c.setFillColor(RED if "Harmonic" in b["pressure"] else WARM_BLACK)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(m+200, y+4, b["pressure"])
        
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 7)
        c.drawString(m+200, y-5, b["intent"])
        
        y -= 35
        
    # Final Summary footer
    y = m + 40
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(m+20, y, W-m-20, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(WARM_BLACK)
    c.drawCentredString(W/2, y - 15, "PROPRIETARY ARCHITECTURAL COMPARISON MATRIX")
    
    c.save()

if __name__ == "__main__":
    if len(sys.argv) < 7:
        sys.exit(0)
    
    m1, d1, y1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    m2, d2, y2 = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    
    from datetime import datetime
    target_dt = datetime.strptime(sys.argv[7], "%Y-%m-%d").date() if len(sys.argv) > 7 else date.today()
    
    def build_p_data(m, d, y, t):
        bc_res = calculate_blueprint(m, d, y, target_date=t)
        prc = bc_res["archetype"]["prc"]
        prc_res = calculate_blueprint(m, d, y, target_date=t, anchor_card=prc) if prc != "?" else {"archetype": {"anchor": "?"}}
        
        def bundle(r):
            if r["archetype"]["anchor"] == "?": return {"anchor": "?"}
            return {
                "anchor": r["archetype"]["anchor"],
                "birth_info": r["birth_info"],
                "long_range": r["long_range"],
                "pluto": r["yearly_spread"]["pluto"],
                "result": r["yearly_spread"]["result"],
                "env": r["environment_displacement"]["environment"],
                "disp": r["environment_displacement"]["displacement"],
                "life_path": r["life_path"],
                "periods": r["yearly_spread"]["periods"]
            }
        return {"BC": bundle(bc_res), "PRC": bundle(prc_res)}

    p1_data = build_p_data(m1, d1, y1, target_dt)
    p2_data = build_p_data(m2, d2, y2, target_dt)
    
    out_file = f"Premium_Deep_Dive_{m1}_{d1}_{y1}_vs_{m2}_{d2}_{y2}.pdf"
    output_path = os.path.join(os.getcwd(), "outputs", out_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    generate_premium_report(p1_data, p2_data, target_dt, output_path)
    print(f"Premium Report Generated: {output_path}")

