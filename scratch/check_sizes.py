from PIL import Image

for name in ['bbmp', 'bda', 'bmrda', 'bmicapa', 'bmrcl', 'kiadb', 'citb', 'rera']:
    im = Image.open(f'scratch/extracted_photos/{name}.png')
    print(f"{name}: size={im.size}")

