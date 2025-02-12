# 23_matplatlib_basic_plot_np.py

import matplotlib.pyplot as plt
import numpy as np

# 데이터 생성
x = [ 1, 2, 3, 4, 5 ]
y = [ 1, 3, 5, 7, 9 ]

x = np.arange( 1, 500 + 1 )
y = np.arange( 1, 1000 + 1, 2 )

# 그래프 생성
plt.plot( x, y )

# 그래프 제목 및 라벨 설정
plt.title('Simple Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# 그래프 표시
plt.show()