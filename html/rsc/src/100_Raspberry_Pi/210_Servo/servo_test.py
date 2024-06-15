# servo_test.py
# 서보의 암을 최소 -> 중간 -> 최대 -> 중간 
# 설정을 무한 반복 합니다.
from gpiozero import Servo
from time import sleep

servo = Servo(17)

while True:
    servo.min()
    print( "servo min")
    sleep( 2 )
    servo.mid()
    print( "servo mid")
    sleep( 2 )
    servo.max()
    print( "servo max")
    sleep( 2 )
    servo.mid()
    print( "servo mid")
    sleep( 2 )
pass