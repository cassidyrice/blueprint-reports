
import os
import sys
import textwrap
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
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
WHITE = HexColor("#FFFFFF")

def get_suit_color(card):
    if any(s in card for s in ["♥", "♦", "H", "D"]):
        return RED
    return WARM_BLACK

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
    c.setLineWidth(1)
    c.rect(m, m, W-2*m, H-2*m)
    
    # Grid
    c.setStrokeColor(HAIRLINE_GRAY)
    c.setLineWidth(0.1)
    for i in range(1, 12):
        x = m + ((W-2*m)/12)*i
        c.line(x, m, x, H-m)
    for i in range(1, 20):
        yy = m + ((H-2*m)/20)*i
        c.line(m, yy, W-m, yy)

def draw_card_chip(c, x, y, card, size=8):
    color = get_suit_color(card)
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.setFillColor(WHITE)
    c.roundRect(x, y - 3, 28, 14, 2, fill=1, stroke=1)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawCentredString(x + 14, y, card)

def get_congruent_challenge(card):
    """Specific interpretation of the Displacement card as a Congruent Challenge."""
    desc = get_card_descriptions().get(card, {}).get("title", "Significant Pressure")
    weekly = get_weekly_meanings().get(card, {}).get("environment", "a transformative catalyst for growth")
    return f"{desc}: Acting as a congruent challenge, this card represents {weekly}."

def analyze_card_hits(source_card, target_bundle):
    """Returns a list of positional hits in target's BC and PRC paths."""
    hits = []
    # Check BC Path
    if source_card in target_bundle["BC"]["life_path"]:
        pos = target_bundle["BC"]["life_path"].index(source_card)
        dyn = REL_DYNAMICS[pos]
        hits.append(f"BC Path: {dyn['name']} (Pos {pos})")
    
    # Check PRC Path
    if target_bundle["PRC"]["anchor"] != "?" and source_card in target_bundle["PRC"]["life_path"]:
        pos = target_bundle["PRC"]["life_path"].index(source_card)
        dyn = REL_DYNAMICS[pos]
        hits.append(f"PRC Path: {dyn['name']} (Pos {pos})")
        
    return hits

