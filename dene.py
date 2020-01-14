import os
import numpy as np
import cv2
from PIL import Image 
 
# Gri tonlamalı resim yükleme
img = cv2.imread('deneme.jpg', 0)
import cv2

a = os.listdir('./images')
#frame = cv2.imread(a[-1]).tobytes()
img = Image.open("./images/"+ a[-1])
img.show()
print(img)
