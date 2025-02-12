# 24_matplatlib_sub_plot.py

import matplotlib.pyplot as plt
import numpy as np

# 데이터 생성
x = np.linspace( 0, 10, 100 )
y1 = np.sin( x )
y2 = np.cos( x )
y3 = y1 + y2

# 여러 그래프 생성
plt.figure()

# 첫 번째 그래프: 사인 함수
#plt.subplot( 2, 1, 1 )
plt.subplot( 311 )
plt.plot( x, y1 )
plt.title( 'My Sine' )

# 두 번째 그래프: 코사인 함수
#plt.subplot( 2, 1, 2 )
plt.subplot( 312 )
plt.plot( x, y2 )
plt.title( 'My Cosine' )

# 세 번째 그래프: 코사인 함수
#plt.subplot( 3, 1, 3 )
plt.subplot( 313 )
plt.plot( x, y3 )
plt.title( 'My Sine + Cosine' )

# 레이아웃을 조정하여 그림 중첩 방지
plt.tight_layout()

# 그래프 표시
plt.show()