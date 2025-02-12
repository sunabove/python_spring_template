# 사각형 그리기 예제
import numpy as np
import cv2
from matplotlib import pyplot as plt

blue, green, red = (0, 0, 255), (0, 255, 0), (255, 0, 0)
image = np.zeros((400, 600, 3), np.uint8)  # 3채널 영상
image[:] = 255 # 3채널 흰색

pt1, pt2 = (50, 50), (250, 150)
pt3, pt4 = (400, 150), (500, 50) 
roi = (50, 200, 200, 100) # 사각형 영역 = 4원소 튜플

cv2.rectangle(image, pt1, pt2, blue, 3, cv2.LINE_4) # 4방향 연결선
cv2.rectangle(image, roi, red, 3, cv2.LINE_8) # 8방향 연결선
cv2.rectangle(image, (400, 200, 100, 100), green, cv2.FILLED) # 내부채움

plt.imshow(image)
plt.show()