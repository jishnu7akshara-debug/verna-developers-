from PIL import Image
import numpy as np

im = Image.open('scratch/card1_strip.png')
arr = np.array(im)
for y in range(0, arr.shape[0], 5):
    # print average color across width
    avg_col = np.mean(arr[y, :, :3], axis=0)
    print(f"y={y}: avg={avg_col}")

