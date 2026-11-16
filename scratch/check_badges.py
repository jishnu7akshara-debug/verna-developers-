from PIL import Image

im1 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')
im2 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826183984_eb290f4c.jpg')

# Let's crop the top left corner of im1 and im2 to see the badges!
badge1 = im1.crop((35, 25, 90, 50))
badge1.save('scratch/badge_im1.png')

badge2 = im2.crop((35, 25, 90, 50))
badge2.save('scratch/badge_im2.png')

print("Saved badges")

