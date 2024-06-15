# servo_pwm_loop.py
# GPIO 핀 17을 사용하여 PWM 신호를 생성합니다. 

import RPi.GPIO as GPIO  # 표준 Raspberry Pi GPIO 라이브러리 임포트
from time import sleep   # 프로그램에 대기(일시 정지) 기능 추가
GPIO.setmode(GPIO.BCM)   # 핀 번호 체계를 BCM 모드로 설정

GPIO.setup(17, GPIO.OUT)  # 핀 17을 출력으로 설정
p = GPIO.PWM(17, 50)      # 핀 17을 PWM 핀으로 설정하고 주파수를 50Hz로 설정
p.start(0)                # PWM 시작, 듀티 사이클을 0으로 설정
sleep(1)                 # 1초 대기

while True :

    for i in [ 1, -1 ] : 
        for dc in range( 6 - 6*i, 6 + 6*i + i, i ):
            print( f"dc = {dc}" )
            # 듀티 사이클을 변경하여 서보 모터를 특정 각도로 이동
            p.ChangeDutyCycle( dc )
            
            sleep( 0.5 ) 
        pass
    pass

pass

p.stop()        # PWM을 중지
GPIO.cleanup()  # GPIO 핀을 기본값으로 재설정