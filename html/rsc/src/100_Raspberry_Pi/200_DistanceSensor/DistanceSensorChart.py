from gpiozero import DistanceSensor  # gpiozero 라이브러리에서 DistanceSensor 클래스를 가져옵니다.
from time import sleep  # 시간 지연을 위해 time 모듈에서 sleep 함수를 가져옵니다.
import matplotlib.pyplot as plt  # 실시간 그래프를 그리기 위해 matplotlib의 pyplot을 가져옵니다.
from matplotlib.animation import FuncAnimation  # 실시간 애니메이션을 만들기 위해 FuncAnimation을 가져옵니다.

# 초음파 거리 센서를 초기화합니다.
distanceSensor = DistanceSensor(echo=17, trigger=4)

# 그래프 초기 설정
fig, ax = plt.subplots()
plt.grid(1, linestyle='--', color="g")
x_data, y_data = [], []
line, = ax.plot(x_data, y_data)
# x축과 y축에 라벨 추가
ax.set_xlabel('Time (100 ms)')  # x축 설명을 설정
ax.set_ylabel('Distance (cm)')  # y축 설명을 설정

def update(frame):
    global x_data, y_data

    x_data.append(frame)  # 현재 시간을 x 축 데이터로 사용합니다.
    y_data.append(distanceSensor.distance*100)  # 센서의 측정 거리(cm)를 y 축 데이터로 사용합니다.

    while len( x_data ) > 50 : # 데이터 개수를 50개 이하로 유지
        x_data.pop( 0 )
        y_data.pop( 0 )
    pass

    line.set_data(x_data, y_data)
    ax.set_xlim(max(0, frame - 50), frame + 10)  # x 축을 실시간으로 업데이트합니다.
    ax.set_ylim(0, max(40, max(y_data) + 5 ) )  # y 축 범위를 설정합니다. (센서의 최대 범위에 따라 조정)

    return line,

# 애니메이션 설정
ani = FuncAnimation(fig, update, interval=100)  # 100ms 간격으로 업데이트

plt.show()  # 그래프를 화면에 표시합니다.
