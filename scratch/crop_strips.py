from PIL import Image

im1 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')
im2 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826183984_eb290f4c.jpg')

# Let's see the cards in im1:
# Card 1: x in [30, 264]
# Card 2: x in [281, 515]
# Card 3: x in [531, 764]
# Card 4: x in [782, 1015]

# Where does the photo start and end vertically?
# In im1, top is around y=55 or so, let's find the card's top border.
# Let's save a vertical strip of card 1:
card1_strip = im1.crop((30, 0, 264, 250))
card1_strip.save('scratch/card1_strip.png')

card5_strip = im2.crop((28, 0, 256, 250))
card5_strip.save('scratch/card5_strip.png')

print("Saved card strips")

