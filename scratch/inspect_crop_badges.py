from PIL import Image
import numpy as np

# In im1:
# Let's see what badge is in each crop of im1 and im2
for f in ['bbmp.png', 'bda.png', 'bmrda.png', 'bmicapa.png', 'bmrcl.png', 'kiadb.png', 'citb.png', 'rera.png']:
    im = Image.open('scratch/extracted_photos/' + f)
    # Check top-left corner (x: 10..60, y: 5..30)
    crop_badge = im.crop((10, 5, 60, 30))
    # print avg color of crop_badge
    print(f, "size:", im.size, "badge corner avg:", np.mean(crop_badge, axis=(0,1)))

