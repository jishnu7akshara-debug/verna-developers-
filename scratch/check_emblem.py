from PIL import Image
import numpy as np

im1 = Image.open('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')

# Let's crop around the bottom-right of card 1 photo (around x: 200..265, y: 135..185)
emblem_crop1 = im1.crop((200, 130, 260, 185))
emblem_crop1.save('scratch/emblem_check1.png')

# Let's check card 2 emblem (x: 450..515, y: 130..185)
emblem_crop2 = im1.crop((450, 130, 515, 185))
emblem_crop2.save('scratch/emblem_check2.png')

print("Saved emblem check crops")

