# 23_matplatlib_basic_plot.py

import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

# 데이터 생성
x = [ 1, 2, 3, 4, 5 ]
y = [ 1, 3, 5, 7, 9 ]

# 그래프 생성
plt.plot( x, y, '--' )

# 그래프 제목 및 라벨 설정
plt.title( 'My Simple Line Plot' )
plt.xlabel( 'My X-axis' )
plt.ylabel( 'My Y-axis' )

# 그래프 표시
plt.show()