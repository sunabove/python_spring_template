# 타원 호 그리기
import numpy as np
import cv2
from matplotlib import pyplot as plt

# 색상 지정
orange, blue, white = (255, 165, 0), (0, 0, 255), (255, 255, 255)
# 영상 생성
image = np.full((300, 700, 3), white, np.uint8)

pt1, pt2 = (180, 150), (550, 150)   # 타원 중심점
size = (120, 60)                    # 타원의 반지름

# 타원의 중심점(2화소 원) 표시
cv2.circle(image, pt1, 1, (0, 0, 255), 4)
cv2.circle(image, pt2, 1, (255, 0, 0), 4)

# 호 그리기
cv2.ellipse(image, pt1, size,  0,  30, 270, orange, 12)
cv2.ellipse(image, pt2, size, 90, -45,  90, orange, 12)

# 타원 그리기
cv2.ellipse(image, pt1, size,  0, 0, 360, blue, 4)
cv2.ellipse(image, pt2, size, 90, 0, 360, blue, 4)

plt.imshow( image ) 
plt.show()