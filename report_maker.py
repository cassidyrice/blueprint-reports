#!/usr/bin/env python3
"""
Precise Report Maker — Card Blueprints

Generates Professional and Compatibility reports with high precision.
Uses the core engine from calculate_blueprint.py.
"""

import os
import sys
import textwrap
from datetime import date
from calculate_blueprint import (
    calculate_blueprint, 
    calculate_compatibility, 
    get_card_descriptions, 
    get_weekly_meanings,
    PLANET_NAMES
)

def create_standard_report(res, filename=None):
    """Generates the precise Professional Report based on the project template."""
    a = res["archetype"]
    t = res["timing"]
    ys = res["yearly_spread"]
    ap = res["active_period"]
    nav = res["navigation"]
    lr = res["long_range"]
    ed = res["environment_displacement"]
    lk = res["lifetime_karma"]
    
    desc = get_card_descriptions()
    weekly = get_weekly_meanings()
    
    lines = []
    lines.append("=" * 70)
    lines.append("CARD BLUEPRINT")
    lines.append("=" * 70)
    
    lines.append("\n--- ARCHETYPE ---")
    lines.append(f"Birth Card:              {a['birth_card']} (Solar Value: {a['solar_value']})")
    if a['prc'] != "?":
        lines.append(f"Planetary Ruling Card:   {a['prc']} ({a['sun_sign']} / {a['ruling_planet']})")
    
    bc_info = desc.get(a['birth_card'], {})
    if bc_info:
        title = bc_info.get('title', '')
        if title: lines.append(f"                         {title}")
        core = bc_info.get('core_identity', '')
        if core:
            wrapped_core = textwrap.fill(core, width=65, initial_indent="                         ", subsequent_indent="                         ")
            lines.append(wrapped_core)
    lines.append(f"                         Domain: {a['domain']}")
    lines.append(f"Purpose:                 {a['purpose']}")
    
    lines.append("\n--- TIMING ---")
    lines.append(f"Birth Date:    {t['birth_date']}")
    lines.append(f"Target Date:   {t['target_date']}")
    lines.append(f"Age:           {t['age']}")
    lines.append(f"Spread Year:   {t['spread_year']}")
    lines.append(f"Crown Line:    {' | '.join(t['crown_line'])}")
    
    lines.append(f"\n--- YEARLY SPREAD ({ys['anchor']}) ---")
    if ys['grid_position']:
        lines.append(f"Grid Position: Row={ys['grid_position']['row']}, Col={ys['grid_position']['col']}")
    lines.append("7 Period Cards:")
    
    # Planets 0-6
    for i in range(7):
        planet = PLANET_NAMES[i]
        card = ys['periods'][i]
        marker = " ◄ ACTIVE" if planet == ap['planet'] else ""
        lines.append(f"  {planet:10s} → {card}{marker}")
        
        # Add meaning if available
        if card in weekly and planet.lower() in weekly[card]:
            m = weekly[card][planet.lower()]
            wrapped_m = textwrap.fill(m, width=65, initial_indent="               ", subsequent_indent="               ")
            lines.append(wrapped_m)
            
    # Pluto and Result (Indices 7 and 8)
    for idx, label in [(7, "Pluto"), (8, "Result")]:
        card = ys['periods'][idx] if idx < len(ys['periods']) else "?"
        lines.append(f"  {label:10s} → {card}")
        if card in weekly and label.lower() in weekly[card]:
            m = weekly[card][label.lower()]
            wrapped_m = textwrap.fill(m, width=65, initial_indent="               ", subsequent_indent="               ")
            lines.append(wrapped_m)
            
    lines.append("\n--- ACTIVE PERIOD ---")
    lines.append(f"Planet:        {ap['planet']}")
    lines.append(f"Day in Year:   {ap['day_in_year']}")
    lines.append(f"Active Card:   {ap['card']}")
    
    lines.append("\n--- LONG RANGE ---")
    lines.append(f"Long Range Card: {lr['card']} (Cycle {lr['cycle']}, Spread {lr['spread']}, {lr['planet']})")
    if lr['card'] in weekly and 'long_range' in weekly[lr['card']]:
        m = weekly[lr['card']]['long_range']
        wrapped_m = textwrap.fill(m, width=65, initial_indent="                 ", subsequent_indent="                 ")
        lines.append(wrapped_m)
        
    lines.append("\n--- ENVIRONMENT & DISPLACEMENT ---")
    lines.append(f"Environment:     {ed['environment']} (who moved into your house)")
    if ed['environment'] in weekly and 'environment' in weekly[ed['environment']]:
        m = weekly[ed['environment']]['environment']
        wrapped_m = textwrap.fill(m, width=65, initial_indent="                 ", subsequent_indent="                 ")
        lines.append(wrapped_m)
    lines.append(f"Displacement:    {ed['displacement']} (landlord where you moved)")
    
    lines.append("\n--- LIFETIME KARMA ---")
    lines.append(f"Challenge:       {lk['challenge']}")
    lines.append(f"Supporting:      {lk['supporting']}")
    
    lines.append("\n--- NAVIGATION ---")
    lines.append(f"Formula:       {nav['formula']}")
    lines.append(f"All 7 Cards:   {', '.join(nav['all_7_cards'])}")
    lines.append("=" * 70)
    
    report = "\n".join(lines)
    if filename:
        save_to_outputs(report, filename)
    return report

