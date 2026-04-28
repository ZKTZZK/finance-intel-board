from PIL import Image
import os

img = Image.open(r'D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_edge.png')
print(f"Original: {img.size[0]}x{img.size[1]}")

# Find actual content height by checking pixel alpha/brightness
import numpy as np
arr = np.array(img.convert('RGBA'))

# Check each row for non-white content
# White background pixels are around 255,255,255 or close to it
# Find last row with significant content (not all white/near-white)
threshold = 240
row_max = arr.max(axis=(1, 2))  # max value per row

# Find first and last rows with content
for top in range(arr.shape[0]):
    if row_max[top] < 255:
        break

for bottom in range(arr.shape[0] - 1, -1, -1):
    if row_max[bottom] < 255:
        break

# Add some padding
padding = 10
top = max(0, top - padding)
bottom = min(arr.shape[0], bottom + padding)

print(f"Content bounds: top={top}, bottom={bottom}, height={bottom-top}")

# Crop
cropped = img.crop((0, top, img.size[0], bottom))
out_path = r'D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_20260428_final.png'
cropped.save(out_path, 'PNG')
print(f"Saved: {cropped.size[0]}x{cropped.size[1]} to {out_path}")
img.close()
