import RPi.GPIO as GPIO
from time import sleep

# GPIO 핀 번호 설정 (예: GPIO18)
ESC_PIN = 18

# PWM 신호 범위 설정
FREQUENCY = 50  # PWM 주파수 (50Hz)
MIN_DUTY_CYCLE = 5  # 1ms 신호 (5% Duty Cycle)
MAX_DUTY_CYCLE = 10  # 2ms 신호 (10% Duty Cycle)

# GPIO 및 PWM 초기화
GPIO.setmode(GPIO.BCM)  # BCM 핀 넘버링 사용
GPIO.setup(ESC_PIN, GPIO.OUT)  # ESC 핀이 출력으로 설정

pwm = GPIO.PWM(ESC_PIN, FREQUENCY)  # PWM 객체 생성
pwm.start(0)  # PWM 신호 초기화 (Duty Cycle = 0)

def calibrate_esc():
    try:
        print("ESC 캘리브레이션 시작")

        # 최대 신호 전송
        print("최대 신호 전송 중...")
        pwm.ChangeDutyCycle(MAX_DUTY_CYCLE)
        sleep(2)  # ESC가 최대 신호를 받아들일 때까지 대기

        # 최소 신호 전송
        print("최소 신호 전송 중...")
        pwm.ChangeDutyCycle(MIN_DUTY_CYCLE)
        sleep(2)  # ESC가 최소 신호를 받아들일 때까지 대기

        print("ESC 캘리브레이션 완료!")
    except KeyboardInterrupt:
        print("ESC 캘리브레이션 중단")
    finally:
        pwm.ChangeDutyCycle(0)  # 신호 중지
        pwm.stop()  # PWM 종료
        GPIO.cleanup()  # GPIO 상태 초기화

# 실행
if __name__ == "__main__":
    calibrate_esc()
