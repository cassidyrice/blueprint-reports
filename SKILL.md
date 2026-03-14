---
name: blueprint-reports
description: Generates print-ready PDF reports in the Card Blueprints architectural/blueprint aesthetic. Two report types — (1) Card Blueprint individual yearly spread report and (2) Compatibility Report for two-person Grand Life Spread analysis. Uses red for ♥/♦ suits and black for ♠/♣ suits throughout. Use this skill whenever the user asks to generate a card blueprint report, compatibility report, printable card report, mail-ready PDF, or any formatted output of card blueprint data or compatibility data. Also trigger when the user pastes structured card blueprint output or compatibility output and wants it turned into a PDF, or says 'make this printable', 'format this for mail', 'generate the report', 'print report', or references the blueprint aesthetic/design for card data.
---

# Blueprint Reports Skill

Generates high-quality, print-ready PDF reports using the Card Blueprints architectural design system. All reports use:

- **Color system**: Red (`#C41E3A`) for ♥/♦ suits, warm black (`#1A1A1A`) for ♠/♣ suits
- **Typography**: BigShoulders-Bold (titles), Outfit/Outfit-Bold (section labels), GeistMono/GeistMono-Bold (data), Jura-Medium (body descriptions), DejaVu-Bold (suit symbols), InstrumentSans-Bold (card labels)
- **Layout**: Architectural frame with registration marks, faint background grid, §-numbered sections, card chips with rounded borders, red accent bars
- **Print specs**: US Letter (8.5×11"), cream background (#FAFAF8), crop marks for professional trimming

## Fonts Required

All fonts load from `/mnt/skills/examples/canvas-design/canvas-fonts/` except DejaVu which loads from `/usr/share/fonts/truetype/dejavu/`. DejaVu is critical for rendering Unicode suit symbols (♥♦♠♣).

## Report Type 1: Card Blueprint (Individual Yearly Spread)

**Script**: `scripts/generate_card_blueprint.py`

Generates a single-page PDF containing:
- §01 ARCHETYPE — Birth card display, solar value, domain, timing (birth date, target date, age/spread year), crown line
- §02 YEARLY SPREAD — 7 planetary period cards (Mercury→Neptune) with descriptions, active period highlighted with red accent bar and ACTIVE badge
- §03 TRANSFORMATION ARC — Pluto and Result cards with dashed connector
- §04 LONG RANGE — Large card display with cycle/spread/planet metadata
- §05 ENVIRONMENT & DISPLACEMENT — Side-by-side with vertical divider
- §06 ACTIVE PERIOD — Red-bordered callout box with planet, card, and day-in-year
- §07 NAVIGATION & KARMA — Formula bar, all 7 cards row, lifetime karma (challenge + supporting)

**To use**: Read the script, then modify the data variables (periods list, card values, dates, descriptions) to match the target person's data. Run with Python.

### Data Format

The script expects structured card blueprint data. Key data points to customize:
- Birth card, solar value, domain
- Birth date, target date, age, spread year
- Crown line (3 cards)
- Grid position (row, column)
- 7 period cards with planet, card, description (2 lines), and active flag
- Pluto card + description
- Result card + description
- Long Range card + cycle/spread/planet
- Environment card + description
- Displacement card
- Formula (birth card + active card + planet)
- Lifetime karma challenge + supporting cards

## Report Type 2: Compatibility Report (Grand Life Spread)

**Script**: `scripts/generate_compatibility_report.py`

Generates a single-page PDF containing:
- §01 SUBJECTS — Two person cards side by side in colored boxes (red tint for Person 1, gray tint for Person 2) with birth dates
- §02 HOW PERSON 1 RELATES TO PERSON 2 — Card chips with arrow, position badge, description. If connection exists: red-accented box with position label. If not: gray box with ✗ mark.
- §03 HOW PERSON 2 RELATES TO PERSON 1 — Same format, handles empty (no connection) state
- §04 SUMMARY — Aligned Goals and Friction Desk side-by-side summary boxes
- §05 RELATIONSHIP MAP — Visual diagram showing directional connections between the two cards

**To use**: Read the script, then modify the data passed to each draw function (person cards, birth dates, position labels, descriptions, aligned goals, friction desk values). Run with Python.

### Data Format

The script expects structured compatibility data:
- Person 1: birth card, birth date
- Person 2: birth card, birth date  
- Direction 1→2: position number, planet name, description, context (or empty)
- Direction 2→1: position number, planet name, description, context (or empty)
- Aligned Goals label
- Friction Desk label

## Design Principles (for both reports)

1. **Body text**: Jura-Medium at 8.5–10pt in warm black — legible at arm's length for physical mail
2. **Section labels**: Outfit-Bold 9pt in mid-gray with hairline rule extending to right margin
3. **Card chips**: Rounded rectangles with colored stroke matching suit, white fill, centered rank+suit
4. **Active states**: Faint red background (#FBF0F0), 2.5pt red left accent bar
5. **Empty states**: Faint gray background, ✗ mark, "not found" messaging
6. **Footer**: GeistMono 7pt with brand line and tagline

## Running

```bash
pip install reportlab --break-system-packages
python scripts/generate_card_blueprint.py
python scripts/generate_compatibility_report.py
```

Output PDFs land in `/home/claude/` — copy to `/mnt/user-data/outputs/` for user delivery.
