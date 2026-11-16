from PIL import Image

im1 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')
im2 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826183984_eb290f4c.jpg')

# Let's crop the text area below the first card in im1 and im2!
# x: 30..250, y: 170..230
im1.crop((30, 170, 250, 230)).save('scratch/im1_title.png')
im2.crop((30, 170, 250, 230)).save('scratch/im2_title.png')
print("Saved im1_title and im2_title")

