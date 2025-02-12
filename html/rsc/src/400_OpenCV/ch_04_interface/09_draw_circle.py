# 원 그리기
import numpy as np
import cv2
from matplotlib import pyplot as plt

red, green, blue  = (255, 0, 0), (0, 255, 0), (0, 0, 255)
white, black = (255, 255, 255), (0, 0, 0)
image = np.full((300, 500, 3),white, np.uint8)

center = (image.shape[1]//2, image.shape[0]//2) # 중심 좌표 - 역순 구성
pt1, pt2 = (300, 50), (100, 220) # 문자열 위치 좌표
shade = (pt2[0] + 2, pt2[1] + 2) # 그림자 좌표

cv2.circle(image, center, 100, blue)
cv2.circle(image, pt1, 50, green, 2)
cv2.circle(image, pt2, 70, red, -1)

font = cv2.FONT_HERSHEY_COMPLEX # 폰트 지정

cv2.putText(image, "center_blue", center, font, 1.2, black)
cv2.putText(image, "center_blue", center, font, 1.0, blue)
cv2.putText(image, "pt1_green", pt1, font, 0.8, green)
cv2.putText(image, "pt2_red", shade,font, 1.2, black, 2)
cv2.putText(image, "pt2_red", pt2, font, 1.2, red, 1)

plt.imshow(image)
plt.show()
