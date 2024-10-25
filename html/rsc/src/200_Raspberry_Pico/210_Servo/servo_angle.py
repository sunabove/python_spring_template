from picozero import Servo
from time import sleep

print( "Hello ...\n" )

servo = Servo(1)
servo.value = 0
sleep( 0.5 )

for i in range(0, 101, 5):
    servo.value = i / 100
    print( f"[{i//5:2d}] servo.value = {servo.value:4.2f}" )
    sleep(0.25)
pass

servo.off()
servo.close()

print( "\nGood bye!" )