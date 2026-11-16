from PIL import Image

im1 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')
width, height = im1.size

# Each row has 4 cards. Let's inspect where the cards start and end.
# In im1, top is around y=20, photo height is around 150px.
# Let's save a crop of the first card's photo area to see.
card1_photo = im1.crop((28, 20, 252, 168))
card1_photo.save('scratch/test_crop1.png')

print("Saved test crop")

