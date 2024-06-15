# servo_angle.py
# 서보의 위치를 값을 통하여 제어합니다.
from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17)

angle = -90
dir = 1
while True :
    angle += (dir*5)
    if angle >= 90 :
        dir = -1
        angle = 90
    elif angle <= -90 :
        dir = +1
        value = -90
    pass
    servo.angle = angle
    sleep( 2 )
    print( f"angle = {angle:+}, servo.angle = {servo.angle:+}, dir = {dir:+}" )
pass