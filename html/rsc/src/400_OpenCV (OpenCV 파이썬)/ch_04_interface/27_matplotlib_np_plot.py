# 27_matplotlib_np_plot.py

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 현재 소스 파일의 폴더 경로를 가져옵니다.
dir = Path( __file__ ).resolve().parent

# x와 y 데이터 생성
x  = np.arange(10)
y1 = np.arange(10)
y2 = np.arange(10)**2
y3 = np.random.choice(50, size=10)

# 그림 객체 생성 - 그래프 크기 지정 (단위: 인치)
plt.figure(figsize=(10,6))

# y1 데이터를 파란색 파선으로 그리기
plt.plot(x, y1, 'b--', linewidth=2)

# y2 데이터를 녹색 원 마커와 실선으로 그리기
plt.plot(x, y2, 'go-', linewidth=3)

# y3 데이터를 청록색 플러스 마커와 점선으로 그리기
plt.plot(x, y3, 'c+:', linewidth=5)

# 그래프 제목 설정
plt.title("Line examples")

# 축 범위 설정
plt.axis([0, 10, 0, 80])

# 레이아웃 자동 조정
plt.tight_layout()

# 그래프를 'sample.png' 파일로 저장 (해상도: 300dpi)
plt.savefig(fname=dir.joinpath("img/sample.png"), dpi=300)

# 그래프 표시
plt.show()