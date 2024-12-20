import time
import pigpio

# PWM 핀 설정
ESC_PIN = 18  # 예시로 GPIO18을 사용, 필요에 따라 수정 가능

# PWM 주파수 및 범위 설정
MIN_PULSE_WIDTH = 1000  # ESC의 최소 PWM (1ms)
MAX_PULSE_WIDTH = 2000  # ESC의 최대 PWM (2ms)

# pigpio 초기화
pi = pigpio.pi()

if not pi.connected:
    print("pigpio daemon이 실행 중인지 확인하세요.")
    exit()

# ESC 초기화 (모터 정지)
pi.set_mode(ESC_PIN, pigpio.OUTPUT)
pi.set_servo_pulsewidth(ESC_PIN, MIN_PULSE_WIDTH)
time.sleep(2)  # ESC가 최소 신호를 받아들일 때까지 대기

# 최대 신호 전송
print("최대 신호 전송 중...")
pi.set_servo_pulsewidth(ESC_PIN, MAX_PULSE_WIDTH)
time.sleep(2)  # ESC가 최대 신호를 받아들일 때까지 대기

# 최소 신호로 복귀
print("최소 신호 전송 중...")
pi.set_servo_pulsewidth(ESC_PIN, MIN_PULSE_WIDTH)
time.sleep(2)  # ESC가 최소 신호로 복귀할 때까지 대기

# 캘리브레이션 완료 메시지 출력
print("ESC 캘리브레이션 완료!")

# 종료
pi.set_servo_pulsewidth(ESC_PIN, 0)  # PWM 신호 종료
pi.stop()  # pigpio 종료
