"""
Some transparent image behave weird, this fixes that. Background should be white transparent.
"""


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os




image_path = os.path.join("Input", "instagram_inverse.png")
image = Image.open(image_path)
img = image.convert("RGBA")

img_array = np.asarray(img).copy()

for i in range(img_array.shape[0]):
    for j in range(img_array.shape[1]):
        if img_array[i, j, 3] == 0:
            img_array[i, j] = [255, 255, 255, 0]

image_fixed = Image.fromarray(img_array)
plt.imshow(img_array)
#plt.show()
image_fixed.save(os.path.join("Input", "instagram_inverse.png"))