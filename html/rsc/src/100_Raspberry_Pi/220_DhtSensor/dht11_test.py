# dht11_test.py
import RPi.GPIO as GPIO
import dht11
from time import sleep

GPIO.setwarnings(False)  # GPIO 관련 경고를 비활성화
GPIO.setmode(GPIO.BCM)   # GPIO 핀 번호를 BCM 방식으로 설정

# DHT11 센서를 GPIO 14번 핀에 연결
instance = dht11.DHT11(pin=14)

try:
    while True:
        result = instance.read() # DHT11 센서로부터 데이터 읽기
        if result.is_valid(): # 유효한 데이터인 경우 온도와 습도를 출력
            print(f"Temperature: {result.temperature:.1f} °C", f" Humidity: {result.humidity:.1f} %")
        else: # 데이터가 유효하지 않은 경우 에러 코드 출력
            print(f"Error: {result.error_code}")
        pass
        
        sleep( 2 )  # 대기 후 다시 읽기
except KeyboardInterrupt: # 키보드 인터럽트(Ctrl+C)로 프로그램 중지
    print( "\nProgram stopped by User" )
finally: 
    GPIO.cleanup() # 프로그램 종료 시 GPIO 핀 정리 
pass