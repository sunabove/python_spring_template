# servo_angle.py
# 서보 각도를 제어합니다.

from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

servo = AngularServo(17, pin_factory=PiGPIOFactory())

angle = -90
dir = 1
duration = 0.5
angle_increment = 5
for _ in range( 180//angle_increment*2 ) : 
    angle = max( -90, min(90, angle) )
    servo.angle = angle
    print( f"angle = {angle:5.1f}, ", end="" )
    print( f"servo.angle = {servo.angle:5.1f}, ", end="" )
    print( f"dir = {dir:+2d}" )
    sleep( duration )

    angle += (dir*angle_increment) 

    if angle >=90 :
        dir = -1
    elif angle <= -90 :
        dir = 1
    pass
pass