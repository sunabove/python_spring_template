# -*- coding: utf-8 -*-
print( "Hello.... Servo Test." )
import sys
sys.path.append('/home/pi/Navio2/Python')

import time

from navio.pwm import PWM

# 서보 관련 설정
SERVO_MIN = 1.0  # 최소 펄스 폭 (ms)
SERVO_MAX = 2.0  # 최대 펄스 폭 (ms)
SERVO_NEUTRAL = 1.5  # 중립 펄스 폭 (ms)

# Navio2 모터 핀 설정
MOTOR_PIN = 0  # 1번 모터 핀 (0부터 시작)

def test_servo():
    # PWM 객체 초기화
    pwm = PWM(MOTOR_PIN)
    pwm.initialize()
    pwm.set_period(50)  # 주기 설정 (50Hz)

    try:
        print("서보를 중립 위치로 이동 중...")
        pwm.set_duty_cycle(SERVO_NEUTRAL)
        time.sleep(2)

        print("서보를 최소 위치로 이동 중...")
        pwm.set_duty_cycle(SERVO_MIN)
        time.sleep(2)

        print("서보를 최대 위치로 이동 중...")
        pwm.set_duty_cycle(SERVO_MAX)
        time.sleep(2)

        print("서보 테스트 완료.")
    except KeyboardInterrupt:
        print("테스트 중단.")
    finally:
        pwm.disable() 
    pass
pass

if __name__ == "__main__":
    test_servo()
pass
