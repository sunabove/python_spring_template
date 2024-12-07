# 2_shift_register.py

import RPi.GPIO as GPIO
import time

# 핀 번호 설정
DS = 10       # 데이터 입력 핀
SHCP = 11     # 쉬프트 레지스터 클럭 핀
STCP = 8      # 저장 레지스터 클럭 (래치) 핀

# GPIO 설정
GPIO.setwarnings( 0 )            # 경고 메시지 비활성화
GPIO.setmode(GPIO.BCM)           # BCM 핀 번호 사용
GPIO.setup(DS, GPIO.OUT)         # DS 핀 출력으로 설정
GPIO.setup(SHCP, GPIO.OUT)       # SHCP 핀 출력으로 설정
GPIO.setup(STCP, GPIO.OUT)       # STCP 핀 출력으로 설정

# 쉬프트 레지스터로 데이터 전송 함수
def shift_out(data):
    # 데이터의 각 비트를 쉬프트 레지스터에 전송
    for bit in range(8):  # 8비트 데이터 처리
        # 현재 비트를 DS 핀으로 출력 (MSB부터 LSB 순으로 전송)
        GPIO.output(DS, data & (1 << (7 - bit)))
        # SHCP 클럭 핀을 HIGH -> LOW로 펄스 전송
        GPIO.output(SHCP, GPIO.HIGH)
        GPIO.output(SHCP, GPIO.LOW)
    pass
pass

# 래치 함수 (출력 갱신)
def latch():
    # STCP 핀을 HIGH -> LOW로 펄스 전송하여 출력 갱신
    GPIO.output(STCP, GPIO.HIGH)
    GPIO.output(STCP, GPIO.LOW)
pass

# 메인 루프
try:
    count = 1  # 카운터 초기값 설정
    duration = 4 # 대기 시간
    while 1:
        # 0부터 7까지 증가한 뒤 다시 감소
        data2 = 0
        for i in range(4) :
            data = i << 1    # 비트 쉬프트 연산
            print( f"[{count:4d}]", end="" )
            print( f"   (1st) {data:>4d} = {data:>08b} (b)", end="" )
            print( f"   (2nd) {data2:>4d} = {data2:>08b} (b)", flush=1 )
            shift_out(data)  # 데이터 전송
            latch()          # 출력 갱신
            time.sleep( duration )  # 대기
            data2 = data
            count += 1       # 카운트 증가
        pass 
    pass
except KeyboardInterrupt:
    # Ctrl+C로 종료 시 GPIO 핀 초기화
    GPIO.cleanup()
pass
