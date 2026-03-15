import math
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT = r"c:\Users\abvik\OneDrive\Desktop\Hotel\outputs\flower_of_life_master.png"
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# ── Canvas setup with 4x supersampling for flawless anti-aliasing ─────────────
SCALE = 4
SIZE_PX = 2000
W = SIZE_PX * SCALE
H = SIZE_PX * SCALE
CX = W // 2
CY = H // 2
R = int(230 * SCALE)

CREAM = (253, 250, 245)
INK = (30, 30, 30)
RED = (196, 30, 58)

def main():
    print("Generating pure mathematical Flower of Life...")
    
    # 1. Base Layer
    base = Image.new("RGBA", (W, H), CREAM)
    
    # 2. Circles Layer (so we can mask it precisely at the boundary)
    circles_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_circles = ImageDraw.Draw(circles_layer)
    
    # Draw an extended grid of circles
    # The math guarantees the classic overlapping petal geometry
    weight = max(1, 4 * SCALE)
    for dx in range(-6, 7):
        for idy in range(-12, 13):
            # Hex grid filter: dx even -> dy integer, dx odd -> dy half-integer
            if dx % 2 == 0 and idy % 2 != 0: continue
            if dx % 2 != 0 and idy % 2 == 0: continue
            dy = idy / 2.0
            
            cx = CX + dx * R * (math.sqrt(3)/2)
            cy = CY + dy * R
            draw_circles.ellipse([cx - R, cy - R, cx + R, cy + R], outline=INK, width=weight)

    # 3. Apply the Circular Mask
    # The outer boundary of the classic 19-circle flower touches exactly at 3*R
    mask = Image.new("L", (W, H), 0)
    draw_mask = ImageDraw.Draw(mask)
    outer_radius = 3 * R
    draw_mask.ellipse([CX - outer_radius, CY - outer_radius, CX + outer_radius, CY + outer_radius], fill=255)
    
    img = Image.composite(circles_layer, base, mask)
    draw = ImageDraw.Draw(img)
    
    # 4. Draw the precise architectural outer rings
    draw.ellipse([CX - outer_radius, CY - outer_radius, CX + outer_radius, CY + outer_radius], outline=INK, width=max(1, 6*SCALE))
    draw.ellipse([CX - outer_radius - 6*SCALE, CY - outer_radius - 6*SCALE, CX + outer_radius + 6*SCALE, CY + outer_radius + 6*SCALE], outline=INK, width=max(1, 12*SCALE))
    
    # 5. The 13 Specific Centers (replacing the green dots)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\seguisym.ttf", int(R * 1.0))
    except:
        font = ImageFont.load_default()

    # The exact coordinates of the 5-4-4 vertical honeycomb
    positions = [
        # Center column (5)
        (0, -2, "♠", INK), (0, -1, "♥", RED), (0, 0, "♦", RED), (0, 1, "♣", INK), (0, 2, "♠", INK),
        # Left column (4)
        (-1, -1.5, "♦", RED), (-1, -0.5, "♥", RED), (-1, 0.5, "♠", INK), (-1, 1.5, "♦", RED),
        # Right column (4)
        (1, -1.5, "♥", RED), (1, -0.5, "♠", INK), (1, 0.5, "♣", INK), (1, 1.5, "♥", RED)
    ]

    for (dx, dy, suit, color) in positions:
        cx = CX + dx * R * (math.sqrt(3)/2)
        cy = CY + dy * R
        
        # Draw a cream backplate under the pip (so lines don't strike through it, matching the green dot size)
        dot_r = R * 0.45
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=CREAM)
        
        # Center the pip visually
        bbox = draw.textbbox((0,0), suit, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        oy = -th * 0.1
        if suit == "♦": oy = -th * 0.15
        if suit == "♥": oy = -th * 0.05
        
        draw.text((cx - tw/2 - bbox[0], cy - th/2 - bbox[1] + oy), suit, font=font, fill=color)

    # Downscale for flawless lines
    img = img.resize((SIZE_PX, SIZE_PX), Image.LANCZOS)
    img.save(OUTPUT)
    print(f"Saved exact geometry to: {OUTPUT}")

if __name__ == "__main__":
    main()
