import matplotlib.pyplot as plt
import numpy as np
from gpiozero import DistanceSensor
from time import sleep, time

# 거리 센서 설정 (GPIO 핀 번호를 적절히 변경하세요)
sensor = DistanceSensor(echo=18, trigger=17)

# 실시간 데이터 수집 및 플로팅을 위한 설정
duration = 20  # 데이터 수집 시간 (초)
interval = 0.1  # 데이터 수집 간격 (초)

# 데이터 저장을 위한 배열 초기화
times = []
distances = []

# 초기 시간 설정
start_time = time()

plt.ion()  # 인터랙티브 모드 켜기
fig, ax = plt.subplots()
line, = ax.plot(times, distances, 'b-')
ax.set_ylim(0, 200)  # 거리 범위 (센티미터)

# 데이터 수집 및 실시간 플로팅
try:
    while time() - start_time < duration:
        current_time = time() - start_time
        distance = sensor.distance * 100  # meters to centimeters
        
        times.append(current_time)
        distances.append(distance)
        
        # 그래프 업데이트
        line.set_xdata(times)
        line.set_ydata(distances)
        ax.relim()
        ax.autoscale_view()
        
        plt.draw()
        plt.pause(interval)
        sleep(interval)

except KeyboardInterrupt:
    print("Data collection stopped by user")

# 인터랙티브 모드 종료 및 최종 그래프 표시
plt.ioff()
plt.show()
