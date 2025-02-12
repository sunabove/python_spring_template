# 사각형 라인 타입 차이 예제

import numpy as np, cv2
from matplotlib import pyplot as plt

# 이미지 생성
image = np.zeros((500, 500, 3), dtype=np.uint8)
image[ : ] = 255

# 사각형 그리기
cv2.rectangle(image, (50, 50), (450, 450), (255, 0, 0), 9, cv2.LINE_4)
cv2.rectangle(image, (70, 70), (430, 430), (0, 255, 0), 9, cv2.LINE_8)
cv2.rectangle(image, (90, 90), (410, 410), (0, 0, 255), 9, cv2.LINE_AA)

# 결과 보기
plt.imshow( image )
plt.show()