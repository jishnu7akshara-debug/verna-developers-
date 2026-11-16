import os
from PIL import Image, ImageFilter

os.makedirs('assets/img/dept', exist_ok=True)

# Let's see the crops from im1 and im2
crops = [
    ('dept-bbmp', 'bbmp'),
    ('dept-bda', 'bda'),
    ('dept-bmrda', 'bmrda'),
    ('dept-bmicapa', 'bmicapa'),
    ('dept-bmrcl', 'bmrcl'),
    ('dept-kiadb', 'kiadb'),
    ('dept-citb', 'citb'),
    ('dept-rera', 'rera'),
]

for out_name, in_name in crops:
    im = Image.open(f'scratch/extracted_photos/{in_name}.png')
    # Let's save 1x and high-quality 2x webp
    im.save(f'assets/img/dept/{out_name}.webp', quality=95)
    # 2x upscale with Lanczos
    w, h = im.size
    im_2x = im.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
    im_2x.save(f'assets/img/dept/{out_name}-2x.webp', quality=95)
    print(f"Generated {out_name}.webp ({im.size}) and -2x.webp ({im_2x.size})")

print("All 8 department header images prepared!")

