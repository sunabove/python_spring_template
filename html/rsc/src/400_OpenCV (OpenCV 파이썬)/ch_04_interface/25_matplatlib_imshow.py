# 25_matplatlib_imshow.py

import cv2
import matplotlib.pyplot as plt
from pathlib import Path

# 현재 소스 파일의 폴더 경로를 가져옵니다.
dir = Path( __file__ ).resolve().parent

# 이미지를 불러옵니다.
image = cv2.imread(dir.joinpath("img/matplot.jpg"), cv2.IMREAD_COLOR)

# 이미지의 행과 열(높이와 너비)을 가져옵니다.
rows, cols = image.shape[:2]

# 이미지를 BGR에서 RGB로 변환합니다.
rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 이미지를 그레이스케일로 변환합니다.
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 첫 번째 figure(챠트, 그라프, 플롯) 생성 (크기: 3x4 인치)
fig = plt.figure(num=1, figsize=(3, 4))

# 원본(BGR) 이미지를 표시합니다.
plt.imshow(image)
plt.title('figure1- original(bgr)')
plt.axis('off')  # 축을 표시하지 않습니다.
plt.tight_layout() # 레이아웃을 조정하여 챠트 요소가 겹치지 않도록 합니다.

# 두 번째 figure 생성 (크기: 6x4 인치)
fig = plt.figure(num=2, figsize=(6, 4))
plt.suptitle('figure2- pyplot image display')

# 서브플롯 1: RGB 이미지 표시
plt.subplot(1, 2, 1)
plt.imshow(rgb_img)
plt.axis([0, cols, rows, 0])  # 이미지의 축을 설정합니다.
plt.title('rgb color')

# 서브플롯 2: 그레이스케일 이미지 표시
plt.subplot(1, 2, 2)
plt.imshow(gray_img, cmap='gray')
plt.title('gray_img2')

plt.tight_layout() # 레이아웃을 조정하여 챠트 요소가 겹치지 않도록 합니다.
# 모든 플롯을 화면에 표시합니다.
plt.show()
