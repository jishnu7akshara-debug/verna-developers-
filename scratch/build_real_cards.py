import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"

def make_gradient(width, height):
    """Create a dark gradient overlay that fades from transparent to rich dark at bottom."""
    grad = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(grad)
    start_y = int(height * 0.55)
    for y in range(start_y, height):
        ratio = ((y - start_y) / (height - start_y)) ** 1.3
        alpha = int(225 * ratio)
        draw.line([(0, y), (width, y)], fill=(6, 10, 16, alpha))
    return grad

def create_circular_logo_badge(logo_path, size=184):
    """Create a pristine white circular medallion with border and centered official logo."""
    super_size = size * 2
    badge = Image.new("RGBA", (super_size, super_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    pad = 6
    # Subtle drop shadow ring
    draw.ellipse([pad - 2, pad - 2, super_size - pad + 2, super_size - pad + 2], fill=(0, 0, 0, 50))
    # Crisp white disc with subtle border
    draw.ellipse([pad, pad, super_size - pad, super_size - pad], fill=(255, 255, 255, 255), outline=(220, 226, 232, 255), width=6)
    
    # Load and fit logo
    logo = Image.open(logo_path).convert("RGBA")
    inner_dim = int(super_size * 0.78)
    logo.thumbnail((inner_dim, inner_dim), Image.Resampling.LANCZOS)
    
    lx = (super_size - logo.width) // 2
    ly = (super_size - logo.height) // 2
    badge.alpha_composite(logo, (lx, ly))
    
    return badge.resize((size, size), Image.Resampling.LANCZOS)

def draw_pill(draw, xy, text, font, fill_color, text_color, radius=8, border_color=None):
    """Draw a smooth rounded pill rectangle with centered text."""
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    px, py = xy
    pad_x = 18
    pad_y = 9
    w = tw + pad_x * 2
    h = th + pad_y * 2
    
    rect = [px, py, px + w, py + h]
    if border_color:
        draw.rounded_rectangle(rect, radius=radius, fill=fill_color, outline=border_color, width=2)
    else:
        draw.rounded_rectangle(rect, radius=radius, fill=fill_color)
    
    tx = px + pad_x - bbox[0]
    ty = py + pad_y - bbox[1]
    draw.text((tx, ty), text, font=font, fill=text_color)
    return px + w, py + h

def build_card(bg_image_path, badge_text, tag_text, label_text, logo_path, out_1x, out_2x):
    """Build a complete 800x500 and 1600x1000 card with real clean photo and official logo."""
    W, H = 1600, 1000
    
    bg = Image.open(bg_image_path).convert("RGBA")
    
    # Crop to 16:10 aspect ratio and resize to 1600x1000
    bg_ratio = bg.width / bg.height
    target_ratio = W / H
    if bg_ratio > target_ratio:
        new_w = int(bg.height * target_ratio)
        offset_x = (bg.width - new_w) // 2
        bg = bg.crop((offset_x, 0, offset_x + new_w, bg.height))
    else:
        new_h = int(bg.width / target_ratio)
        offset_y = (bg.height - new_h) // 2
        bg = bg.crop((0, offset_y, bg.width, offset_y + new_h))
        
    bg = bg.resize((W, H), Image.Resampling.LANCZOS)
    
    # Clarity enhancements: sharpness & contrast
    enhancer = ImageEnhance.Sharpness(bg)
    bg = enhancer.enhance(1.25)
    bg = ImageEnhance.Contrast(bg).enhance(1.05)
    
    # Apply bottom gradient
    grad = make_gradient(W, H)
    bg.alpha_composite(grad)
    
    # Overlay layer
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Typography
    font_badge = ImageFont.truetype(FONT_BOLD, 36)
    font_tag = ImageFont.truetype(FONT_BOLD, 26)
    font_label = ImageFont.truetype(FONT_BOLD, 36)
    
    # 1. Top-Left Badge (Dark Forest Green #133e2a)
    draw_pill(draw, (36, 32), badge_text, font_badge, fill_color=(19, 62, 42, 245), text_color=(255, 255, 255, 255), radius=8)
    
    # 2. Top-Right Tag (Frosted Translucent #f8fafc with white border)
    bbox_tag = font_tag.getbbox(tag_text)
    tw_tag = bbox_tag[2] - bbox_tag[0]
    tag_w = tw_tag + 36
    tag_x = W - 36 - tag_w
    draw_pill(draw, (tag_x, 32), tag_text, font_tag, fill_color=(255, 255, 255, 225), text_color=(30, 41, 59, 255), radius=8, border_color=(255, 255, 255, 255))
    
    # 3. Bottom-Left Label
    draw.text((42, H - 76), label_text, font=font_label, fill=(0, 0, 0, 230))
    draw.text((40, H - 78), label_text, font=font_label, fill=(255, 255, 255, 255))
    
    # 4. Bottom-Right Circular Medallion (Single crisp medallion)
    badge_img = create_circular_logo_badge(logo_path, size=184)
    badge_x = W - 36 - 184
    badge_y = H - 28 - 184
    overlay.alpha_composite(badge_img, (badge_x, badge_y))
    
    # Composite
    final_2x = Image.alpha_composite(bg, overlay).convert("RGB")
    final_1x = final_2x.resize((800, 500), Image.Resampling.LANCZOS)
    
    # Save WebP
    final_2x.save(out_2x, format="WEBP", quality=95)
    final_1x.save(out_1x, format="WEBP", quality=95)
    print(f"OK: {out_1x} ({os.path.getsize(out_1x)} B) | {out_2x} ({os.path.getsize(out_2x)} B)")

if __name__ == "__main__":
    os.makedirs("assets/img/dept", exist_ok=True)
    
    # 100% CLEAN HIGH-RESOLUTION PHOTOGRAPHS (NO BURNT-IN TEXT, NO BURNT-IN LOGOS)
    cards = [
        {
            "id": "bbmp",
            "bg": "scratch/downloads/bbmp_building.jpg",
            "badge": "BBMP",
            "tag": "KAR-AUTH-01",
            "label": "Greater Bengaluru Civic Works",
            "logo": "scratch/downloads/bbmp_logo.jpg"
        },
        {
            "id": "bda",
            "bg": "scratch/downloads/bda_urban.jpg",
            "badge": "BDA",
            "tag": "KAR-AUTH-02",
            "label": "Bengaluru Urban Planning",
            "logo": "scratch/downloads/bda_logo.jpg"
        },
        {
            "id": "bmrda",
            "bg": "scratch/downloads/nh48_highway.jpg",
            "badge": "BMRDA",
            "tag": "KAR-AUTH-03",
            "label": "Metropolitan Regional Planning",
            "logo": "scratch/downloads/karnataka_seal.png"
        },
        {
            "id": "bmicapa",
            "bg": "scratch/downloads/nice_road.jpg",
            "badge": "BMICAPA",
            "tag": "KAR-AUTH-04",
            "label": "NICE Expressway Corridor",
            "logo": "scratch/downloads/karnataka_seal.png"
        },
        {
            "id": "bmrcl",
            "bg": "scratch/downloads/metro_train.jpg",
            "badge": "BMRCL",
            "tag": "KAR-AUTH-05",
            "label": "Namma Metro Transit Network",
            "logo": "scratch/downloads/metro_logo.png"
        },
        {
            "id": "kiadb",
            "bg": "scratch/downloads/kiadb_ecity.jpg",
            "badge": "KIADB",
            "tag": "KAR-AUTH-06",
            "label": "State Industrial Estates",
            "logo": "scratch/downloads/kiadb_right.png"
        },
        {
            "id": "citb",
            "bg": "scratch/downloads/citb_tree_road.jpg",
            "badge": "CITB",
            "tag": "KAR-AUTH-07",
            "label": "Heritage Planned Layouts",
            "logo": "scratch/downloads/karnataka_seal.png"
        },
        {
            "id": "rera",
            "bg": "scratch/downloads/prestige_tower.jpg",
            "badge": "RERA",
            "tag": "KAR-AUTH-08",
            "label": "Statutory Project Regulatory Board",
            "logo": "scratch/downloads/logos.png"
        }
    ]
    
    print("Regenerating all 8 official high-resolution department cards with clean photos...")
    for c in cards:
        out_1x = f"assets/img/dept/dept-{c['id']}.webp"
        out_2x = f"assets/img/dept/dept-{c['id']}-2x.webp"
        build_card(c["bg"], c["badge"], c["tag"], c["label"], c["logo"], out_1x, out_2x)
    print("All 8 cards generated with 100% clean photos, single badges, and single official logos!")
