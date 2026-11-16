from PIL import Image
import os

for f in sorted(os.listdir('scratch/extracted_photos')):
    if f.endswith('.png'):
        im = Image.open('scratch/extracted_photos/' + f)
        print(f, im.size)

