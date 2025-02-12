# servo_cali.py
# 서보 암을 중앙 방향으로 부착합니다.

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

servo = Servo(17, pin_factory=PiGPIOFactory())

duration = 1

print( "Start calibrating ...\n" )

count = 0 
for _ in range( 3 ) :
    count += 1
    print( f"{count:2d}: Locating servo min angle ..." )
    servo.min()
    sleep( duration )
    print( f"{count:2d}: Servo value = {servo.value:4.1f}" )

    count += 1
    print( f"{count:2d}: Locating servo middle angle ..." )
    servo.mid()
    sleep( duration )
    print( f"{count:2d}: Servo value = {servo.value:4.1f}" )

    count += 1
    print( f"{count:2d}: Locating servo max angle ..." )
    servo.max()
    sleep( duration )
    print( f"{count:2d}: Servo value = {servo.value:4.1f}" )

    count += 1
    print( f"{count:2d}: Locating servo middle angle ..." )
    servo.mid()
    sleep( duration )
    print( f"{count:2d}: Servo value = {servo.value:4.1f}" )
pass

print( "\nAttach the servo arm at 90 degree!" )