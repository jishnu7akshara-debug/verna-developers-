from PIL import Image

im1 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')
im2 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826183984_eb290f4c.jpg')

# In im1, height is 404. Let's crop the bottom of card 1: (30, 300, 264, 404)
bot1 = im1.crop((30, 320, 264, 404))
bot1.save('scratch/bot1.png')

bot2 = im2.crop((28, 300, 256, 381))
bot2.save('scratch/bot2.png')

print("Saved footer crops")

