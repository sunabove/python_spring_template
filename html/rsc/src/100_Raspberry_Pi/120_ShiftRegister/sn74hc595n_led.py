import RPi.GPIO as GPIO
import time

# 핀 번호 설정
DS = 10
SHCP = 11
STCP = 8

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(DS, GPIO.OUT)
GPIO.setup(SHCP, GPIO.OUT)
GPIO.setup(STCP, GPIO.OUT)

def shift_out(data):
    for bit in range(8):
        GPIO.output(DS, data & (1 << (7 - bit)))
        GPIO.output(SHCP, GPIO.HIGH)
        GPIO.output(SHCP, GPIO.LOW)

def latch():
    GPIO.output(STCP, GPIO.HIGH)
    GPIO.output(STCP, GPIO.LOW)

try:
    while True:
        for i in range(256):  # 0~255
            shift_out(i)
            latch()
            time.sleep(0.1)
        pass
    pass
except KeyboardInterrupt:
    GPIO.cleanup()
pass