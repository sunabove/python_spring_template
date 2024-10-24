# servo_pwm.py
# GPIO 핀 17을 사용하여 PWM 신호로 서보 모터를 제어하는 프로그램

import RPi.GPIO as GPIO  # Raspberry Pi GPIO 제어를 위한 표준 라이브러리 임포트
from time import sleep   # 프로그램에 대기(일시 정지) 기능을 추가하기 위한 sleep 함수 임포트

# GPIO 경고 메시지를 비활성화하고 BCM 핀 번호 모드를 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)   # GPIO 핀 번호 체계를 BCM 모드로 설정

GPIO.setup(17, GPIO.OUT)  # GPIO 핀 17을 출력 모드로 설정

duration = 0.5  # 각 PWM 신호에서 대기할 시간 (0.5초)

frq = 50  # 서보 모터에 사용할 PWM 신호의 주파수 (50Hz)
p = GPIO.PWM(17, frq)  # GPIO 핀 17에 PWM 신호를 설정하고 주파수를 50Hz로 설정
p.start(0)  # PWM을 시작하고 듀티 사이클을 0으로 설정 (서보 모터가 움직이지 않음)
sleep(duration)  # 듀티 사이클이 0인 상태에서 대기
p.ChangeDutyCycle(0)  # 듀티 사이클을 0으로 설정 (안정화)
sleep(duration)  # 다시 대기

count = 0 # 실행 횟수
# 서보를 -90도에서 90도까지 증가시킨 후 다시 -90도로 감소시키는 동작을 2회 반복
for i in (list(range(0, 126, 5)) + list(range(125, -1, -5)))*2:
    count += 1 # 실행 횟수 증가
    dc = i / 10  # 듀티 사이클을 0에서 12.5까지 0.5씩 증가 또는 감소
    print(f"[{count:3d}] Pwm: freq: {frq} hz, duty cycle = {dc:4.1f} %")  # 현재 듀티 사이클 출력
    p.ChangeDutyCycle(dc)  # 듀티 사이클을 변경하여 서보 모터의 각도 제어
    sleep(duration)  # 각도 변경 후 대기
pass

# PWM 신호를 중지하고, GPIO 핀을 기본값으로 재설정
p.stop()  # PWM을 중지
GPIO.cleanup()  # 사용한 GPIO 핀을 초기 상태로 복구
