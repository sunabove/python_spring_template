# 직선 그리기 예제

import numpy as np
import cv2
from matplotlib import pyplot as plt

green, red = (0, 255, 0), (255, 0, 0 )
image = np.zeros((400, 600,3), np.uint8)  # 3채널 영상
image[:] = 255 # 3채널 흰색
image[:] = 126 # 3채널 흰색

pt1, pt2 = (50, 50), (250, 150)
pt3, pt4 = (400, 150), (500, 50) 

cv2.line(image, pt1, pt2, red)
cv2.line(image, pt3, pt4, green, 3, cv2.LINE_AA) # 계산 현상 감소선

plt.imshow(image) # 영상 출력
plt.show()