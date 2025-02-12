# 문자 출력 예제
import numpy as np
import cv2
from matplotlib import pyplot as plt

olive, violet, brown = (0, 128, 128), (221, 160, 221), (165, 42 , 42) 
pt1, pt2 = (50, 230), (50, 310) # 문자열 위치 좌표

image = np.zeros((350, 500,3), np.uint8)
image.fill(255)

cv2.putText(image, "SIMPLEX", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, brown)
cv2.putText(image, "DUPLEX", (50, 120), cv2.FONT_HERSHEY_DUPLEX, 2, olive)
cv2.putText(image, "TRIPLEX", pt1, cv2.FONT_HERSHEY_TRIPLEX, 2, violet)
fontFace = cv2.FONT_HERSHEY_PLAIN | cv2.FONT_ITALIC 
cv2.putText(image, "ITALIC ", pt2, fontFace, 2, violet)

plt.imshow(image) 
plt.show()