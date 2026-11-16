import os
from PIL import Image

os.makedirs('scratch/extracted_photos', exist_ok=True)

im1 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')
im2 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826183984_eb290f4c.jpg')

# In im1:
# Card 1 (BBMP): (30, 24, 263, 169)
# Card 2 (BDA): (281, 24, 514, 169)
# Card 3 (BMRDA): (531, 24, 764, 169)
# Card 4 (BMICAPA): (782, 24, 1015, 169)

crops1 = [
    ('bbmp', (30, 24, 263, 169)),
    ('bda', (281, 24, 514, 169)),
    ('bmrda', (531, 24, 764, 169)),
    ('bmicapa', (782, 24, 1015, 169))
]

for name, box in crops1:
    cr = im1.crop(box)
    cr.save(f'scratch/extracted_photos/{name}.png')
    print(f"Saved {name}: {cr.size}")

# In im2:
# Card 5 (BMRCL): (28, 22, 256, 165)
# Card 6 (KIADB): (272, 22, 500, 165)
# Card 7 (CITB): (514, 22, 742, 165)
# Card 8 (RERA): (759, 22, 987, 165)

crops2 = [
    ('bmrcl', (28, 22, 256, 165)),
    ('kiadb', (272, 22, 500, 165)),
    ('citb', (514, 22, 742, 165)),
    ('rera', (759, 22, 987, 165))
]

for name, box in crops2:
    cr = im2.crop(box)
    cr.save(f'scratch/extracted_photos/{name}.png')
    print(f"Saved {name}: {cr.size}")

