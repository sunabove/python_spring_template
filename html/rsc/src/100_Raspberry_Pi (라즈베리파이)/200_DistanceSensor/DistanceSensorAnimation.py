# DistanceSensorAnimation.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gpiozero import DistanceSensor
import time

# 거리 센서 설정 (GPIO 핀 번호를 적절히 변경하세요)
sensor = DistanceSensor(echo=17, trigger=4)

# 그래프 설정
fig, ax = plt.subplots()
xdata, ydata = [], []
line, = ax.plot([], [], 'b-')

ax.set_ylim(0, 110)  # 거리 범위 (센티미터)
ax.set_xlim(0, 10)   # 시간 범위 (초)

# 축, 레이블 제목 설정
ax.set_title( "Distance Sensor" )
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Distance (cm)')

ax.grid(which='major', axis='both', linestyle='--')

# 시작 시간
start_time = time.time()

# 업데이트 함수: 이 함수는 새로운 데이터를 가져와서 그래프를 업데이트합니다.
def animate( frame ):
    current_time = time.time() - start_time
    distance = sensor.distance * 100  # meters to centimeters
    
    print( distance, "cm" )
    
    xdata.append(current_time)
    ydata.append(distance)
    
    # 축 업데이트
    if current_time > ax.get_xlim()[1]:
        ax.set_xlim(ax.get_xlim()[0], current_time + 1)
        ax.figure.canvas.draw()
    pass

    line.set_data(xdata, ydata)
    
    return line,
pass

# 애니메이션 설정
ani = animation.FuncAnimation(fig, animate, interval=10, blit=True)

# 그래프 표시
plt.show()
