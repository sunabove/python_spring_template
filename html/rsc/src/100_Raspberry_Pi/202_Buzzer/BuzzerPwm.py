# gpiozero 라이브러리의 PWMLED 임포트
from gpiozero import PWMLED
# time 모듈에서 sleep 함수를 임포트하여 시간 지연 사용
from time import sleep

# GPIO 4번 핀에 연결된 부저를 PWMLED 객체로 생성 
# PWM 제어를 위해 PWMLED 사용
buzzer = PWMLED(4)  

# 0에서 100까지 10씩 증가시키면서 PWM duty cycle을 조절
# PWM duty cycle에 따라 부저의 출력 강도가 조절됨
for i in range(0, 101, 10):  
    buzzer.value = i / 100  # PWM duty cycle을 0.0에서 1.0 사이로 설정
    sleep(0.4)  # 0.4초 동안 현재 설정된 PWM 값으로 부저를 유지
pass