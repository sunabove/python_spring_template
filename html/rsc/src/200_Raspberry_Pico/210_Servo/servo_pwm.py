from machine import Pin, PWM
from time import sleep

# 서보 모터 설정 (핀 1번에 연결)
servo = PWM(Pin(1))
servo.freq(50)  # 서보 모터의 PWM 주파수 설정 (50Hz)

# 최소 및 최대 듀티 사이클 설정 (서보 모터의 최소 및 최대 각도)
MIN_DUTY = 1638   # 0도 (약 2.5% 듀티 사이클)
MAX_DUTY = 8192   # 180도 (약 12.5% 듀티 사이클)

duration = 0.1
count = 0 
for duty in range( MIN_DUTY, MAX_DUTY + 116, 116 ) :
    count += 1    
    print( f"[{count:2d}] duty_u16 = {duty:4d}, duty_cycle ={duty/65535*100:6.2f}%" ) 
    servo.duty_u16( duty )
    sleep( duration )  # 대기 
pass

# 프로그램 종료 시 서보 모터 PWM 해제
servo.deinit()