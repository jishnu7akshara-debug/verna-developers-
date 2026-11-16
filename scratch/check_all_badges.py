from PIL import Image

for name in ['dept-bbmp', 'dept-bda', 'dept-bmrda', 'dept-bmicapa', 'dept-bmrcl', 'dept-kiadb', 'dept-citb', 'dept-rera']:
    im = Image.open(f'assets/img/dept/{name}.webp')
    badge = im.crop((5, 5, 80, 40))
    badge.save(f'scratch/check_{name}_badge.png')
    print(f"Saved scratch/check_{name}_badge.png")

