from PIL import Image

for name in ['dept-bbmp', 'dept-bda', 'dept-bmrda', 'dept-bmicapa', 'dept-bmrcl', 'dept-kiadb', 'dept-citb', 'dept-rera']:
    im = Image.open(f'assets/img/dept/{name}.webp')
    print(f"{name}: size={im.size}")

