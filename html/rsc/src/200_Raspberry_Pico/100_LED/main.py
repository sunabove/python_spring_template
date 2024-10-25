from machine import Pin, Timer

led = Pin(25, Pin.OUT)

timer = Timer()

def ledblink(timer):
    led.toggle()
pass

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=ledblink)