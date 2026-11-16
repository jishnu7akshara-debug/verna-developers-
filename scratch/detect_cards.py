from PIL import Image
import numpy as np

def analyze(img_path):
    im = Image.open(img_path)
    arr = np.array(im)
    h, w, _ = arr.shape
    # Check which pixels are NOT pure white (or very close to 255)
    non_white = np.mean(arr[:, :, :3], axis=2) < 250
    
    # row profile
    row_counts = np.sum(non_white, axis=1)
    col_counts = np.sum(non_white, axis=0)
    
    top = np.where(row_counts > 10)[0][0]
    bottom = np.where(row_counts > 10)[0][-1]
    
    print(f"File: {img_path}")
    print(f"Vertical bounds: {top} to {bottom}")
    
    # Find columns where cards are
    # Gap between cards has low non_white count
    in_card = False
    cards = []
    start_c = None
    for c in range(w):
        # column has non-white pixels
        if np.sum(non_white[top:bottom, c]) > 10:
            if not in_card:
                in_card = True
                start_c = c
        else:
            if in_card:
                in_card = False
                cards.append((start_c, c))
    if in_card:
        cards.append((start_c, w))
    
    print(f"Found {len(cards)} cards: {cards}")
    return top, bottom, cards

top1, bottom1, cards1 = analyze('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826177929_9f78780a.jpg')
top2, bottom2, cards2 = analyze('C:/Users/admin/.gemini/antigravity/brain/e66b7736-7567-4103-a04f-1cefadac29fd/.user_uploaded/media_1794826183984_eb290f4c.jpg')

