# 26_matplotlib_interplation.py

import matplotlib.pyplot as plt
import numpy as np

# 보간법의 종류
methods = ['none', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36']

# 0 ~ 1 사이의 임의 난수로 5x5 그리드(행렬, 영상)를 생성
grid = np.random.rand( 5, 5 )

# 2x3 형태의 서브플롯 생성 (총 6개의 플롯)
fig, axs = plt.subplots( nrows=2, ncols=3, figsize=(8, 6) )

# 각 서브플롯에 대해 다른 보간법을 적용하여 이미지 표시
for ax, method in zip( axs.flat, methods ):
    ax.imshow( grid, interpolation=method, cmap='gray' )  # 명암도 영상 표시
    ax.set_title( method )  # 보간법 이름을 제목으로 설정
pass

# 서브플롯 간격을 자동으로 조정
plt.tight_layout()

# 모든 플롯을 화면에 표시
plt.show()
