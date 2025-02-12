import RPi.GPIO as GPIO
import dht11
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# GPIO 초기화 및 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# DHT11 센서를 GPIO 14번 핀에 연결
instance = dht11.DHT11(pin=14)

# 데이터 저장용 리스트 초기화
temperature_data = []
humidity_data    = []
time_data        = []

# 그래프 설정
fig, ax1 = plt.subplots()
fig.suptitle('DHT11 Sensor Data')

ax2 = ax1.twinx()  # 공유 x축을 가진 두 번째 y축

def animate(i):
    result = instance.read()
    if result.is_valid():        
        current_time = datetime.now().strftime("%M:%S")
        temperature_data.append(result.temperature)
        humidity_data.append(result.humidity)
        time_data.append(current_time)

        print(current_time, f"Temperature: {result.temperature:.1f} °C", f"Humidity: {result.humidity:.1f} %")

        # 최근 20개 데이터만 유지
        if len(time_data) > 20:
            time_data.pop(0)
            temperature_data.pop(0)
            humidity_data.pop(0)
        pass
        
        # 온도 데이터 업데이트
        ax1.clear()
        ax2.clear()
        
        ax1.plot(time_data, temperature_data, 'r--o', label='Temperature (°C)')
        ax2.plot(time_data, humidity_data, 'b--*', label='Humidity (%)')
        
        # 설정 갱신
        ax1.set_xlabel('Time')
        # 그리드설정
        ax1.grid(which='major', axis='both', linestyle='--')

        ax1.set_ylabel('Temperature (°C)', color='red')
        ax2.set_ylabel('Humidity (%)', color='blue')
        ax2.yaxis.set_label_position( "right" )
        ax2.yaxis.tick_right()
        
        ax1.tick_params(axis='y', labelcolor='red')
        ax2.tick_params(axis='y', labelcolor='blue')

        ax1.set_ylim( 0, 80 ) # 온도 y축 최대값 설정
        ax2.set_ylim( 0, 80 ) # 습도 y축 최대값 설정
        
        # x축 눈금 각도 조정
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # 그래프 범례
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # 서브플롯 사이 간격 조정
        plt.subplots_adjust(hspace=0.5)
    pass
pass

# 애니메이션 설정
ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    print( "\nProgram stopped by User")
finally:
    GPIO.cleanup()
pass
