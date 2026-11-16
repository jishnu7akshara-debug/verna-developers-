from PIL import Image

im = Image.open('scratch/extracted_photos/bbmp.png')
print("bbmp size:", im.size)
# The size is (233, 145).
# On a screen where card is 260px or 280px wide, 233px is close to 1x.
# If we upscale to 466x290 or 600x373 using Pillow LANCZOS, let's see how it looks.
im_up = im.resize((560, 348), Image.Resampling.LANCZOS)
im_up.save('scratch/bbmp_upscaled.webp', quality=92)
print("Saved upscaled test")

