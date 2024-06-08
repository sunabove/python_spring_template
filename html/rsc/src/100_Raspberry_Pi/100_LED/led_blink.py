# 패키지 임포트
from gpiozero import LED
from time import sleep

# LED 생성
led = LED(17)

# 무한 반복
while True :
    led.on()    # LED 켜기
    sleep( 1 )  # 1초간 정지
    led.off()   # LED 꺼기
    sleep( 1 )  # 1초간 정지
pass