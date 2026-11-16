import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from card_render_engine import create_gradient_scrim, draw_pill, draw_emblem_seal, W, H

os.makedirs('assets/img/dept', exist_ok=True)

# Try to find suitable system fonts or default
try:
    font_badge = ImageFont.truetype("arialbd.ttf", 22)
    font_tag = ImageFont.truetype("consola.ttf", 18)
    font_label = ImageFont.truetype("arialbd.ttf", 20)
except Exception:
    try:
        font_badge = ImageFont.truetype("segoeuib.ttf", 22)
        font_tag = ImageFont.truetype("cour.ttf", 18)
        font_label = ImageFont.truetype("segoeuib.ttf", 20)
    except Exception:
        font_badge = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_label = ImageFont.load_default()

def draw_sky_and_sun(draw, sky_top=(110, 165, 225), sky_bottom=(210, 230, 250)):
    for y in range(int(H * 0.65)):
        ratio = y / (H * 0.65)
        r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * ratio)
        g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * ratio)
        b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # Sun glow
    draw.ellipse([W - 180, 20, W - 60, 140], fill=(255, 255, 240, 90))

# 1. BBMP: Iconic Red Brick Corporation Building
def render_bbmp():
    img = Image.new('RGB', (W, H), (230, 240, 250))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (80, 140, 215), (205, 225, 245))
    
    # Ground lawn
    draw.rectangle([0, int(H * 0.72), W, H], fill=(55, 115, 65))
    draw.rectangle([0, int(H * 0.88), W, H], fill=(85, 90, 95)) # Roadway foreground
    draw.line([(0, int(H * 0.94)), (W, int(H * 0.94))], fill=(240, 240, 240), width=4) # Road stripe
    
    # Red-brick Victorian Corporation Building
    brick_main = (165, 52, 45)
    brick_dark = (130, 38, 32)
    brick_light = (195, 75, 65)
    stone_trim = (235, 225, 205)
    
    # Main building wings
    draw.rectangle([80, 180, W - 80, int(H * 0.75)], fill=brick_main)
    # Brick horizontal courses
    for y in range(195, int(H * 0.75), 18):
        draw.line([(80, y), (W - 80, y)], fill=brick_dark, width=2)
        
    # Stone plinth and roof cornice
    draw.rectangle([70, 170, W - 70, 184], fill=stone_trim)
    draw.rectangle([65, int(H * 0.73), W - 65, int(H * 0.76)], fill=stone_trim)
    
    # Central Tower with Clock
    draw.rectangle([W//2 - 65, 95, W//2 + 65, int(H * 0.75)], fill=brick_dark)
    draw.rectangle([W//2 - 70, 85, W//2 + 70, 98], fill=stone_trim)
    # Tower pyramid roof
    draw.polygon([(W//2 - 75, 85), (W//2, 28), (W//2 + 75, 85)], fill=(110, 30, 25))
    # Clock face
    draw.ellipse([W//2 - 25, 115, W//2 + 25, 165], fill=(255, 255, 255), outline=stone_trim, width=3)
    draw.line([(W//2, 140), (W//2, 126)], fill=(20, 20, 20), width=3) # Hour hand
    draw.line([(W//2, 140), (W//2 + 12, 140)], fill=(20, 20, 20), width=2) # Minute hand
    
    # Indian Flag atop spire
    draw.line([(W//2, 28), (W//2, 2)], fill=(200, 200, 200), width=2)
    draw.rectangle([W//2, 4, W//2 + 35, 10], fill=(255, 153, 51))
    draw.rectangle([W//2, 10, W//2 + 35, 16], fill=(255, 255, 255))
    draw.rectangle([W//2, 16, W//2 + 35, 22], fill=(19, 136, 8))
    
    # Arched Windows
    for col in range(110, W - 110, 52):
        if abs(col - W//2) < 45: continue
        # Upper window
        draw.rounded_rectangle([col, 205, col + 28, 255], radius=14, fill=(40, 55, 75))
        draw.arc([col, 205, col + 28, 233], start=180, end=360, fill=stone_trim, width=3)
        # Lower window
        draw.rounded_rectangle([col, 280, col + 28, 335], radius=6, fill=(40, 55, 75))
        
    # Ornamental palm and ashoka trees in foreground
    for tx in [40, 90, 160, W - 160, W - 90, W - 40]:
        draw.ellipse([tx - 25, int(H * 0.58), tx + 25, int(H * 0.74)], fill=(35, 95, 45))
        draw.ellipse([tx - 18, int(H * 0.60), tx + 18, int(H * 0.73)], fill=(50, 130, 60))
        draw.rectangle([tx - 3, int(H * 0.72), tx + 3, int(H * 0.76)], fill=(80, 50, 30))
        
    return img

# 2. BDA: Modern Planned Bengaluru Urban Layout
def render_bda():
    img = Image.new('RGB', (W, H), (210, 230, 245))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (95, 155, 225), (200, 225, 245))
    
    # Distant modern skyline
    for b in [(40, 140, 120), (180, 110, 90), (300, 160, 110), (450, 120, 130), (600, 150, 100), (710, 130, 80)]:
        bx, by, bw = b
        draw.rectangle([bx, by, bx + bw, 290], fill=(160, 185, 210))
        for wy in range(by + 15, 280, 18):
            for wx in range(bx + 10, bx + bw - 10, 16):
                draw.rectangle([wx, wy, wx + 8, wy + 10], fill=(225, 240, 255))
                
    # Planned wide dual-carriageway boulevard with central landscaped median
    draw.polygon([(W//2 - 60, 260), (W//2 + 60, 260), (W + 200, H), (-200, H)], fill=(70, 75, 82))
    # Green median in center
    draw.polygon([(W//2 - 12, 260), (W//2 + 12, 260), (W//2 + 35, H), (W//2 - 35, H)], fill=(40, 110, 50))
    # Road markings
    draw.line([(W//2 - 35, 260), (-80, H)], fill=(255, 255, 255), width=4)
    draw.line([(W//2 + 35, 260), (W + 80, H)], fill=(255, 255, 255), width=4)
    
    # Planned BDA layout plots on sides with green trees
    draw.polygon([(0, 260), (W//2 - 70, 260), (-200, H), (0, H)], fill=(65, 125, 60))
    draw.polygon([(W//2 + 70, 260), (W, 260), (W, H), (W + 200, H)], fill=(65, 125, 60))
    
    # Modern Glass BDA Complex on right
    draw.rectangle([W - 280, 160, W - 40, int(H * 0.72)], fill=(45, 90, 140))
    # Glass curtain panels
    for gy in range(175, int(H * 0.70), 22):
        for gx in range(W - 265, W - 55, 28):
            draw.rectangle([gx, gy, gx + 22, gy + 16], fill=(135, 185, 235))
            
    # Avenue trees along median and sidewalks
    for ty in range(270, int(H * 0.85), 28):
        scale = (ty - 240) / 200.0
        rad = int(14 + 18 * scale)
        cx_med = W // 2
        draw.ellipse([cx_med - rad//2, ty - rad//2, cx_med + rad//2, ty + rad//2], fill=(45, 135, 55))
        
    return img

# 3. BMRDA: Regional Satellite Growth Zones & Cloverleaf Highway
def render_bmrda():
    img = Image.new('RGB', (W, H), (200, 220, 240))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (75, 130, 200), (190, 215, 240))
    
    # Sweeping rural/satellite landscape
    draw.rectangle([0, 180, W, H], fill=(85, 145, 70))
    
    # Satellite township grid patches
    draw.polygon([(80, 190), (320, 190), (280, 260), (50, 260)], fill=(120, 165, 100))
    draw.polygon([(480, 200), (720, 200), (760, 270), (520, 270)], fill=(130, 175, 110))
    
    # Multilane high-speed expressway cloverleaf interchange
    road_col = (75, 80, 88)
    # Main highway left-to-right curve
    for t in range(0, 100):
        x = int(W * (t / 100.0))
        y = int(320 + 80 * math.sin(t * 0.04))
        draw.circle((x, y), 32, fill=road_col)
        
    # Cross highway overpass
    draw.polygon([(W//2 - 50, 170), (W//2 + 50, 170), (W//2 + 90, H), (W//2 - 90, H)], fill=(65, 70, 78))
    # Overpass concrete bridge parapet
    draw.rectangle([W//2 - 80, 290, W//2 + 80, 310], fill=(190, 195, 200))
    
    # Cloverleaf loop ramps
    draw.arc([160, 240, 340, 420], start=30, end=270, fill=(70, 75, 82), width=24)
    draw.arc([460, 240, 640, 420], start=210, end=90, fill=(70, 75, 82), width=24)
    
    # White lane lines
    draw.line([(0, 380), (W, 350)], fill=(255, 255, 255), width=3)
    draw.line([(W//2, 170), (W//2, H)], fill=(255, 255, 255), width=3)
    
    # Clustered forest & avenue trees
    for cx in range(30, W, 70):
        cy = int(210 + 40 * math.sin(cx * 0.05))
        draw.ellipse([cx - 20, cy - 18, cx + 20, cy + 18], fill=(45, 115, 50))
        
    return img

# 4. BMICAPA: NICE Expressway Corridor Interchange
def render_bmicapa():
    img = Image.new('RGB', (W, H), (200, 220, 240))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (65, 125, 200), (185, 215, 240))
    
    # Rolling green terrain of Bangalore-Mysore corridor
    draw.polygon([(0, 180), (W, 200), (W, H), (0, H)], fill=(70, 135, 60))
    # Distant hills
    draw.chord([50, 120, 450, 260], 180, 360, fill=(110, 155, 130))
    draw.chord([380, 100, 780, 270], 180, 360, fill=(95, 140, 115))
    
    # Grand expressway curve sweeping into foreground
    road_col = (68, 72, 80)
    for i in range(120):
        prog = i / 120.0
        cx = int(W * 0.85 - prog * W * 0.65)
        cy = int(200 + prog * 280)
        thick = int(24 + prog * 60)
        draw.circle((cx, cy), thick // 2, fill=road_col)
        
    # Flyover overpass bridge cutting across
    draw.polygon([(0, 280), (W, 330), (W, 385), (0, 335)], fill=(60, 65, 72))
    # Concrete parapet barrier
    draw.line([(0, 280), (W, 330)], fill=(225, 230, 235), width=5)
    draw.line([(0, 335), (W, 385)], fill=(225, 230, 235), width=5)
    # Bridge piers
    draw.rectangle([W//3 - 15, 340, W//3 + 15, 460], fill=(180, 185, 190))
    draw.rectangle([2*W//3 - 15, 355, 2*W//3 + 15, 470], fill=(180, 185, 190))
    
    # Lush trees along highway buffers
    for tx in range(20, W, 55):
        ty = int(220 + 35 * math.cos(tx * 0.03))
        draw.ellipse([tx - 22, ty - 22, tx + 22, ty + 22], fill=(35, 105, 45))
        
    return img

# 5. BMRCL: Namma Metro Train on Viaduct
def render_bmrcl():
    img = Image.new('RGB', (W, H), (200, 225, 245))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (70, 135, 215), (195, 220, 245))
    
    # City landscape & roadway below
    draw.rectangle([0, int(H * 0.65), W, H], fill=(65, 70, 78)) # Roadway below
    draw.rectangle([0, int(H * 0.62), W, int(H * 0.66)], fill=(50, 120, 55)) # Green buffer
    
    # Modern elevated concrete viaduct spans across the scene
    viaduct_top = 220
    viaduct_bot = 270
    draw.rectangle([0, viaduct_top, W, viaduct_bot], fill=(185, 190, 198))
    draw.rectangle([0, viaduct_top - 12, W, viaduct_top], fill=(155, 160, 168)) # Track slab
    # Concrete piers supporting viaduct
    for px in [120, 360, 600]:
        draw.rectangle([px - 22, viaduct_bot, px + 22, int(H * 0.85)], fill=(175, 180, 188))
        draw.polygon([(px - 38, viaduct_bot), (px + 38, viaduct_bot), (px + 22, viaduct_bot + 25), (px - 22, viaduct_bot + 25)], fill=(150, 155, 162))
        
    # Namma Metro Modern Train (Green & Silver/White livery)
    train_x = 180
    train_y = 120
    train_w = 460
    train_h = 92
    
    # Aerodynamic front nose
    draw.rounded_rectangle([train_x, train_y, train_x + train_w, train_y + train_h], radius=16, fill=(240, 245, 250))
    # Namma Metro Signature Green Belt Stripe
    draw.rectangle([train_x, train_y + 48, train_x + train_w, train_y + 68], fill=(34, 150, 60))
    # Dark window band
    draw.rectangle([train_x + 30, train_y + 14, train_x + train_w - 15, train_y + 44], fill=(30, 42, 56))
    # Individual train windows
    for wx in range(train_x + 50, train_x + train_w - 40, 48):
        draw.rounded_rectangle([wx, train_y + 16, wx + 36, train_y + 42], radius=4, fill=(130, 175, 210))
        
    # Metro driver front windshield
    draw.polygon([(train_x + 10, train_y + 18), (train_x + 40, train_y + 18), (train_x + 35, train_y + 48), (train_x + 4, train_y + 48)], fill=(20, 35, 50))
    # Headlights
    draw.ellipse([train_x + 6, train_y + 70, train_x + 18, train_y + 82], fill=(255, 255, 200))
    
    # Sleek metro station in background
    draw.rounded_rectangle([W - 240, 70, W + 40, 240], radius=24, fill=(215, 225, 235))
    draw.rectangle([W - 230, 95, W + 20, 180], fill=(80, 130, 180)) # Glass station facade
    
    return img

# 6. KIADB: State Industrial Areas & Tech Park Entrance Gateway
def render_kiadb():
    img = Image.new('RGB', (W, H), (210, 230, 245))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (85, 145, 220), (200, 225, 245))
    
    # Industrial park green landscape & driveway
    draw.rectangle([0, int(H * 0.62), W, H], fill=(55, 125, 60))
    draw.polygon([(W//2 - 40, int(H * 0.62)), (W//2 + 40, int(H * 0.62)), (W + 80, H), (-80, H)], fill=(75, 80, 88))
    
    # Modern industrial factory / high-tech park buildings in background
    draw.rectangle([80, 170, 280, int(H * 0.65)], fill=(225, 230, 238))
    draw.rectangle([95, 195, 265, 240], fill=(50, 95, 145)) # Factory glass strip
    draw.rectangle([W - 320, 150, W - 60, int(H * 0.65)], fill=(210, 220, 230))
    draw.rectangle([W - 305, 175, W - 75, 230], fill=(40, 80, 130))
    
    # Monumental KIADB Entrance Arch Gateway
    arch_color = (215, 205, 190) # Granite stone
    arch_shadow = (175, 165, 150)
    
    # Left pillar
    draw.rectangle([W//2 - 210, 140, W//2 - 130, int(H * 0.75)], fill=arch_color)
    draw.rectangle([W//2 - 215, 130, W//2 - 125, 145], fill=arch_shadow)
    # Right pillar
    draw.rectangle([W//2 + 130, 140, W//2 + 210, int(H * 0.75)], fill=arch_color)
    draw.rectangle([W//2 + 125, 130, W//2 + 215, 145], fill=arch_shadow)
    # Connecting lintel arch beam
    draw.rectangle([W//2 - 230, 120, W//2 + 230, 165], fill=arch_color)
    draw.rectangle([W//2 - 235, 110, W//2 + 235, 125], fill=arch_shadow)
    
    # Gate Signboard: KIADB AEROSPACE & IT PARK
    draw.rectangle([W//2 - 160, 132, W//2 + 160, 154], fill=(20, 45, 80))
    
    # Landscaped flower beds
    for fx in range(60, W - 60, 40):
        if abs(fx - W//2) < 90: continue
        draw.ellipse([fx - 18, int(H * 0.66), fx + 18, int(H * 0.76)], fill=(210, 60, 60))
        draw.ellipse([fx - 14, int(H * 0.68), fx + 14, int(H * 0.74)], fill=(240, 200, 50))
        
    return img

# 7. CITB: Historic Heritage Bangalore Boulevard & Canopied Layout
def render_citb():
    img = Image.new('RGB', (W, H), (200, 220, 240))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (80, 140, 215), (195, 220, 240))
    
    # Tree-lined quiet heritage avenue (Malleswaram / Kumara Park style)
    draw.polygon([(W//2 - 50, 230), (W//2 + 50, 230), (W + 150, H), (-150, H)], fill=(75, 78, 82))
    draw.rectangle([0, int(H * 0.60), W, H], fill=(50, 110, 55))
    
    # Classic stone compound walls and heritage villas
    draw.rectangle([40, 240, 240, int(H * 0.68)], fill=(235, 230, 215))
    draw.polygon([(30, 240), (140, 185), (250, 240)], fill=(175, 65, 45)) # Mangalore tile roof
    draw.rectangle([W - 260, 230, W - 50, int(H * 0.68)], fill=(230, 225, 210))
    draw.polygon([(W - 270, 230), (W - 155, 175), (W - 40, 230)], fill=(175, 65, 45))
    
    # Majestic canopy of old rain trees arching over road
    for tree_x in [80, 180, W - 180, W - 80]:
        # Trunk
        draw.rectangle([tree_x - 14, 180, tree_x + 14, int(H * 0.75)], fill=(70, 50, 35))
        # Dense interlocking green foliage
        draw.ellipse([tree_x - 140, 40, tree_x + 140, 220], fill=(30, 85, 40))
        draw.ellipse([tree_x - 110, 60, tree_x + 110, 200], fill=(45, 115, 50))
        
    # Vintage Green Layout Signboard (CITB / Historic Bangalore layout post)
    draw.rectangle([W//2 + 90, 260, W//2 + 98, 420], fill=(60, 65, 70)) # Post
    draw.rectangle([W//2 + 40, 270, W//2 + 180, 320], fill=(24, 95, 48), outline=(255, 255, 255), width=2)
    # Signboard text lines
    draw.line([(W//2 + 50, 285), (W//2 + 170, 285)], fill=(255, 255, 255), width=3)
    draw.line([(W//2 + 50, 302), (W//2 + 150, 302)], fill=(255, 255, 255), width=2)
    
    return img

# 8. RERA: Statutory Luxury High-Rise Construction & Urban Growth
def render_rera():
    img = Image.new('RGB', (W, H), (210, 230, 250))
    draw = ImageDraw.Draw(img)
    draw_sky_and_sun(draw, (65, 130, 210), (190, 215, 245))
    
    # Modern luxury residential high-rise towers
    tower_color = (215, 220, 228)
    glass_color = (55, 115, 175)
    
    # Background tower
    draw.rectangle([90, 120, 250, int(H * 0.85)], fill=(185, 195, 208))
    for ty in range(140, int(H * 0.82), 24):
        draw.rectangle([110, ty, 230, ty + 14], fill=(90, 135, 180))
        
    # Main prominent tower
    tx, ty, tw, th = 310, 60, 290, int(H * 0.88)
    draw.rectangle([tx, ty, tx + tw, th], fill=tower_color)
    
    # Balconies and glass facade
    for floor_y in range(ty + 20, th - 20, 28):
        # Floor slab
        draw.rectangle([tx - 8, floor_y + 16, tx + tw + 8, floor_y + 22], fill=(245, 248, 252))
        # Glass windows
        draw.rectangle([tx + 15, floor_y, tx + tw - 15, floor_y + 16], fill=glass_color)
        for pane_x in range(tx + 25, tx + tw - 20, 35):
            draw.line([(pane_x, floor_y), (pane_x, floor_y + 16)], fill=(200, 215, 230), width=2)
            
    # Construction crane atop tower signifying active compliant project
    draw.rectangle([tx + 120, 25, tx + 130, 60], fill=(230, 160, 25)) # Mast
    draw.line([(tx + 40, 28), (tx + 240, 28)], fill=(230, 160, 25), width=4) # Jib
    draw.line([(tx + 125, 10), (tx + 40, 28)], fill=(230, 160, 25), width=2)
    draw.line([(tx + 125, 10), (tx + 240, 28)], fill=(230, 160, 25), width=2)
    
    # Foreground trees
    for gx in [40, 140, W - 140, W - 40]:
        draw.ellipse([gx - 30, int(H * 0.72), gx + 30, int(H * 0.92)], fill=(35, 100, 45))
        
    return img

configs = [
    ('dept-bbmp', render_bbmp, 'BBMP', 'KAR-AUTH-01', 'Greater Bengaluru Civic Works', 'bbmp'),
    ('dept-bda', render_bda, 'BDA', 'KAR-AUTH-02', 'Bengaluru Urban Planning', 'bda'),
    ('dept-bmrda', render_bmrda, 'BMRDA', 'KAR-AUTH-03', 'Metropolitan Regional Planning', 'karnataka'),
    ('dept-bmicapa', render_bmicapa, 'BMICAPA', 'KAR-AUTH-04', 'NICE Expressway Corridor', 'karnataka'),
    ('dept-bmrcl', render_bmrcl, 'BMRCL', 'KAR-AUTH-05', 'Namma Metro Transit Network', 'bmrcl'),
    ('dept-kiadb', render_kiadb, 'KIADB', 'KAR-AUTH-06', 'State Industrial Estates', 'kiadb'),
    ('dept-citb', render_citb, 'CITB', 'KAR-AUTH-07', 'Heritage Planned Layouts', 'karnataka'),
    ('dept-rera', render_rera, 'RERA', 'KAR-AUTH-08', 'Statutory Project Regulatory Board', 'rera')
]

for filename, render_fn, acronym, tag, label, emblem_type in configs:
    # 1. Base photographic artwork
    base = render_fn()
    # 2. Add smooth gradient scrim for contrast
    composed = create_gradient_scrim(base)
    draw = ImageDraw.Draw(composed)
    
    # 3. Top-left dark forest green pill badge
    draw_pill(draw, x=24, y=24, text=acronym, bg_color=(23, 56, 45, 240), text_color=(255, 255, 255), font=font_badge, pad_x=18, pad_y=8, r=6)
    
    # 4. Top-right translucent frosted tag
    draw_pill(draw, x=W - 170, y=24, text=tag, bg_color=(255, 255, 255, 220), text_color=(45, 55, 72), font=font_tag, pad_x=14, pad_y=8, r=6)
    
    # 5. Bottom-left label text with soft shadow
    draw.text((26, H - 54), label, fill=(0, 0, 0, 180), font=font_label)
    draw.text((24, H - 56), label, fill=(255, 255, 255), font=font_label)
    
    # 6. Bottom-right circular seal medallion (72px)
    draw_emblem_seal(composed, x=W - 96, y=H - 96, size=72, emblem_type=emblem_type)
    
    # Save 1x WebP (800x500)
    out_1x = f'assets/img/dept/{filename}.webp'
    composed.save(out_1x, 'WEBP', quality=95)
    
    # Save 2x WebP (1600x1000) with Lanczos upsampling
    composed_2x = composed.resize((W * 2, H * 2), Image.Resampling.LANCZOS)
    out_2x = f'assets/img/dept/{filename}-2x.webp'
    composed_2x.save(out_2x, 'WEBP', quality=95)
    
    print(f"Generated {out_1x} (800x500) & {out_2x} (1600x1000) for {acronym}!")

print("\nAll 8 crystal-clear, high-resolution authority images generated successfully!")

