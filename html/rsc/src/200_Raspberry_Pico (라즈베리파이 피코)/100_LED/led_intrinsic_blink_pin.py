from machine import Pin, Timer

inbuiltLed = 25

led = Pin(inbuiltLed, Pin.OUT)

timer = Timer()

def ledblink(timer):

    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=ledblink)