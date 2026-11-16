from PIL import Image
import numpy as np

im = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794827005185_3aa1a0dc.png')
# Save original user logo as assets/img/verna-logo-full.png
im.save('assets/img/verna-logo-full.png')

# Create clean transparent version where white/near-white becomes transparent
arr = np.array(im.convert('RGBA'))
# Calculate luminance: 0 is black, 255 is white
rgb = arr[:, :, :3].astype(float)
lum = 0.299 * rgb[:,:,0] + 0.587 * rgb[:,:,1] + 0.114 * rgb[:,:,2]

# Where luminance is near 255, make transparent
# Let's create smooth antialiased alpha based on darkness
alpha = np.clip((255.0 - lum) * (255.0 / 220.0), 0, 255).astype(np.uint8)

# Foreground is deep navy / black: rgb=[16, 24, 40]
transparent_arr = np.zeros_like(arr)
transparent_arr[:, :, 0] = 16  # dark navy
transparent_arr[:, :, 1] = 24
transparent_arr[:, :, 2] = 40
transparent_arr[:, :, 3] = alpha

trans_img = Image.fromarray(transparent_arr, 'RGBA')
trans_img.save('assets/img/verna-logo-transparent.png')

# Let's also create 2x and 3x upscaled versions with LANCZOS
w, h = im.size
trans_img_2x = trans_img.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
trans_img_2x.save('assets/img/verna-logo-transparent-2x.png')

trans_img_3x = trans_img.resize((w * 3, h * 3), Image.Resampling.LANCZOS)
trans_img_3x.save('assets/img/verna-logo-transparent-3x.png')

print("Logo processed and saved!")

