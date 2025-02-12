print( "Hello.... Motor Test." )
import sys
sys.path.append('/home/pi/Navio2/Python')

import time
from navio.pwm import PWM

# 모터 설정
MOTOR_PIN = 0  # Navio2의 1번 모터 핀 (0부터 시작)
PWM_FREQUENCY = 50  # PWM 주파수 (50Hz)
ESC_MIN = 1.0  # ESC 최소 펄스 (ms)
ESC_MAX = 2.0  # ESC 최대 펄스 (ms)
ESC_NEUTRAL = 1.5  # 중립값 (ms)

def initialize_motor(pwm):
    print("모터 초기화 중...")
    pwm.set_duty_cycle(ESC_NEUTRAL)  # 모터를 중립 상태로 설정
    time.sleep(2)  # ESC 초기화 대기

def test_motor(pwm):
    try:
        # 최소값으로 테스트
        print("모터 최소 출력 테스트 중...")
        pwm.set_duty_cycle(ESC_MIN)
        time.sleep(2)

        # 최대값으로 테스트
        print("모터 최대 출력 테스트 중...")
        pwm.set_duty_cycle(ESC_MAX)
        time.sleep(2)

        # 중립값으로 복원
        print("모터 중립 상태로 복원...")
        pwm.set_duty_cycle(ESC_NEUTRAL)
        time.sleep(2)
    finally:
        pwm.disable()
        print("모터 테스트 종료.")
    pass
pass

if __name__ == "__main__":
    pwm = PWM(MOTOR_PIN)
    pwm.initialize()
    pwm.set_period(PWM_FREQUENCY)  # 50Hz PWM 신호 설정

    initialize_motor(pwm)
    test_motor(pwm)
pass