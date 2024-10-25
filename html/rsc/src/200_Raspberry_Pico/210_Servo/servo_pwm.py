from machine import Pin, PWM
from time import sleep

# 서보 모터 설정 (핀 1번에 연결)
servo = PWM(Pin(1))
servo.freq(50)  # 서보 모터의 PWM 주파수 설정 (50Hz)

duration = 0.5
count = 0 
for percent in range( 2, 14 ) :
    count += 1
    duty_u16 = 65535*percent//100
    print( f"[{count:2d}] duty_u16 = {duty_u16:4d}, duty_cycle ={percent:3d}%" ) 
    servo.duty_u16( duty_u16 )
    sleep( duration )  # 대기 
pass

# 프로그램 종료 시 서보 모터 PWM 해제
servo.deinit()