def generate_report(p1_data, p2_data, target_date, out_path):
    c = canvas.Canvas(out_path, pagesize=letter)
    W, H = letter
    m = 0.55 * inch
    
    def start_page(title, rev):
        c.setFillColor(BG_CREAM)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        draw_blueprint_extras(c, W, H, m)
        c.setFillColor(WARM_BLACK)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(m + 20, H - m - 40, title)
        c.setFont("Helvetica", 8)
        c.setFillColor(MID_GRAY)
        c.drawString(m + 20, H - m - 55, f"ARCHITECTURAL AUDIT  \u00b7  {target_date.isoformat()}  \u00b7  {rev}")

    def draw_subject_box(x, y, data, label):
        c.setFillColor(WHITE)
        c.setStrokeColor(MID_GRAY)
        c.roundRect(x, y-40, (W-2*m)/2 - 10, 50, 4, fill=1, stroke=1)
        c.setFillColor(WARM_BLACK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 10, y - 5, f"{label}: {data['BC']['anchor']}")
        c.setFont("Helvetica", 8)
        c.setFillColor(MID_GRAY)
        c.drawString(x + 10, y - 18, f"Born: {data['BC']['birth_info']['m']}/{data['BC']['birth_info']['d']}/{data['BC']['birth_info']['y']}")
        if data['PRC']['anchor'] != "?":
            c.drawString(x + 10, y - 30, f"PRC: {data['PRC']['anchor']}")

    # PAGE 1: P1 Audit
    start_page("COMPATIBILITY DEEP DIVE", "REV 03 / SEC A")
    y = H - m - 80
    draw_subject_box(m + 10, y, p1_data, "PERSON 1 SOURCE")
    draw_subject_box(W/2 + 5, y, p2_data, "PERSON 2 TARGET")
    
    y -= 65
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(RED)
    c.drawString(m + 20, y, "\u00a701  AUDIT: PERSON 1 ANALYSIS OF PERSON 2")
    y -= 5
    c.setStrokeColor(RED)
    c.setLineWidth(1)
    c.line(m + 20, y, W - m - 20, y)
    y -= 25

    def run_audit(source_bundle, target_bundle, current_y):
        for anchor_key in ["BC", "PRC"]:
            src = source_bundle[anchor_key]
            if src["anchor"] == "?": continue
            
            c.setFillColor(WARM_BLACK)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(m + 20, current_y, f">> AUDITING {anchor_key} SPREAD ({src['anchor']})")
            current_y -= 15
            
            # Headers
            c.setFont("Helvetica-Bold", 7)
            c.setFillColor(MID_GRAY)
            c.drawString(m + 30, current_y, "CARD TYPE")
            c.drawString(m + 100, current_y, "CARD")
            c.drawString(m + 140, current_y, "TARGET HIT / DYNAMIC")
            current_y -= 10
            
            metrics = [
                ("Long Range", src["long_range"]),
                ("Pluto", src["pluto"]),
                ("Result", src["result"]),
                ("Environment", src["env"]),
                ("Displacement", src["disp"]),
                ("Karma Supp", src["karma_supp"]),
                ("Karma Chall", src["karma_chall"])
            ]
            
            for label, card in metrics:
                c.setFillColor(WARM_BLACK)
                c.setFont("Helvetica", 8)
                c.drawString(m + 30, current_y, label)
                draw_card_chip(c, m + 100, current_y, card)
                
                hits = analyze_card_hits(card, target_bundle)
                if hits:
                    c.setFillColor(RED)
                    c.setFont("Helvetica-Bold", 7.5)
                    c.drawString(m + 140, current_y, " | ".join(hits))
                else:
                    c.setFillColor(MID_GRAY)
                    c.setFont("Helvetica", 7.5)
                    c.drawString(m + 140, current_y, "No Direct Hit")
                
                if label == "Displacement":
                    current_y -= 10
                    c.setFont("Helvetica-Oblique", 6.5)
                    c.setFillColor(MID_GRAY)
                    chall_text = get_congruent_challenge(card)
                    wrapped = textwrap.fill(chall_text, width=100)
                    for line in wrapped.split('\n'):
                        c.drawString(m + 140, current_y, line)
                        current_y -= 8
                    current_y += 8 # Correction
                
                current_y -= 15
            current_y -= 10
        return current_y

    y = run_audit(p1_data, p2_data, y)
    
    # Footnote page 1
    c.setFont("Helvetica", 7)
    c.setFillColor(MID_GRAY)
    c.drawString(m + 20, m + 15, "Cardology Deep Dive Analysis | Precision Engine v3.0 | Page 1 of 2")
    
    # PAGE 2: P2 Audit
    c.showPage()
    start_page("COMPATIBILITY DEEP DIVE", "REV 03 / SEC B")
    y = H - m - 80
    draw_subject_box(m + 10, y, p2_data, "PERSON 2 SOURCE")
    draw_subject_box(W/2 + 5, y, p1_data, "PERSON 1 TARGET")
    
    y -= 65
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(RED)
    c.drawString(m + 20, y, "\u00a702  AUDIT: PERSON 2 ANALYSIS OF PERSON 1")
    y -= 5
    c.setStrokeColor(RED)
    c.setLineWidth(1)
    c.line(m + 20, y, W - m - 20, y)
    y -= 25
    
    run_audit(p2_data, p1_data, y)
    
    # Footnote page 2
    c.setFont("Helvetica", 7)
    c.setFillColor(MID_GRAY)
    c.drawString(m + 20, m + 15, "Cardology Deep Dive Analysis | Precision Engine v3.0 | Page 2 of 2")
    
    c.save()

if __name__ == "__main__":
    if len(sys.argv) < 7:
        sys.exit(0)
    
    from calculate_blueprint import calculate_blueprint
    from datetime import datetime
    
    m1, d1, y1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    m2, d2, y2 = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    target_dt = datetime.strptime(sys.argv[7], "%Y-%m-%d").date()
    
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
                "karma_supp": r["lifetime_karma"]["supporting"],
                "karma_chall": r["lifetime_karma"]["challenge"],
                "life_path": r["life_path"]
            }
        return {"BC": bundle(bc_res), "PRC": bundle(prc_res)}

    p1_data = build_p_data(m1, d1, y1, target_dt)
    p2_data = build_p_data(m2, d2, y2, target_dt)
    
    out_file = f"Professional_Deep_Dive_{m1}_{d1}_{y1}_vs_{m2}_{d2}_{y2}.pdf"
    output_path = os.path.join(os.getcwd(), "outputs", out_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    generate_report(p1_data, p2_data, target_dt, output_path)
    print(f"Professional Report Generated: {output_path}")

