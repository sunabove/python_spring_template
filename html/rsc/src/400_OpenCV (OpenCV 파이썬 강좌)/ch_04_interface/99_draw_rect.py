# 사각형 그리기 예제
import numpy as np
import cv2
from matplotlib import pyplot as plt

cyan, red = (0, 255, 255), (255, 0, 0)
image = np.zeros((100, 200, 3), np.uint8)  # 3채널 영상
image[:] = 255 # 3채널 흰색

cv2.rectangle(image, (50, 25, 100, 50), cyan, cv2.FILLED) 
cv2.rectangle(image, (50, 25, 100, 50), red, 2, cv2.LINE_8 )

plt.imshow(image)
plt.show()