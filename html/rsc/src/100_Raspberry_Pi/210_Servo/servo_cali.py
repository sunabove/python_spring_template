# servo_cali.py
# 서보를 중앙에 위치시킵니다.
# 서보 암을 중앙 방향으로 부착합니다.

from gpiozero import Servo
from time import sleep

servo = Servo(17)

while True:
    servo.mid()
    sleep( 2 )
pass