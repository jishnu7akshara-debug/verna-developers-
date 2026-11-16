import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs('assets/img/dept', exist_ok=True)

W, H = 800, 500

def create_gradient_scrim(img):
    # Overlay top dark scrim and bottom dark scrim for text readability
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Top scrim
    for y in range(120):
        alpha = int(140 * (1 - y / 120.0))
        draw.line([(0, y), (W, y)], fill=(10, 20, 30, alpha))
        
    # Bottom scrim
    for y in range(H - 160, H):
        prog = (y - (H - 160)) / 160.0
        alpha = int(210 * (prog ** 1.3))
        draw.line([(0, y), (W, y)], fill=(10, 16, 26, alpha))
        
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def draw_pill(draw, x, y, text, bg_color, text_color, font, pad_x=16, pad_y=8, r=6):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + pad_x * 2
    h = th + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=bg_color)
    draw.text((x + pad_x, y + pad_y - 1), text, fill=text_color, font=font)
    return w, h

def draw_emblem_seal(img, x, y, size, emblem_type):
    # Circular white container with shadow
    emblem = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    edraw = ImageDraw.Draw(emblem)
    
    # White base
    edraw.ellipse([2, 2, size - 3, size - 3], fill=(255, 255, 255, 255), outline=(220, 225, 230, 255), width=2)
    center = size / 2.0
    
    # Inner decorative ring
    inner_r = size / 2.0 - 6
    edraw.ellipse([center - inner_r, center - inner_r, center + inner_r, center + inner_r], outline=(200, 160, 100, 200), width=1)
    
    if emblem_type == 'bbmp':
        # BBMP: Blue & Gold municipal shield
        edraw.ellipse([center - 18, center - 18, center + 18, center + 18], fill=(24, 76, 140, 255))
        edraw.ellipse([center - 13, center - 13, center + 13, center + 13], fill=(255, 255, 255, 255))
        # Municipal gate tower
        edraw.rectangle([center - 6, center - 8, center + 6, center + 8], fill=(24, 76, 140, 255))
        edraw.polygon([(center - 8, center - 8), (center, center - 14), (center + 8, center - 8)], fill=(190, 40, 40, 255))
        
    elif emblem_type == 'bda':
        # BDA: Royal blue & gold geometric wheel
        edraw.ellipse([center - 18, center - 18, center + 18, center + 18], fill=(16, 50, 110, 255))
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            x1 = center + math.cos(rad) * 6
            y1 = center + math.sin(rad) * 6
            x2 = center + math.cos(rad) * 16
            y2 = center + math.sin(rad) * 16
            edraw.line([(x1, y1), (x2, y2)], fill=(255, 215, 0, 255), width=2)
        edraw.ellipse([center - 6, center - 6, center + 6, center + 6], fill=(255, 255, 255, 255))
        
    elif emblem_type == 'karnataka':
        # Karnataka Gandaberunda (Red shield, gold two-headed eagle)
        edraw.ellipse([center - 18, center - 18, center + 18, center + 18], fill=(168, 28, 36, 255))
        # Gold eagle wings & lions
        edraw.polygon([(center, center - 12), (center - 11, center - 2), (center - 8, center + 8),
                       (center, center + 14), (center + 8, center + 8), (center + 11, center - 2)], fill=(245, 195, 65, 255))
        # Center crest
        edraw.ellipse([center - 4, center - 4, center + 4, center + 4], fill=(255, 255, 255, 255))
        
    elif emblem_type == 'bmrcl':
        # Namma Metro Pinwheel (Magenta / purple petals)
        for deg in [0, 90, 180, 270]:
            rad = math.radians(deg)
            cx = center + math.cos(rad) * 9
            cy = center + math.sin(rad) * 9
            edraw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(160, 32, 120, 230))
        edraw.ellipse([center - 5, center - 5, center + 5, center + 5], fill=(255, 255, 255, 255))
        
    elif emblem_type == 'kiadb':
        # KIADB: Industrial gear emblem (Red & Gold)
        edraw.ellipse([center - 18, center - 18, center + 18, center + 18], fill=(220, 160, 30, 255))
        # Gear teeth
        for deg in range(0, 360, 30):
            rad = math.radians(deg)
            tx = center + math.cos(rad) * 19
            ty = center + math.sin(rad) * 19
            edraw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(180, 30, 30, 255))
        edraw.ellipse([center - 13, center - 13, center + 13, center + 13], fill=(180, 30, 30, 255))
        edraw.ellipse([center - 7, center - 7, center + 7, center + 7], fill=(255, 255, 255, 255))
        
    elif emblem_type == 'rera':
        # RERA: Scales of justice & gold rim
        edraw.ellipse([center - 18, center - 18, center + 18, center + 18], fill=(26, 70, 60, 255))
        # Scales of justice
        edraw.line([(center, center - 12), (center, center + 12)], fill=(240, 200, 80, 255), width=2)
        edraw.line([(center - 10, center - 6), (center + 10, center - 6)], fill=(240, 200, 80, 255), width=2)
        edraw.ellipse([center - 12, center - 1, center - 6, center + 3], outline=(240, 200, 80, 255), width=1)
        edraw.ellipse([center + 6, center - 1, center + 12, center + 3], outline=(240, 200, 80, 255), width=1)

    # Paste onto image with slight drop shadow
    shadow = Image.new('RGBA', (size + 8, size + 8), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([4, 4, size + 4, size + 4], fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    
    img.alpha_composite(shadow, (x - 2, y))
    img.alpha_composite(emblem, (x, y))

print("Emblem helper ready.")
