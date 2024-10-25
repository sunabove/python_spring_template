from machine import Pin, PWM  # GPIO 핀 제어를 위한 Pin과 PWM 클래스 임포트
from time import sleep  # 대기 기능을 위한 sleep 함수 임포트

# 프로그램 시작 메시지
print("Hello ...\n")

# 서보 모터 설정 (핀 1번에 연결)
pwm = PWM(Pin(1))  # 핀 1번에 PWM 신호 설정
pwm.freq(50)  # 서보 모터의 PWM 주파수를 50Hz로 설정 (서보 모터 기본 주파수)

# 각 듀티 사이클 변경 시 대기 시간
duration = 0.25  # 0.5초 대기
count = 0  # 실행 카운트 초기화

# 듀티 사이클을 2%에서 12.5%까지 증가시키며 서보 제어
values = list( range(20, 125 + 5, 5) ) # 2%부터 12.5%까지 각도를 증가
for value in ( values + values[-2:1:-1] ) * 4 :  
    count += 1  # 카운트 증가
    percent = value/1000
    duty_u16 = int( 65535 * percent ) # 듀티 사이클을 16비트 정수로 변환
    print(f"[{count:2d}] duty_u16 = {duty_u16:4d}, duty_cycle = {percent*100:4.1f}%")  # 현재 듀티 사이클 출력
    pwm.duty_u16(duty_u16)  # 듀티 사이클을 서보에 적용
    sleep(duration)  # 설정된 대기 시간 동안 대기
pass

# 서보 모터 종료
pwm.deinit()  # PWM을 해제하여 핀 초기화

# 프로그램 종료 메시지
print("\nGood bye!")