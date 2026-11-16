from PIL import Image
import numpy as np

arr1 = np.array(Image.open('scratch/emblem_check1.png'))
print('arr1 shape:', arr1.shape)
# Find the circular emblem center and radius
# where in y does the photo end?
# Let's inspect the bottom rows
print('y from 30 to 55 (relative to 130):')
for y in range(30, arr1.shape[0], 3):
    # inspect right edge
    print(f"y={130+y}: rightmost 10 pixels avg={np.mean(arr1[y, 40:55, :3], axis=0)}")

