# liquid_level_test.py
from gpiozero import Button
from time import sleep

liquidSensor = Button( 14 )

count = 0
def when_pressed() :
    global count
    count += 1

    print( f"[{count:2d}] No water detected." )
pass

def when_released() :
    global count
    count += 1

    print( f"[{count:2d}] Water detected." )
pass

liquidSensor.when_pressed = when_pressed
liquidSensor.when_released = when_released

input( "Press Enter to quit...\n" )
print( "Good bye!")