def create_compatibility_report(p1, p2, comp, filename=None):
    """Generates the precise Compatibility Report based on the Grand Life Spread logic."""
    lines = []
    lines.append("=" * 70)
    lines.append("COMPATIBILITY REPORT (GRAND LIFE SPREAD)")
    lines.append("=" * 70)
    lines.append(f"Person 1: {p1['archetype']['birth_card']} (PRC: {p1['archetype']['prc']})")
    lines.append(f"Person 2: {p2['archetype']['birth_card']} (PRC: {p2['archetype']['prc']})")
    lines.append("-" * 70)
    
    def format_view(view_name, conns, person_name, other_name, target_bc, target_prc):
        lines.append(f"HOW {person_name} RELATES TO {other_name}:")
        
        mapping = [
            ("BC to BC", conns["bc_to_bc"], target_bc),
            ("BC to PRC", conns["bc_to_prc"], target_prc),
            ("PRC to BC", conns["prc_to_bc"], target_bc),
            ("PRC to PRC", conns["prc_to_prc"], target_prc)
        ]
        
        found = False
        for label, view, card in mapping:
            if card != "?" and view["pos"] >= 0:
                found = True
                d = view["dynamic"]
                lines.append(f"  {label:10s} -> Pos: {view['pos']} ({d['name']}) : {d['tagline']}")
                wrapped_desc = textwrap.fill(d['desc'], width=60, initial_indent="               Context: ", subsequent_indent="                        ")
                lines.append(wrapped_desc)
        
        if not found:
            lines.append(f"  No direct Life Path connections found in this pairing.")
        lines.append("")

    format_view("P1 View", comp["connections_p1"], "PERSON 1", "PERSON 2", p2['archetype']['birth_card'], p2['archetype']['prc'])
    format_view("P2 View", comp["connections_p2"], "PERSON 2", "PERSON 1", p1['archetype']['birth_card'], p1['archetype']['prc'])
    
    lines.append("-" * 70)
    
    aligned = []
    frictions = []
    for view in [comp["connections_p1"], comp["connections_p2"]]:
        for conn in view.values():
            aligned.extend(conn["aligned"])
            frictions.extend(conn["friction"])
    
    aligned = sorted(list(set(aligned)))
    frictions = sorted(list(set(frictions)))
    
    lines.append(f"ALIGNED GOALS: {', '.join(aligned) if aligned else 'Natural Balance'}")
    lines.append(f"FRICTION DESK: {', '.join(frictions) if frictions else 'Low Conflict'}")
    
    if comp["is_karma_bc"]:
        lines.append(f"SPECIAL LINK:  P2 (Birth Card) is P1's MOON mate (Strong Intimacy).")
    if comp["is_karma_prc"]:
        lines.append(f"SPECIAL LINK:  P2 (PRC) is P1's MOON mate (Strong Intimacy).")
        
    lines.append("=" * 70)
    
    report = "\n".join(lines)
    if filename:
        save_to_outputs(report, filename)
    return report

def save_to_outputs(content, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\nReport saved to: {filepath}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python report_maker.py <m1> <d1> <y1> [m2 d2 y2] [--report]")
        sys.exit(0)
        
    m1, d1, y1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    res1 = calculate_blueprint(m1, d1, y1)
    
    if len(sys.argv) >= 7 and sys.argv[4].isdigit():
        m2, d2, y2 = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
        res2 = calculate_blueprint(m2, d2, y2)
        comp = calculate_compatibility(res1, res2)
        
        report = create_compatibility_report(res1, res2, comp)
        print(report)
        
        if "--report" in sys.argv:
            fname = f"Compatibility_{m1}_{d1}_{y1}_vs_{m2}_{d2}_{y2}.txt"
            save_to_outputs(report, fname)
    else:
        report = create_standard_report(res1)
        print(report)
        
        if "--report" in sys.argv:
            fname = f"Blueprint_{m1}_{d1}_{y1}.txt"
            save_to_outputs(report, fname)
