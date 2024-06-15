# servo_test.py
# 서보의 위치를 값을 통하여 제어합니다.
from gpiozero import Servo
from time import sleep

servo = Servo(17)

value = -1.0
dir = 1
while True :
    value += (dir*0.1)
    if value > 1 :
        dir = -1
        value = 1.0
    elif value < -1 :
        dir = +1
        value = -1.0
    pass

    servo.value = value
    sleep( 2 )
    print( f"value = {value:+1.1f}, servo.value = {servo.value:+1.1f}, dir = {dir}" )
pass