from PIL import Image
import numpy as np

im = Image.open('scratch/card5_strip.png')
arr = np.array(im)
for y in range(0, 200, 5):
    avg_col = np.mean(arr[y, :, :3], axis=0)
    print(f"y={y}: avg={avg_col}")

