"""
GNT Logo Enhancement Script — v3
Erases old tiny 'EVENTS & DECORATORS' text and redraws it
~70% larger and bolder along the bottom elliptical arc.
Works from the original clean logo files.
"""
import math
from PIL import Image, ImageDraw, ImageFont

GOLD = (184, 135, 70)         # #B88746
DARK_BRONZE = (138, 100, 40)  # #8A6428 — new text for dark logo
WHITE_TEXT = (255, 255, 255)  # white text for white-on-dark logo


def erase_old_text(img, is_white):
    """Remove old small text pixels from the bottom text band (y ~615–795)."""
    pixels = img.load()
    w, h = img.size
    for y in range(615, 795):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a < 10:
                continue
            # Keep gold oval-border pixels
            dist_gold = abs(r - GOLD[0]) + abs(g - GOLD[1]) + abs(b - GOLD[2])
            if dist_gold < 40:
                continue
            # Erase text pixels
            if is_white:
                if r > 150 and g > 150 and b > 140:
                    pixels[x, y] = (0, 0, 0, 0)
            else:
                if r < 165 and g < 135 and b < 100:
                    pixels[x, y] = (0, 0, 0, 0)
    return img


def draw_curved_text(img, text, text_color, font):
    """Draw text along the BOTTOM elliptical arc of the oval logo.

    In PIL/screen coordinates y increases downward, so angles where
    sin > 0 place points below the center.  The bottom arc uses
    parametric angles from ~145° → 35° (left-to-right, since
    cos(145) < 0 and cos(35) > 0).
    """
    w, h = img.size
    cx, cy = w // 2, h // 2          # ≈ 739, 437

    # Ellipse radii that place text just inside the oval border
    rx = 540
    ry = 330

    # Per-character metrics
    spacing = 7
    char_data = []
    for ch in text:
        bbox = font.getbbox(ch)
        cw = bbox[2] - bbox[0]
        char_data.append((ch, cw, bbox))
    total_width = sum(cw for _, cw, _ in char_data) + spacing * (len(text) - 1)

    # Bottom arc goes from angle 145° (left) through 90° (bottom) to 35° (right)
    # We iterate left-to-right, so angles go from 145 down to 35
    start_deg = 145.0  # left side
    end_deg = 35.0     # right side
    arc_span = start_deg - end_deg  # 110 degrees total

    cumulative = 0
    for ch, cw, bbox in char_data:
        frac = (cumulative + cw / 2) / total_width
        # Interpolate from start_deg down to end_deg
        angle_deg = start_deg - frac * arc_span
        angle_rad = math.radians(angle_deg)

        # Position on ellipse
        x = cx + rx * math.cos(angle_rad)
        y = cy + ry * math.sin(angle_rad)

        # Tangent direction for letter rotation on an ellipse:
        # dx/dt = -rx*sin(t),  dy/dt = ry*cos(t)
        tang = math.atan2(ry * math.cos(angle_rad), -rx * math.sin(angle_rad))
        rot_deg = math.degrees(tang)

        # Render single character
        ch_h = bbox[3] - bbox[1]
        pad = 30
        canvas_size = max(cw, ch_h) + pad * 2

        char_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        tx = (canvas_size - cw) // 2 - bbox[0]
        ty = (canvas_size - ch_h) // 2 - bbox[1]
        char_draw.text((tx, ty), ch, fill=(*text_color, 255), font=font)

        # Rotate to follow the arc
        rotated = char_img.rotate(-rot_deg + 90, expand=False, resample=Image.BICUBIC)

        # Paste with alpha compositing
        px = int(x - canvas_size // 2)
        py = int(y - canvas_size // 2)
        if 0 <= px and 0 <= py and px + canvas_size <= w and py + canvas_size <= h:
            img.paste(rotated, (px, py), rotated)

        cumulative += cw + spacing

    return img


def enhance_logo(input_path, output_path, text_color, is_white):
    print(f"Processing {input_path} ...")
    img = Image.open(input_path).convert("RGBA")

    # Step 1 — erase old text
    img = erase_old_text(img, is_white)
    print("  [OK] Old text erased")

    # Step 2 — load bold serif font
    font_size = 50
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", font_size)
        print(f"  [OK] Using Georgia Bold @ {font_size}px")
    except Exception:
        font = ImageFont.truetype("C:/Windows/Fonts/timesbd.ttf", font_size)
        print(f"  [OK] Using Times Bold @ {font_size}px")

    # Step 3 — draw new large, bold, curved text
    img = draw_curved_text(img, "EVENTS  &  DECORATORS", text_color, font)
    print("  [OK] New text drawn")

    # Step 4 — save without lossy compression
    img.save(output_path, "PNG", optimize=False)
    print(f"  [OK] Saved -> {output_path}")


# ── main ─────────────────────────────────────────────
if __name__ == "__main__":
    # Restore originals first from git
    import subprocess, shutil
    # Process from current files (already restored via git checkout)
    enhance_logo(
        "src/assets/gnt-logo.png",
        "src/assets/gnt-logo.png",
        DARK_BRONZE,
        is_white=False,
    )
    enhance_logo(
        "src/assets/gnt-logo-white.png",
        "src/assets/gnt-logo-white.png",
        WHITE_TEXT,
        is_white=True,
    )
    print("\n[DONE] Both logos enhanced successfully!")
