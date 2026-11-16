from PIL import Image
import numpy as np

for fname, idx_name in [('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg', 'row1'),
                        ('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826183984_eb290f4c.jpg', 'row2')]:
    im = Image.open(fname)
    w, h = im.size
    print(f'=== {idx_name} ({w}x{h}) ===')
    # Let's inspect a horizontal line through the photo area around y=50
    # and find where border between cards is
    rgb = np.array(im)
    # Check y=25 to 160
    # Let's see background color outside cards
    print('top left pixel:', rgb[5, 5])
    # Let's find columns where card border exists
    # Look at a row in the middle of card photos, e.g. y=80
    row_pixels = rgb[80, :, :3]
    # In between cards there is background gap
    # Let's look at y=10 to find card tops

