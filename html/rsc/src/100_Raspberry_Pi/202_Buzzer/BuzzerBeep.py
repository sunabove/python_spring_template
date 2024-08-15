from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(pin=4, active_high=1)
buzzer.beep(on_time=1, off_time=0.5, n=4)

input("Enter to quit! ")