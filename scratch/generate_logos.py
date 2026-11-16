from PIL import Image
import numpy as np

# Load user uploaded logo
im = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794827005185_3aa1a0dc.png')
w, h = im.size

# High-res 3x resize for crisp display
im_3x = im.resize((w * 3, h * 3), Image.Resampling.LANCZOS)
arr = np.array(im_3x.convert('RGBA'))

rgb = arr[:, :, :3].astype(float)
lum = 0.299 * rgb[:,:,0] + 0.587 * rgb[:,:,1] + 0.114 * rgb[:,:,2]

# Alpha: 0 where white (lum=255), 255 where black (lum=0)
alpha = np.clip((255.0 - lum) * (255.0 / 210.0), 0, 255).astype(np.uint8)

# 1. Dark logo on transparent background (Navy/Charcoal: #10224A)
dark_logo = np.zeros_like(arr)
dark_logo[:, :, 0] = 16   # R
dark_logo[:, :, 1] = 34   # G
dark_logo[:, :, 2] = 74   # B
dark_logo[:, :, 3] = alpha
Image.fromarray(dark_logo, 'RGBA').save('assets/img/verna-logo-dark.png')

# 2. Light logo on transparent background (Off-white / Cream: #FAF7F2)
light_logo = np.zeros_like(arr)
light_logo[:, :, 0] = 250 # R
light_logo[:, :, 1] = 247 # G
light_logo[:, :, 2] = 242 # B
light_logo[:, :, 3] = alpha
Image.fromarray(light_logo, 'RGBA').save('assets/img/verna-logo-white.png')

# 3. Gold accent logo (#C5A059)
gold_logo = np.zeros_like(arr)
gold_logo[:, :, 0] = 197
gold_logo[:, :, 1] = 160
gold_logo[:, :, 2] = 89
gold_logo[:, :, 3] = alpha
Image.fromarray(gold_logo, 'RGBA').save('assets/img/verna-logo-gold.png')

print("All crisp transparent logos generated successfully!")

